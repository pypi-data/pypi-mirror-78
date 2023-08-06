import concurrent
import importlib
import logging
import threading
import time

from concurrent.futures.thread import ThreadPoolExecutor
from enum import Enum

from executor.job import JobFactory, Job


class DefaultJobFactory(JobFactory):

    def __init__(self):
        self._logger = logging.getLogger("yqg-py-scheduler.jobFactory")

    def create(self, class_name):
        try:
            tokens = class_name.split(".")
            module_name = ".".join(tokens[0:(len(tokens) - 1)])
            class_name = tokens[len(tokens) - 1]
            module = importlib.import_module(module_name)
            clazz = getattr(module, class_name)
        except Exception as ex:
            self._logger.exception("Error creating job instance from %s" % class_name)
            raise ex

        if issubclass(clazz, Job):
            return clazz()
        else:
            raise ValueError("%s is not subclass of Job" % class_name)


class TriggerState(Enum):
    INIT = 'INIT'
    RUNNING = 'RUNNING'
    INTERRUPTING = 'INTERRUPTING'
    INTERRUPTED = 'INTERRUPTED'
    DONE = 'DONE'


# 实现是not thread-safe，调用的类要保证线程安全
class Trigger(object):

    def __init__(self, tid, jid, name, job, params):
        self._tid = tid
        self._jid = jid
        self._name = name
        self._job = job
        self._params = params
        self._state = TriggerState.INIT
        self._result = None
        self._exception = None
        self._time_completed = None
        self._future = None

    def set_result(self, result):
        self._result = result
        self._time_completed = int(round(time.time() * 1000))

    def set_exception(self, exception):
        self._exception = exception
        self._time_completed = int(round(time.time() * 1000))

    def set_future(self, future):
        self._future = future

    def set_state(self, state):
        self._state = state

    def id(self):
        return self._tid

    def job_id(self):
        return self._jid

    def name(self):
        return self._name

    def job(self):
        return self._job

    def state(self):
        return self._state

    def result(self):
        return self._result

    def exception(self):
        return self._exception

    def future(self):
        return self._future

    def params(self):
        return self._params

    def time_completed(self):
        return self._time_completed

    def __str__(self):
        return "(%s, %s, %s, %s)" % (self._tid, self._jid, self._name, self._job.__class__.__name__)


class ExecutorState(Enum):
    STARTED = 'STARTED'
    SHUT_DOWN = 'SHUT_DOWN'


class IllegalStateException(Exception):

    def __init__(self, expect, actual):
        self._expect = expect
        self._actual = actual

    def __str__(self):
        if type(self.expect) is list:
            states = map(lambda x : x.name, self._expect)
            return "expect state %s, actual state %s" % (",".join(states), self._actual.name)
        else:
            return "expect state %s, actual state %s" % (self._expect.name, self._actual.name)


class DuplicateTriggerException(Exception):

    def __init__(self, trigger_id):
        self._trigger_id = trigger_id

    def __str__(self):
        return "duplicate trigger %s" % self._trigger_id


class TriggerNotFoundException(ValueError):

    def __init__(self, trigger_id):
        self._trigger_id = trigger_id

    def __str__(self):
        return "trigger %s can't be found" % self._trigger_id


