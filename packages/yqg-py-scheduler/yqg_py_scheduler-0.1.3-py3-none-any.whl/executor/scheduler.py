import json
import logging
import threading
import time


class Scheduler(object):
    """
    维护remote scheduler的信息，主要是地址和epoch
    """

    def __init__(self):
        self._metadata = None
        self._logger = logging.getLogger("yqg-py-scheduler.yqg-py-scheduler")
        self._cond = threading.Condition()

    def metadata(self):
        return self._metadata

    def update_metadata(self, value, stat):
        # Design Insights:
        #
        # metadata的更新工作只给watcher做，好处是避免了并发更新的场景。
        # 假设我们允许并发更新，为了让逻辑正确，有2种方法：
        # 1. 悲观锁：先获取锁再读取zk更新本地metadata
        # 2. 乐观锁：先读取zk，更新metadata时检查版本（比如epoch）
        # 方案1不可行，因为使用的kazoo库不支持。
        # 方案2不可行，因为没法做到检查版本和更新版本是一个原子操作，
        # 除非引入锁，但那就和乐观锁的初衷相悖了，且实现也复杂
        #
        # 因此最后采用的设计就是避免了并发更新。
        with self._cond:
            if stat is None:
                self._logger.info(value)
                # stat为空说明节点被删除了，可能是master宕机了，此时不处理metadata
                # 也就是说，我们会保存旧的scheduler master信息，直到新的master选出
                # 这样设计的好处有2个：
                # 1. 调用者不用判断metadata()是否为空，逻辑简化了
                # 2. 不需要引入一个额外的字段，记录update_metadata的次数
                self._logger.info("master node is down..")
                return

            self._logger.info("Version: %s, value: %s" % (stat.version, value))
            try:
                data = json.loads(value.decode('utf-8'))
                address = data['address']
                epoch = data['epoch']
                time_updated = data['timeUpdated']
            except:
                raise ValueError("Unable to parse yqg-py-scheduler metadata %s" % value)

            self._metadata = SchedulerMetadata(address, epoch, time_updated)
            self._cond.notify_all()
            self._logger.info("metadata updated: %s" % self._metadata)

    def await_metadata(self, target_epoch, timeout=None):
        with self._cond:
            remaining_timeout = timeout
            while self._metadata.epoch() < target_epoch:
                start_time = time.time()
                self._cond.wait(remaining_timeout)
                remaining_timeout -= (time.time() - start_time)
                if remaining_timeout < 0:
                    raise TimeoutError("error waiting for yqg-py-scheduler epoch to be larger than %s" % target_epoch)


# 不是thread-safe
class SchedulerMetadata(object):

    def __init__(self, address, epoch, time_updated):
        self._address = address
        self._epoch = epoch
        self._time_updated = time_updated

    def address(self):
        return self._address

    def epoch(self):
        return self._epoch

    def time_updated(self):
        return self._time_updated

    def __str__(self):
        s = {"address": self._address, "epoch": self._epoch, "timeUpdated": self._time_updated}
        return json.dumps(s)


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