import json
import logging
import random
import threading
import uuid
import time
from abc import abstractmethod
from enum import Enum
from queue import PriorityQueue

import requests


class RetryStrategy(object):

    @abstractmethod
    def next_interval(self, item):
        """""
        当fn执行失败后，调用retry strategy获取下次执行时间，返回-1表示不需要重试
        :param item: Tuple(int, Tuple(fn, args, kwargs))
        :return: next interval
        """
        pass

    @abstractmethod
    def clear(self, item):
        """
        当fn执行成功后，调用retry strategy
        :param item: Tuple(int, Tuple(fn, args, kwargs))
        :return: None
        """
        pass


class NoRetryStrategy(RetryStrategy):

    def next_interval(self, item):
        return -1

    def clear(self, item):
        pass


class ExponentialRetryStrategy(RetryStrategy):
    """
    1. 失败后指数重试
    2. 每次增加一些随机的抖动
    3. 限制最大重试次数
    """

    def __init__(self, init_interval=1, max_interval=5, max_retries=10):
        self._init_interval = init_interval
        self._max_interval = max_interval
        if max_retries < 1:
            raise ValueError("max_retires should be larger than 1")
        self._max_retries = max_retries
        self._retries_count = {}
        self._intervals = {}

    def next_interval(self, item):
        prev_interval, exec_info = item
        if exec_info._id not in self._retries_count:
            self._retries_count[exec_info._id] = 1
            self._intervals[exec_info._id] = self._init_interval
            return self._init_interval
        else:
            if self._retries_count[exec_info._id] >= self._max_retries:
                return -1
            else:
                self._retries_count[exec_info._id] += 1
                jitter = random.uniform(0.5, 1.5)
                interval = min(self._intervals[exec_info._id] * 2 * jitter, self._max_interval)
                self._intervals[exec_info._id] = interval
                return interval

    def clear(self, item):
        prev_interval, exec_info = item
        self._intervals.pop(exec_info._id)
        self._retries_count.pop(exec_info._id)


class _ExecInfo(object):

    def __init__(self, fn, args, kwargs):
        self._id = uuid.uuid4()
        self._fn = fn
        self._args = args
        self._kwargs = kwargs


class _Timer(threading.Thread):
    """
    默认的timer类，每个timer对应一个线程，资源开销较大，不适合大量定时任务。
    新的timer类，优化了资源使用，只需要一个线程来驱动所有定时任务。
    所有定时任务都维护在一个PriorityQueue中，存取效率是O(logN)。

    start() 启动Timer
    shutdown() 关闭Timer，并执行所有未到期的函数

    queue里每个item是个Tuple(int, ExecInfo)
    """

    _WAIT_TIME = 10

    def __init__(self, retry_strategy=None):
        self._queue = PriorityQueue()
        self._cond = threading.Condition() # 控制_queue的并发操作
        self._stop_flag = False
        self._stopped_event = threading.Event()
        self._logger = logging.getLogger("yqg-py-scheduler.timer")
        self._retry_strategy = retry_strategy if retry_strategy else NoRetryStrategy()
        super(_Timer, self).__init__(daemon=True)

    def run(self) -> None:
        self._stopped_event.clear()

        while True:
            # extract all items to execute
            items = []
            with self._cond:
                now = time.time()
                # examine all items
                while self._queue.qsize() > 0:
                    ts, _ = self._queue.queue[0]

                    # 如果item到期或者处于shutdown过程，则可以执行
                    if ts <= now or self._stop_flag:
                        item = self._queue.get()  # remove first item
                        items.append(item)
                    else:
                        break

            # execute all items & schedule retry if necessary
            # TODO: consider using a threading pool
            for item in items:
                ts, exec_info = item
                fn = exec_info._fn
                args = exec_info._args
                kwargs = exec_info._kwargs
                try:
                    fn(*args, **kwargs)
                except:
                    self._logger.exception("Error executing timer")
                    if self._stop_flag:
                        # shutdown 过程中不重试, 尽快结束
                        self._logger.exception("skip retry because of shutdown process")
                    else:
                        next_interval = self._retry_strategy.next_interval(item)
                        if next_interval > 0:
                            self._logger.exception("reschedule timer in %s seconds" % next_interval)
                            self._queue.put((time.time() + next_interval, exec_info))
                        else:
                            self._logger.error("max retry exceeded.. ")

            # wait until next item to execute
            with self._cond:
                if self._stop_flag:
                    if self._queue.qsize() > 0:
                        # 如果在shutdown过程，则不需要sleep，尽快执行完剩下的item
                        continue
                    else:
                        # 结束主循环
                        break
                else:
                    now = time.time()
                    if self._queue.qsize() > 0:
                        ts, exec_info = self._queue.queue[0]
                        time_to_sleep = ts - now
                    else:
                        time_to_sleep = self._WAIT_TIME

                    if time_to_sleep > 0:
                        # 如果在执行fn的时候，有新的任务schedule，那time_to_sleep有可能为负
                        self._cond.wait(time_to_sleep)

        self._stopped_event.set()

    def schedule(self, interval, fn, *args, **kwargs):
        with self._cond:
            if self._stop_flag:
                self._logger.error("timer is stopped...")
                return
            else:
                now = time.time()
                exec_info = _ExecInfo(fn, args, kwargs)
                self._queue.put((now + interval, exec_info))
                self._cond.notify_all()

    def shutdown(self, timeout=None):
        with self._cond:
            self._stop_flag = True
            self._cond.notify_all()

        return self._stopped_event.wait(timeout=timeout)


