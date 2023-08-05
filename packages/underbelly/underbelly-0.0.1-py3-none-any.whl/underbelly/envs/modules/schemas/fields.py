from underbelly.imports import *
from underbelly.envs.utils import (
    flatten_dict,
    const_hash,
    AnyDict,
)


class Field:
    supported_types = [str, int, float, bool, dict, list, np.dtype]

    def __init__(self, name: str, _type: type, rules: AnyDict = {}) -> None:
        if _type not in self.supported_types:
            raise ValueError(f"{name} cannot be type: {_type}")
        self.name = name
        self.field_type = _type
        self._rules: AnyDict = rules

    def definition(self) -> AnyDict:
        return {
            "field_type": self.field_type,
            "rules": self._rules,
        }

    def flattened_rules(self) -> dict:
        return flatten_dict(self._rules)

    def __str__(self) -> str:
        return f"{self.name}:{self.field_type}:{self.flattened_rules()}"

    def hashed(self):
        return const_hash(str(self))


def field_reduce(f1: Field, f2: Field):
    return const_hash(f"{f1.hashed()}{f2.hashed()}")


def field_def_map(f1: Field):
    return {
        str(f1.name): f1.definition()
    }


def field_def_reduce(f1: dict, f2: dict):
    return toolz.dicttoolz.merge(f1, f2)


__all__ = [
    'Field',
    'field_reduce',
    'field_def_map',
    'field_def_reduce',
]
