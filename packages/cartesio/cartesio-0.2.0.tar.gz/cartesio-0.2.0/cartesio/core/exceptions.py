__all__ = ["CartesioException", "ParameterException", "ArrayParameterException"]


class CartesioException(Exception):
    pass


class ParameterException(CartesioException):
    pass


class ArrayParameterException(ParameterException):
    pass
