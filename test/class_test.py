from src.dtb_tools.common.decorator import (
    check_params_type,
    Deprecation,
    err_handle,
    ErrHandler,
)
from src.dtb_tools.common.err import ParamsTypeErr


def handler(ex, func, a, *args, **kwargs):
    print(a)
    print(kwargs)


class h1(ErrHandler):
    def handler(self, ex, func, *args, **kwargs):
        print(self.args)
        print(self.kwargs)
        print(ex)


@err_handle((TypeError, handler, {"tuple": "tup"}), h1(TypeError, type="type"))
@check_params_type({"c": str})
def test_check_params_type(a: int, b: str, **kwargs):
    print(a, b)


@Deprecation("3rd")
def tt(a: int):
    print("ss")


try:
    test_check_params_type("a", 5)
except ParamsTypeErr:
    print("pa")
except TypeError:
    print("type")
