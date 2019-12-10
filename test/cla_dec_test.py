import datetime
import functools
import timeit

from src.dtb_tools.common.decorator import LogTime
import numpy as np


class d:
    def __init__(self, func):
        self.f = func

    def __call__(self, *args, **kwargs):
        # print(self.n)
        print(args)
        print(kwargs)

        return self.f(*args, **kwargs)


class c_d:
    def __init__(self, log_name="unknow", with_log=None, to_log: bool = False):
        self.log_name = log_name
        self.with_log = with_log

        self.show = True if with_log is not None and to_log else False

    def __call__(self, func):
        """
        这个是 方法的日志，如果打上如此的装饰器，可以添加参数 debug/Debug,即使本身并不需要
        :param log_name: log title
        :param with_log: log func
        :param to_log:  show log or not
        :return:
        """

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if self.show:
                st = datetime.datetime.now()
                self.with_log("{}:start...".format(self.log_name))
            f = func(*args, **kwargs)
            if self.show:
                et = datetime.datetime.now()
                self.with_log(
                    "{0}:end……time consuming：{1}".format(self.log_name, et - st)
                )
            return f

        return decorator


class c_d_2:
    __slots__ = ["log_name", "with_log", "show"]

    def __init__(self, log_name="unknow", with_log=None, to_log: bool = False):
        self.log_name = log_name
        self.with_log = with_log

        self.show = True if with_log is not None and to_log else False

    def __call__(self, func):
        """
        这个是 方法的日志，如果打上如此的装饰器，可以添加参数 debug/Debug,即使本身并不需要
        :param log_name: log title
        :param with_log: log func
        :param to_log:  show log or not
        :return:
        """

        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if self.show:
                st = datetime.datetime.now()
                self.with_log("{}:start...".format(self.log_name))
            f = func(*args, **kwargs)
            if self.show:
                et = datetime.datetime.now()
                self.with_log(
                    "{0}:end……time consuming：{1}".format(self.log_name, et - st)
                )
            return f

        return decorator


@c_d(with_log=print, to_log=True)
def test_(a, b):
    print(a, b)


@LogTime(with_log=print, to_log=True)
def test_2(a, b):
    print(a, b)


@c_d_2(with_log=print, to_log=True)
def test_3(a, b):
    print(a, b)


t1 = timeit.Timer("test_(5,6)", "from cla_dec_test import test_")
t2 = timeit.Timer("test_2(5,6)", "from cla_dec_test import test_2")
t3 = timeit.Timer("test_3(5,6)", "from cla_dec_test import test_3")


def p(t):
    s = t.repeat(10, 10000)
    print(s)
    print(np.mean(s))


"""
repeat 5 : 
0.23945409240004664
0.2581265689999782
0.22191880059999675
repeat 10
0.22386971110008744
0.2552294083000106
0.2158995718000824
"""

p(t3)
