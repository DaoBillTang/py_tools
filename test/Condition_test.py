import random
from time import sleep

from dtb_tools.common.container.BlockValue import BlockValue
from dtb_tools.common.decorator import run_background

a = BlockValue(0)


@run_background()
def put():
    i = 0
    while True:
        a.put_skip(i, 5)
        print("put=={}", i)
        i += 1
        # sleep(random.randint(1, 10))
        sleep(1)


put()
a.put(1)


@run_background()
def get():
    while True:
        b = a.get()
        print("get", b)


get()
