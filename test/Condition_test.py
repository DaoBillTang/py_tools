import random
import threading
from time import sleep

from src.dtb_tools.common.decorator import run_background


class BlockValue:

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


a = BlockValue()


@run_background()
def put():
    i = 0
    while True:
        a.put(i)
        print("put=={}", i)
        i += 1
        sleep(random.randint(1, 5))


put()

while True:
    b = a.get()
    print("get", b)
