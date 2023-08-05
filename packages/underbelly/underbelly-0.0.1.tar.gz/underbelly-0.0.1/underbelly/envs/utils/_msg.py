# Messages
from loguru import logger
from underbelly.imports import *

from underbelly.envs.utils._typing import *
from termcolor import colored


@curry
def bold_color(colour: str, msg: str):
    return colored(msg, colour, attrs=['bold'])


def rprior() -> typing.Callable:
    _col = inspect.stack()[1][3]
    return bold_color(_col)


def white(s: str):
    return rprior()(s)


def cyan(s: str):
    return rprior()(s)


def magenta(s: str):
    return rprior()(s)


def green(s: str):
    return rprior()(s)


def yellow(s: str):
    return rprior()(s)


def bool_msg(name: str, ch: bool):
    _cased = white(name.casefold())
    return {
        False: f"There are {magenta('NOT')} {_cased}.",
        True: f"There {cyan('ARE')} {_cased}."
    }[ch]


def property_msg(name: str, value: Any):
    _capped = yellow(name.casefold())
    return f"The property: {_capped} has the value: {magenta(value)}"


__all__ = ['bool_msg', 'property_msg']