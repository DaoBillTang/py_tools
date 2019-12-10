import logging

from src.dtb_tools.common.decorator import (
    LogTime,
    check_params_type,
    run_safe,
    err_handle,
    with_cache,
    run_background,
)


@LogTime(with_log=logging.error, to_log=True)
@check_params_type
def test(x: int, y: str, z):
    logging.error("end")


@LogTime(with_log=logging.error, to_log=True)
@run_safe
def test_safe():
    logging.debug("test_safe")
    raise


def handler(err, *args, **kwargs):
    logging.error(err)


@LogTime(with_log=logging.error, to_log=True)
@err_handle((RuntimeError, handler), (ValueError,))
def test_err():
    logging.debug("test_safe")
    raise KeyError


cache = {}


@LogTime(with_log=logging.error, to_log=True)
@with_cache(cache, "a")
def test_cache(a):
    return a


def test_cache_2(key, data):
    """
        a = test_cache_2("a", "s")
        print(a)
        a = test_cache_2("b", "b")
        print(a)
        a = test_cache_2("a", "f")
        print(a)
        print(cache)
    :param key:
    :param data:
    :return:
    """

    @LogTime(with_log=print, to_log=True)
    @with_cache(cache, key, with_log=print)
    def test_cache_inner(a):
        return a

    return test_cache_inner(data)


def thread_test():
    import random
    from time import sleep

    @run_background(with_log=print)
    def test(a):
        i = 0
        while i != 10:
            print("{}=={}".format(a, i))
            i = random.randint(0, 10)
            sleep(1)
        print("{}->end".format(a))

    test("a")
    test("b")
    test("c")


# thread_test()


def type_handler(err, func, x, y):
    print("func type err")
    return "err"


def handler_and_params():
    @err_handle((TypeError, type_handler))
    @check_params_type
    def test(x: int, y: str):
        return "success"

    a = test(5, 6)
    print(a)


handler_and_params()
