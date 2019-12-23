import datetime
import functools
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from inspect import signature

from dtb_tools.common.err import ParamsTypeErr, ReturnTypeErr

typeNone = type(None)


class LogDecoratorUnit:
    """
        最 基础的 展示log 的
    """

    def __init__(self, log_name=None, with_log: callable = None, to_log: bool = True):
        self.log_name = log_name
        self.with_log = with_log
        self.show = True if with_log is not None and to_log else False

    def show_log(self, *text):
        ls = [i.__str__() for i in text]
        if self.show:
            t = "{}:{}".format(self.log_name, "".join(ls))
            self.with_log(t)


class LogTime(LogDecoratorUnit):
    """
         这个是 方法的日志，如果打上如此的装饰器，可以添加参数 debug/Debug,即使本身并不需要
         :param log_name: log title
         :param with_log: log func
         :param to_log:  show log or not
         :return:
    """

    __slots__ = ["log_name", "with_log", "show", "log_return", "log_err"]

    def __init__(self, log_name="unknow", with_log=None, to_log: bool = True, log_return=False):
        super().__init__(log_name, with_log, to_log)
        self.log_return = log_return

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            st = datetime.datetime.now()
            self.show_log("start...")
            f = func(*args, **kwargs)
            self.show_log("end……time consuming", (datetime.datetime.now() - st).__str__())

            if self.log_return:
                self.show_log("return->", f)
            return f

        return decorator


class Deprecation(LogDecoratorUnit):
    __slots__ = ["ev"]

    def __init__(self, expected_version):
        super().__init__("deprecationWarning:", DeprecationWarning)
        self.ev = expected_version

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            self.show_log("当前方法：{}预期将在版本{}后删除，请注意".format(func.__name__, self.ev))
            f = func(*args, **kwargs)
            return f

        return decorator


class CheckParamsType:
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


class ApplicationInstance:

    def __init__(self, bind: str, with_log_success=None, with_log_err=None):
        self.bind = bind
        self.with_log_success = with_log_success
        self.with_log_err = with_log_err

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            try:
                import socket
                s = socket.socket()
                host = socket.gethostname()
                s.bind((host, self.bind))
                if self.with_log_success:
                    self.with_log_success("application instance start")
                return func(*args, **kwargs)
            except:
                self.with_log_err("start application err,can not bind {}".format(self.bind))
                sys.exit(0)

        return decorator


class RunSafe(LogDecoratorUnit):

    def __init__(self, log_name="run safe has err", with_log=None):
        super().__init__(log_name=log_name, with_log=with_log)

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            try:
                f = func(*args, **kwargs)
                return f
            except Exception as ex:
                self.show_log(ex)

        return decorator


class ErrHandler:
    """
        重写 handler 方法
    """

    def __init__(self, ex, *args, **kwargs):
        self.ex = ex
        self.args = args
        self.kwargs = kwargs

    def handler(self, ex, func, *args, **kwargs):
        raise

    def __call__(self, ex, func, *args, **kwargs):
        f = self.handler(ex, func, *args, **kwargs)
        return f


def err_handle(*handler):
    """
      对于 err  进行处理：
            是一个允许三个参数的 tuple 或者 ErrHandler 的子类,
                第一个参数是 exception
                第二个是 callable
                第三个是
    :param handler: a list with tuple;
        (Exception,an  function , like func(err);u can do something when exception,dict {err handle kwargs})
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
                    if isinstance(i, tuple):
                        err = i[0]
                        if isinstance(ex, err):
                            if len(i) == 2:
                                f = i[1](ex, func, *args, **kwargs)
                                return f
                            elif len(i) == 3:
                                f = i[1](
                                    ex, func, err_handle_kwargs=i[2], *args, **kwargs
                                )
                                return f
                            else:
                                return
                    elif isinstance(i, ErrHandler) and isinstance(ex, i.ex):
                        return i(ex, func, *args, **kwargs)

                    else:
                        continue

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


def run_background(with_log: callable = None, pool: ThreadPoolExecutor = None):
    """
        run func in background
            可以选择指定线程池进行操作
    :param with_log:
    :param pool: 线程池 ThreadPoolExecutor
    :return:
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if pool:
                pool.submit(func, *args, **kwargs)
                if with_log:
                    with_log("func {} in pool {}".format(func.__name__, pool))
            else:
                t = threading.Thread(target=func, args=args, kwargs=kwargs)
                t.start()
                if with_log:
                    with_log("func {} in thread {}".format(func.__name__, t.name))

        return wrapper

    return decorator


class Repeatedly(LogDecoratorUnit):
    """
        进行多次的尝试 ，如果 超过次数，抛出异常
    """

    def __init__(self, count=3, do_err: callable = None, do_success: callable = None, with_log: callable = None):
        super().__init__(log_name="Repeatedly", with_log=with_log)
        self.count = count
        self.do_success = do_success
        self.do_err = do_err

    def has_next(self, c):
        if self.count <= 0:
            return True
        return c < self.count

    def __call__(self, func):
        @functools.wraps(func)
        def decorator(*args, **kwargs):
            c = 0
            while self.has_next(c):
                try:
                    self.show_log("进行第{}次尝试".format(c + 1))
                    f = func(*args, **kwargs)
                    if self.do_success:
                        self.do_success()
                    return f
                except Exception as ex:
                    c += 1
                    if not self.has_next(c):
                        if self.do_err:
                            self.do_err()
                        raise ex
                    else:
                        pass

        return decorator


class RunLimitTime:
    """
        运行 func 进行时间的 限制
    """

    def __init__(self):
        pass

    def __call__(self, func):
        pass
