from src.dtb_tools.common.decorator import check_params_type, deprecation, err_handle
from src.dtb_tools.common.err import ParamsTypeErr


def handler(ex, func, a, *args, **kwargs):
    print(a)


@err_handle((TypeError,handler))
@check_params_type({"c": str})
def test_check_params_type(a: int, b: str, **kwargs):
    print(a, b)


@deprecation("3rd")
def tt(a: int):
    print("ss")


try:
    test_check_params_type("a", 5)
except ParamsTypeErr:
    print("pa")
except TypeError:
    print("type")
