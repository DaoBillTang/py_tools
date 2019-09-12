class DtbErr(Exception):
    pass


class ParamsTypeErr(DtbErr, TypeError):
    pass


class ReturnTypeErr(DtbErr, TypeError, RuntimeError):
    pass
