import logging
import sys
import threading
import time
import timeit

from kazoo.protocol.states import KazooState
from kazoo.recipe.watchers import DataWatch


class OldSchedulerEpochException(RuntimeError):

    def __init__(self, local_epoch, remote_epoch):
        self._local_epoch = local_epoch
        self._remote_epoch = remote_epoch

    def __str__(self):
        return "local epoch %s > remote_epoch %s" % (self._local_epoch, self._remote_epoch)


class ExecutorApplication(object):
    """
    整合了zk, executor, zookeeper, yqg-py-scheduler, notifier
    """

    def __init__(self, id, zk, executor, scheduler, notifier):
        self._id = id
        self._zk = zk
        self._zk_suspended_timer = None
        self._executor = executor
        self._scheduler = scheduler
        self._notifier = notifier
        self._logger = logging.getLogger("yqg-py-scheduler.app")

    def start(self):

        # 监听zk connection状态
        self._zk.add_listener(self._zk_connection_listener)

        # 连接zk
        self._zk.start(timeout=30)

        # register executor node
        # 如果节点存在，zk.create()会抛异常NodeExistsError，
        # 比如executor在lease过期之前快速重启，就可能会有这种情况，
        # 此时等待lease过期节点消失再重启即可。
        self._zk.create("/dist_scheduler/executor/%s" % self._id, ephemeral=True, makepath=True)

        # watch yqg-py-scheduler master node
        DataWatch(self._zk, "/dist_scheduler/scheduler/master", self._on_scheduler_master_change)

        # start notifier
        self._notifier.start()

    def _zk_connection_listener(self, state):
        # Design Insights:
        #
        # zk connection的状态迁移有如下几种：
        # LOST -> CONNECTED: 新连接或者连接LOST后又重连上
        # CONNECTED -> SUSPENDED: 连接有问题，但有可能恢复
        # CONNECTED -> LOST: 目前只可能是因为auth证书有问题
        # SUSPENDED -> LOST: 重新连上zk后发现session timeout
        # SUSPENDED -> CONNECTED: 重新连上zk后，session也没timeout
        #
        # executor的理想处理方案如下：
        # LOST -> CONNECTED: pass
        # CONNECTED -> SUSPENDED: pause all jobs
        # CONNECTED -> LOST: sys.exit
        # SUSPENDED -> LOST: cancel all paused jobs
        # SUSPENDED -> CONNECTED: resume all paused jobs
        #
        # 但是这个方案没法实现，因为目前阶段job无法支持pause/resume/cancel等操作。
        #
        # 因此，目前采取的是一个简单粗暴的处理方案：
        # LOST -> CONNECTED: pass
        # CONNECTED -> SUSPENDED: start timer
        # CONNECTED -> LOST: sys.exit
        # SUSPENDED -> LOST: clear timer & sys.exit
        # SUSPENDED -> CONNECTED: clear timer
        #
        # 需要timer是为了应对network partition的情况。由于kazoo没有实现本地的session timeout。
        # 如果发生network partition, 在重新连接上zookeeper之前，connection将一直处于suspended状态。
        # 因此设计了一个timer，如果超过given time，还未恢复连接，则直接sys.exit
        #
        # 在实现过程中，又有点不同。因为Kazoo库的connectionListener只会传current state，不会传递prev state，
        # 所以prev state只能靠自己记录或者用其他的等价条件判断（比如是否有zk_suspended_timer)
        if state == KazooState.CONNECTED:
            # 如果有timer，则说明之前的状态是SUSPENDED。否则是LOST
            if self._zk_suspended_timer is None:
                self._logger.info("zk connection state: LOST -> CONNECTED")
                pass
            else:
                self._logger.info("zk connection state: SUSPENDED -> CONNECTED")
                self._zk_suspended_timer.cancel()
                self._zk_suspended_timer = None
        elif state == KazooState.SUSPENDED:
            self._logger.info("zk connection state: CONNECTED -> SUSPENDED")

            def exit_on_long_suspend():
                self._logger.error("zk connection is suspended too long. exit now..")
                sys.exit(1)

            self._zk_suspended_timer = threading.Timer(120, exit_on_long_suspend)
            self._zk_suspended_timer.start()
        elif state == KazooState.LOST:
            # 如果有timer，则说明之前的状态是SUSPENDED。否则是CONNECTED
            if self._zk_suspended_timer is None:
                self._logger.info("zk connection state: CONNECTED -> LOST")
            else:
                self._logger.info("zk connection state: SUSPENDED -> LOST")
                self._zk_suspended_timer.cancel()
                self._zk_suspended_timer = None
            sys.exit(1)
        else:
            raise RuntimeError("unknown zk connection state  %s" % state)

    def _on_scheduler_master_change(self, value, stat):
        self._scheduler.update_metadata(value, stat)

    def _ensure_valid_epoch(self, remote_epoch):
        local_epoch = self._scheduler.metadata().epoch()
        if local_epoch > remote_epoch:
            raise OldSchedulerEpochException(local_epoch, remote_epoch)
        elif local_epoch < remote_epoch:
            self._scheduler.await_metadata(remote_epoch, timeout=60)

    def _time_it(self, fn, error_msg = None):
        start_time = time.time()
        try:
            fn()
        except:
            self._logger.exception(error_msg)
        finally:
            return time.time() - start_time

    def shutdown(self, timeout):
        hooks = [
            (lambda t : self._zk.stop(), "stop zk client"),
            (lambda t : self._executor.shutdown(timeout=t), "shutdown executor"),
            (lambda t : self._notifier.shutdown(timeout=t), "shutdown notifier")
        ]

        time_remaining = timeout
        for hook in hooks:
            start_time = time.time()
            try:
                hook[0](time_remaining)
            except TimeoutError:
                self._logger.exception("app shutdown times out while %s" % hook[1])
                break
            except Exception:
                self._logger.exception("error while %" % hook[1])
            finally:
                time_remaining = time_remaining - (time.time() - start_time)

    def trigger(self, remote_epoch, trigger_id, job_id, name, class_name, params=None):
        self._ensure_valid_epoch(remote_epoch)
        return self._executor.trigger(trigger_id, job_id, name, class_name, params, self._on_trigger_complete)

    def _on_trigger_complete(self, trigger):
        self._notifier.notify(trigger)

    def interrupt(self, remote_epoch, trigger_id):
        self._ensure_valid_epoch(remote_epoch)
        self._executor.interrupt(trigger_id)

    def list_triggers(self, remote_epoch, trigger_id=None):
        self._ensure_valid_epoch(remote_epoch)
        return self._executor.triggers(tid=trigger_id)