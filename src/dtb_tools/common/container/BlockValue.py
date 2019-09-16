import threading
from time import monotonic

from dtb_tools.common.err import TimeOutErr


class BlockValue:
    """
        这是一个阻塞的 写入/读取 的模型，
    """

    def __init__(self, init_value=None):
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.set_lock = threading.Condition(self.mutex)
        self.value = init_value
        self.num = 0

    def get(self, timeout=None):
        with self.not_empty:
            if timeout is None:
                while self.value is None:
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = monotonic() + timeout
                while self.value is None:
                    remaining = endtime - monotonic()
                    if remaining <= 0.0:
                        raise TimeOutErr("time out")
                    self.not_empty.wait(remaining)
            item = self.value
            self.value = None
            self.num = 0
            return item

    def put_skip(self, item, skip):
        """
            通过计数器，满足条件才添加数据
        :param skip:
        :return:
        """
        with self.set_lock:
            self.num += 1
            if self.num >= skip:
                self.value = item
                self.not_empty.notify()

    def put(self, item):
        with self.set_lock:
            self.value = item
            self.not_empty.notify()