class Executor(object):

    def __init__(self, threads_count=16, job_factory=None):
        self._thread_pool = ThreadPoolExecutor(max_workers=threads_count)
        self._job_factory = job_factory if job_factory else DefaultJobFactory()
        self._triggers = {} # 当前活跃的trigger, tid -> trigger
        self._logger = logging.getLogger("yqg-py-scheduler.executor")
        self._state = ExecutorState.STARTED
        self._state_lock = threading.RLock() # 控制executor内部的状态变更

    def shutdown(self, timeout=None):
        with self._state_lock:
            self._logger.info("shutting down executor")
            if self._state == ExecutorState.STARTED:
                self._state = ExecutorState.SHUT_DOWN
            else:
                return

        # interrupt all jobs
        for tid in self._triggers.keys():
            self._logger.info("interrupt trigger %s" % self._triggers[tid])
            self._triggers[tid].job().interrupt()
        self._thread_pool.shutdown(wait=False)

        # wait for all jobs to complete or timeout
        # thread pool没有内置的timeout，只能通过future来实现了
        remaining_timeout = timeout
        for tid in list(self._triggers.keys()):
            if tid not in self._triggers:
                # 有可能同步被删除了
                continue
            trigger = self._triggers[tid]
            future = trigger.future()
            self._logger.info("wait for result of %s" % trigger)
            start_time = time.time()
            try:
                future.result(timeout=remaining_timeout)
            except concurrent.futures._base.TimeoutError:
                # 将future的TimeoutError转化成原生的TimeoutError
                raise TimeoutError("Timeout while shutting down executor.")
            finally:
                remaining_timeout = max(remaining_timeout - (time.time() - start_time), 0)

        self._logger.info("executor was shut down")

    def trigger(self, tid, jid, name, class_name, params=None, callback=None):
        with self._state_lock:
            if self._state != ExecutorState.STARTED:
                raise IllegalStateException(ExecutorState.STARTED, self._state)

            if tid in self._triggers:
                raise DuplicateTriggerException(tid)

            # create trigger
            job = self._job_factory.create(class_name)
            trigger = Trigger(tid, jid, name, job, params)

            # submit to thread pool
            future = self._thread_pool.submit(self._run_job, trigger, callback)
            trigger.set_future(future)
            self._triggers[tid] = trigger

            self._logger.info("%s was submitted to thread pool" % trigger)

        return trigger

    def _run_job(self, trigger, callback=None):
        # update trigger state
        with self._state_lock:
            st = trigger.state()
            if st == TriggerState.INIT:
                trigger.set_state(TriggerState.RUNNING)
            elif st == TriggerState.INTERRUPTING:
                # thread pool的原理是，worker先从工作队列里获取work item，再执行
                # 有可能interrupt()的调用发生在获得work item之后，执行之前，此时future.cancel()无法成功
                # 这种情况的概率很小，以后优化下。
                pass
            else:
                raise IllegalStateException([TriggerState.INIT, TriggerState.INTERRUPTING], st)

        # do real work
        job = trigger.job()
        try:
            params = trigger.params() if trigger.params() else {}
            result = job.run(**params)
            job_run_result = (True, result)
        except Exception as ex:
            self._logger.exception("Error running job %s" % trigger)
            job_run_result = (False, ex)

        # update trigger
        with self._state_lock:
            if job_run_result[0]:
                trigger.set_result(job_run_result[1])
            else:
                trigger.set_exception(job_run_result[1])

            st = trigger.state()
            if st == TriggerState.RUNNING:
                trigger.set_state(TriggerState.DONE)
            elif st == TriggerState.INTERRUPTING:
                trigger.set_state(TriggerState.INTERRUPTED)
            else:
                raise IllegalStateException([TriggerState.RUNNING, TriggerState.INTERRUPTING], st)

            self._triggers.pop(trigger.id())

        # run callback if any
        if callback:
            try:
                callback(trigger)
            except:
                self._logger.exception("error running callback of trigger %s" % trigger)

    def interrupt(self, tid):
        with self._state_lock:
            if self._state != ExecutorState.STARTED:
                raise IllegalStateException(ExecutorState.STARTED, self._state)

            if tid not in self._triggers:
                raise TriggerNotFoundException(tid)

            trigger = self._triggers[tid]
            if trigger.state() in [TriggerState.DONE, TriggerState.INTERRUPTING, TriggerState.INTERRUPTED]:
                self._logger.info("%s was in state %s, cannot be interrupted" % (trigger, trigger.state()))
                return
            else:
                if trigger.future().cancel():
                    # job还没被thread pool执行，cancel成功
                    trigger.set_state(TriggerState.INTERRUPTED)
                    self._logger.info("%s was interrupted" % trigger)
                else:
                    # job已经被thread pool执行了，cancel失败
                    # 此时只能将状态置为INTERRUPTING，然后等待job结束
                    trigger.set_state(TriggerState.INTERRUPTING)
                    trigger.job().interrupt()
                    self._logger.info("%s was interrupting" % trigger)

    def triggers(self, tid=None):
        with self._state_lock:
            if tid is None:
                return self._triggers
            else:
                if tid not in self._triggers:
                    raise TriggerNotFoundException(tid)
                return self._triggers[tid]


class MockZKClient(object):

    def create(self, path, value=b"", acl=None, ephemeral=False,
               sequence=False, makepath=False, include_data=False):
        pass

    def start(self):
        pass

    def add_listener(self, listener):
        pass

    def remove_listener(self, listener):
        pass


class MockScheduler(object):

    def __init__(self):
        self._logger = logging.getLogger("yqg-py-scheduler.MockNotifier")

    def start(self):
        pass

    def metadata(self):
        return None

    def notify(self, trigger):
        self._logger.info("notify result of trigger %s" % trigger)

    def shutdown(self, timeout=None):
        pass