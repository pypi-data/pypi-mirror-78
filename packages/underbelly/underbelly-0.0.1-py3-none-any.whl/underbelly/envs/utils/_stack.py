from underbelly.imports import *


def called_function():
    return inspect.currentframe().f_back.f_back.f_code.co_name


__all__ = ['called_function']