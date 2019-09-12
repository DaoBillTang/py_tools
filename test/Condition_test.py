import random
import threading
from time import monotonic
from time import sleep

from dtb_tools.common.decorator import run_background


class BlockValue:

    def __init__(self):
        self.mutex = threading.Lock()
        self.not_empty = threading.Condition(self.mutex)
        self.set_lock = threading.Condition(self.mutex)
        self.value = None

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
                        raise RuntimeError("time out")
                    self.not_empty.wait(remaining)
            item = self.value
            self.value = None
            return item

    def put(self, item):
        with self.set_lock:
            self.value = item
            self.not_empty.notify()


a = BlockValue()


@run_background()
def put():
    i = 0
    while True:
        a.put(i)
        print("put=={}", i)
        i += 1
        sleep(random.randint(1, 10))


# put()
a.put(1)
while True:
    b = a.get(timeout=10)
    print("get", b)
