from time import sleep
import numpy as np

from dtb_tools.common.decorator import RunRepeatIntervalTime, IntervalInfo

info = IntervalInfo(name="b", interval=5)


@RunRepeatIntervalTime(info)
def f1(a):
    print("---", a)


while True:
    sleep(1)
    a = np.random.randint(0, 5)
    if a <= 3:
        a = 0

    print("===", a)
    f1(a)