class NotifierState(Enum):
    INIT = 0
    STARTED = 1
    SHUTDOWN = 2


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


class Notifier(threading.Thread):
    """
    负责发送trigger结果给remote scheduler，并在失败时安排重试
    """

    def __init__(self, scheduler):
        super(Notifier).__init__()
        self._scheduler = scheduler
        self._timer = _Timer(ExponentialRetryStrategy(max_retries=30, max_interval=120))
        self._state = NotifierState.INIT
        self._state_lock = threading.RLock()
        self._logger = logging.getLogger("yqg-py-scheduler.notifier")

    def start(self):
        with self._state_lock:
            if self._state != NotifierState.INIT:
                raise IllegalStateException(NotifierState.INIT, self._state)

            self._timer.start()
            self._state = NotifierState.STARTED

    def shutdown(self, timeout=None):
        with self._state_lock:
            if self._state != NotifierState.STARTED:
                raise IllegalStateException(NotifierState.STARTED, self._state)
            self._state = NotifierState.SHUTDOWN

        self._logger.info("shutting down notifier")
        fully_stopped = self._timer.shutdown(timeout=timeout)
        if not fully_stopped:
            raise TimeoutError("Time out while shutting down notifier.")
        self._logger.info("notifier was shut down cleanly")

    def notify(self, trigger):
        with self._state_lock:
            if self._state != NotifierState.STARTED:
                raise IllegalStateException(NotifierState.STARTED, self._state)
            self._timer.schedule(0, self._do_notify, trigger)

    def _do_notify(self, trigger):
        # 先保存原来的metadata，如果发生metadata更新，也不会读取到中间值
        md = self._scheduler.metadata()
        data = {
            "schedulerInfo": {
                "address": md.address(),
                "epoch": md.epoch(),
                "timeUpdated": md.time_updated()
            },
            "body": {
                "context": {
                    "jobId": trigger.job_id(),
                    "triggerId": trigger.id(),
                    "timeStamp": trigger.time_completed(),
                    "jobName": trigger.name(),
                    "className": ".".join([trigger.job().__module__, type(trigger.job()).__name__]),
                    "params": json.dumps(trigger.params())
                },
                "status": "SUCCESS",  # 包含状态类型有SUCCESS，FAILED，INTERRUPTED
                "msg": ""
            }
        }
        self._logger.info(json.dumps(data))

        # 给scheduler发送结果，response格式如下：
        #
        # {
        #     "status": {
        #         "code": 0,
        #         "detail": “”,
        #         "serverResponseTime": 1594102627173
        #     },
        #     "body": ""
        # }
        #
        # 如果发生网络问题，会抛出相应exception触发重试
        # 如果成功返回，但是返回code不为0，且不为17003, 17004，也抛出exception触发重试
        resp = requests.post("http://%s/internal/executeResult" % md.address(), data=data, timeout=5)
        data = resp.json()
        if data["status"]["code"] not in [0, 17003, 17004]:
            raise RuntimeError("Unexpected response returned from yqg-py-scheduler: %s" % resp)


class MockNotifier(object):

    def __init__(self):
        self._logger = logging.getLogger("yqg-py-scheduler.MockNotifier")

    def notify(self, trigger):
        self._logger.info("notify trigger..")

    def start(self):
        pass

    def shutdown(self, timeout=None):
        pass