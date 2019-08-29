import logging

from src.dtb_tools.common.decorator import log_time, check_params_type, run_safe, err_handle


@log_time(with_log=logging.error, to_log=True)
@check_params_type
def test(x: int, y: str, z):
    logging.error("end")


@log_time(with_log=logging.error, to_log=True)
@run_safe
def test_safe():
    logging.debug("test_safe")
    raise


def handler(err, *args, **kwargs):
    logging.error(err)


@log_time(with_log=logging.error, to_log=True)
@err_handle((RuntimeError, handler), (ValueError,))
def test_err():
    logging.debug("test_safe")
    raise KeyError


test_err()
