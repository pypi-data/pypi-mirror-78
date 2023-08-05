import functools
from itertools import starmap
import itertools, copy
from typing import Callable, Iterable
from loguru import logger
from toolz import compose
from toolz.curried import diff, filter, join, groupby, keyfilter, map, merge, reduceby, pipe, sliding_window
from toolz.functoolz import curry

from underbelly.envs.utils._typing import *


def pick(whitelist, d):
    return keyfilter(lambda k: k in whitelist, d)


def omit(blacklist, d):
    return keyfilter(lambda k: k not in blacklist, d)


def compact(iter):
    return filter(None, iter)


def keyjoin(leftkey, leftseq, rightkey, rightseq):
    return starmap(merge, join(leftkey, leftseq, rightkey, rightseq))


def areidentical(*seqs):
    return not any(diff(*seqs, default=object()))


def split_apply_combine(split_op, apply_op, *seqs):
    return reduceby(split_op, apply_op, seqs, 0)


def select_by(map_func: Callable, filter_func: Callable, *seqs):
    return pipe(seqs, filter(filter_func), map(map_func), list)


def sliding_op(map_func: Callable, size: int = 2, iter: Iterable = []):
    return pipe(iter, sliding_window(size), map(map_func))


@curry
def all_equal(iterable):
    "Returns True if all the elements are equal to each other"
    g = itertools.groupby(iterable)
    return next(g, True) and not next(g, False)


def add_definition(obj: type, items: Tuple):
    k, v = items
    obj.__dict__[k] = copy.deepcopy(v)


def remove_definition(obj: type, k: str):
    del obj.__dict__[k]


add_definition = curry(add_definition)
remove_definition = curry(remove_definition)

__all__ = [
    'pick',
    'omit',
    'compact',
    'keyjoin',
    'groupby',
    'compose',
    'areidentical',
    'split_apply_combine',
    'select_by',
    'all_equal',
    'add_definition',
    'remove_definition'
]