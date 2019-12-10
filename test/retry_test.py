import numpy as np

from dtb_tools.common.decorator import Repeatedly


def f():
    print("f")


def s():
    print("s")


@Repeatedly(count=-1, do_success=s, do_err=f)
def f(a, b, *args, **kwargs):
    c = np.random.randint(a, high=b)

    if c > 10:
        print(c)
    else:
        raise ValueError(c)


f(4, 15)

from datetime import datetime

st = datetime.now()
et = datetime.now()

# s = "".join(["e", et - st])
# print(s)
print((et-st).__str__())
