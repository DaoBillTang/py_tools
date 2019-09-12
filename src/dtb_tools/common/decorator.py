import datetime
import functools
import sys
import threading
from inspect import signature

from dtb_tools.common.err import ParamsTypeErr, ReturnTypeErr

typeNone = type(None)


class log_time:
    """
         这个是 方法的日志，如果打上如此的装饰器，可以添加参数 debug/Debug,即使本身并不需要
         :param log_name: log title
         :param with_log: log func
         :param to_log:  show log or not
         :return:
    """
    __slots__ = ["log_name", "with_log", "show"]

    def __init__(self, log_name="unknow", with_log=None, to_log: bool = True):
        self.log_name = log_name
        self.with_log = with_log
        self.show = True if with_log is not None and to_log else False

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            if self.show:
                st = datetime.datetime.now()
                self.with_log("{}:start...".format(self.log_name))
            f = func(*args, **kwargs)
            if self.show:
                et = datetime.datetime.now()
                self.with_log("{0}:end……time consuming：{1}".format(self.log_name, et - st))
            return f

        return decorator


class deprecation:
    __slots__ = ["ev"]

    def __init__(self, expected_version):
        self.ev = expected_version

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            DeprecationWarning(
                "当前方法：{}预期将在版本{}后删除，请注意".format(func.__name__, self.ev)
            )
            f = func(*args, **kwargs)
            return f

        return decorator


class check_params_type:
    """
            装饰器：
            用于对于 进行了 函数注释的方法进行 参数类型 以及 返回值检验；
            注意：
                对于**args 和*kwargs 而言， 并没有限制 其下的 参数 的类型；
                        所以需要 限制的话，请 前移为 普通参数，或有默认值的参数
            注意：
                对于 有默认参数 None 的值，不填写 参数并不会出发判定机制；
                对于 可以为None 的值，添加type(None),或者本类里面的 typeNone  可以通过参数验证
            ：create by: dtb
            :except TypeError:
                对于 signature (参数签名) 进行 参数绑定 时， 以及参数类型 判断时 都可能返回 TypeError
        :return:
    """
    __slots__ = ["kwdict"]

    def __init__(self, kwdict=None):
        self.kwdict = kwdict

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            rules = func.__annotations__  # 获取参数与返回值的注解
            sig = signature(func)
            bound_values = sig.bind(*args, **kwargs)

            if self.kwdict is not None:
                rules.update(self.kwdict)

            for name, value in bound_values.arguments.items():
                if name in rules and not isinstance(value, rules[name]):
                    self.show_err(func.__name__, name, rules[name], type(value))

            for name, value in kwargs.items():  # 检查传入的关键字参数类型
                if name in rules and not isinstance(value, rules[name]):
                    self.show_err(func.__name__, name, rules[name], type(value))

            back = func(*args, **kwargs)

            if "return" in rules and not isinstance(back, rules["return"]):
                # 检查返回值类型
                raise ReturnTypeErr(
                    "func {}  want return %s , but %s" % (rules["return"], type(back))
                )
            return back

        return decorator

    def show_err(self, func_name, name, value, typec):
        raise ParamsTypeErr(
            "func [{}] should Argument {} must be {};but  {}".format(
                func_name, name, value, typec
            )
        )


def applicationInstance(bind: str, with_log_success=None, with_log_err=None):
    """
        通过监听特定端口,确定没有多个实例运行
    :param bind: 需要绑定监听的接口
    :param with_log_success
    :param with_log_err
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def fun(*args, **kwargs):
            import socket

            try:
                global s
                s = socket.socket()
                host = socket.gethostname()
                s.bind((host, bind))
                if with_log_success:
                    with_log_success("application instance start")
                return func(*args, **kwargs)
            except:
                with_log_err("start application err,can not bind {}".format(bind))
                sys.exit(0)

        return fun

    return decorator


def run_safe(func):
    """
        func run with safe
    :param func:
    :return:
    """

    def wrapper(*args, **kwargs):
        try:
            f = func(*args, **kwargs)
            return f
        except:
            pass

    return wrapper


def err_handle(*handler):
    """

    :param handler: a list with tuple;
        (Exception,an  function , like func(err);u can do something when exception)
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                f = func(*args, **kwargs)
                return f
            except Exception as ex:
                for i in handler:
                    if isinstance(ex, i[0]):
                        if len(i) == 2:
                            f = i[1](ex, func, *args, **kwargs)
                            return f
                        else:
                            return
                raise ex

        return wrapper

    return decorator


def with_cache(
        cache: dict,
        key,
        with_log: callable = None,
        by_get: bool = True,
        by_save: bool = True,
):
    """
        get something with cache
    :param cache: dict
    :param key:
    :param with_log : with log
    :param by_get
    :param by_save
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if by_get:
                want = cache.get(key, None)
            else:
                want = None

            if want:
                if with_log:
                    with_log("use cache data by key {}".format(key))

                return want

            f = func(*args, **kwargs)

            if by_save and f is not None:
                if with_log:
                    with_log("save cache data by key {}".format(key))
                cache[key] = f

            return f

        return wrapper

    return decorator


def run_background(with_log: callable = None):
    """
        run func in background
    :param with_thead:
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=func, args=args, kwargs=kwargs)

            if with_log:
                with_log("run func {} thread {} ".format(func.__name__, t.name))
            t.start()
            if with_log:
                with_log("end func {} in thread {}".format(func.__name__, t.name))

        return wrapper

    return decorator
