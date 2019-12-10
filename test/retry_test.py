import numpy as np

from dtb_tools.common.decorator import Repeatedly


def f():
    print("f")


def s():
    print("s")


@Repeatedly(count=-1, do_success=s, do_err=f, with_log=print)
def f(a, b, *args, **kwargs):
    c = np.random.randint(a, high=b)

    if c > 10:
        print(c)
    else:
        raise ValueError(c)


f(1, 12)
