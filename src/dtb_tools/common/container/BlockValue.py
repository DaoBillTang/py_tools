import threading


class BlockValue:
    """
        这是一个阻塞的 写入/读取 的模型，
    """

    def __init__(self):
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.set_lock = threading.Condition(self.mutex)
        self.value = None

    def get(self):
        with self.not_empty:
            while self.value is None:
                self.not_empty.wait()
            item = self.value
            self.value = None
            return item

    def put(self, item):
        with self.set_lock:
            self.value = item
            self.not_empty.notify()
