import decimal
from typing import Tuple

from toolz.curried import do
from underbelly.imports import *
from toolz import curry
from toolz import dicttoolz
from underbelly.envs.utils._msg import *
from underbelly.envs.utils._typing import *
from underbelly.envs.utils._toolz import *

ATTRS = ['__add__', '__sub__', '__mul__', '__truediv__', '__pow__']


def flatten_dict(dd: AnyDict, separator='_', prefix=''):
    return {
        prefix + separator + k if prefix else k: v for kk,
        vv in dd.items() for k,
        v in flatten_dict(vv, separator, kk).items()
    } if isinstance(dd, dict) else {
        prefix: dd
    }


def is_falsy(item: Any) -> bool:
    return (not bool(item))


def is_numeric(obj):
    return all(hasattr(obj, attr) for attr in ATTRS)


def num_check(
    obj: typing.Union[int, float, decimal.Decimal, np.number]
) -> bool:
    return all(hasattr(obj, attr) for attr in ATTRS)


@curry
def cinstance(_type: typing.Type, item) -> bool:
    k, v = item
    if not isinstance(k, str): return False
    if _type in [int, float, decimal.Decimal, np.ndarray]: return num_check(v)
    return isinstance(v, _type)


@curry
def failing_filter(failed_list: list, success_list: list, item: Tuple) -> bool:
    v1, v2, v3 = item
    action = {
        False: failed_list.append, True: success_list.append
    }
    action[v1]({
        v2: v3
    })

    return v1


def extract_instance(
    _dict: AnyDict, _instance_type: typing.Type
) -> typing.Tuple[AnyDict, bool]:
    """Extracts Instance

    Extracts the given declared instance from the dictionary given. Returns a boolean if we've found something.

    Parameters
    ----------
    _dict : AnyDict
        The dictionary we're extracting values from.
    _instance_type : typing.Type
        The instance type we're checking.

    Returns
    -------
    typing.Tuple[AnyDict, bool]
        A tuple with the dictionary and a variable indicating that there are variables.
    """
    items: AnyDict = {}
    is_items = False
    if is_falsy(_dict):
        return items, is_items
    current_type = cinstance(_instance_type)
    items = dicttoolz.itemfilter(current_type, _dict)
    return items, (not is_falsy(items))


def const_hash(s: str) -> str:
    m = md5()
    m.update(s.encode('utf-8'))
    return m.hexdigest()


def get_type(value: Any) -> type:
    if isinstance(value, type):
        return value
    return type(value)


@curry
def is_item(reference: dict, item: Tuple):
    """Is item

    Checks to see if the item is inside of the dictionary. To be used with filterself.

    Parameters
    ----------
    reference : dict
        The dictionary we're trying to compare it to. Checking the instance on top of everything else
    item : Tuple
        The item inside of the itemfilter.

    Returns
    -------
    bool
        True if the item and instance type is within the reference dictionary.
    """

    k, v = item
    _ref = reference
    if k not in _ref: return False, k, None

    current_type = get_type(_ref[k])
    if not isinstance(v, current_type): False, k, current_type
    return True, k, current_type


@curry
def is_item_key(reference: dict, item: Tuple):
    """Is item

    Checks to see if the item is inside of the dictionary. To be used with filterself.

    Parameters
    ----------
    reference : dict
        The dictionary we're trying to compare it to. Checking the instance on top of everything else
    item : Tuple
        The item inside of the itemfilter.

    Returns
    -------
    bool
        True if the item and instance type is within the reference dictionary.
    """

    k, v = item
    _ref = reference
    if not k in _ref: return False, k, None

    current_type = get_type(_ref[k])
    if not isinstance(v, current_type): False, k, current_type
    return True, k, current_type


def is_match_dict(reference: AnyDict,
                    _checking: AnyDict) -> Tuple[bool, AnyList, AnyList]:
    """Is Match Dict

    Checks to see if the dictionaries match. Checks the instance types too.

    Args:
        _checking (AnyDict): The dictionary we're checking.
        reference (AnyDict): The reference dictionary.

    Returns:
        bool: True if both the keys and instance types match.
    """

    if is_falsy(_checking) or is_falsy(reference):
        logger.error("Nothing in one of the dictionary. Can't compare.")
        return False, list(reference.keys()), []

    _is_item = is_item(_checking)
    missing: list = []
    successful: list = []

    reporting = failing_filter(missing, successful)

    def bpipe(x: dict):
        return pipe(x.items(), map(_is_item), map(reporting), list, all_equal)

    _ch = bpipe(reference)

    return _ch, missing, successful


def is_match_list_dict(reference: AnyList,
                        d: AnyDict,
                        is_any: bool = False) -> Tuple[bool, dict]:
    if is_falsy(d) or is_falsy(reference):
        return False, {}
    is_valid = False
    if is_any:
        is_valid = any(x in d for x in reference)
    else:
        is_valid = all(x in d for x in reference)
    if not is_valid:
        return False, {}
    return True, keyfilter(lambda y: y in reference, d)


def is_match_key_dict(reference: AnyDict,
                        d: AnyDict,
                        is_any: bool = False) -> Tuple[bool, dict]:
    keys = list(reference.keys())
    return is_match_list_dict(keys, d, is_any=is_any)


__all__ = [
    'flatten_dict',
    'extract_instance',
    'num_check',
    'is_falsy',
    'const_hash',
    'is_match_dict',
    'is_match_key_dict',
    'is_match_list_dict'
]

if __name__ == "__main__":
    e1 = {
        "shit": "dick", "poop": 2, "green": "blue", "red": "period"
    }
    e2 = {
        "shit": "dick", "poop": 2, "green": "blue"
    }
    logger.warning(is_match_dict(e1, e2))
    extracted, is_extracted = extract_instance(e1, float)
    logger.info(bool_msg("Extracted Instances", is_extracted))
    logger.info(extracted)
