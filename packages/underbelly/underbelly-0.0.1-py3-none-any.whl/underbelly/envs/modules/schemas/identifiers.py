import copy
from underbelly.imports import *
from underbelly.envs.modules.schemas.fields import *
from underbelly.envs.utils import (
    extract_instance,
    add_definition,
    remove_definition,
    AnyDict,
)
from toolz.curried import reduce, pipe


class Identifier(metaclass=VerificationType):
    __kwfields: dict = {}
    __iskwfields: bool = False

    __initfields: dict = {}
    __isinitfields: bool = False

    __merged_fields: dict = {}
    __field_key: str = ""
    __field_definitions: AnyDict = {}

    def __init__(self, **kwargs) -> None:

        self.__kwfields, self.__iskwfields = self.__extract_fields(kwargs)

    @property
    def field_key(self) -> str:
        return self.__field_key

    def definition(self) -> AnyDict:
        return self.__field_definitions

    def __extract_fields(self, items: AnyDict):
        return extract_instance(items, Field)

    def __merge_fields(self):
        if not self.__iskwfields and not self.__isinitfields:
            raise AttributeError(
                "You didn't add any fields. You need to add at least 1."
            )
        while True:
            if not self.__isinitfields:
                self.__merged_fields = self.__kwfields
                break
            if not self.__iskwfields:
                self.__merged_fields = self.__initfields
                break
            self.__merged_fields = toolz.dicttoolz.merge(
                self.__initfields, self.__kwfields
            )
            break
        logger.success("Successfully merged")

        self.__merged_fields = collections.OrderedDict(
            sorted(self.__merged_fields.items())
        )
        _add_definition = add_definition(self)
        map(_add_definition, self.__merged_fields)

    def __extract_init(self):
        rdef = remove_definition(self)
        self.__initfields, self.__isinitfields = self.__extract_fields(self.__dict__)
        # remove_definition = remove_definition(self)
        keymap(rdef, self.__initfields)

    def __create_field_key(self):
        logger.info(self.__merged_fields)
        mv = self.__merged_fields.values()
        __idkey = reduce(field_reduce, mv)
        __field_map = pipe(
            mv,
            map(field_def_map),
            reduce(field_def_reduce),
        )

        self.__field_key = __idkey
        self.__field_definitions = __field_map

    def __clear_fields(self):
        del self.__kwfields
        del self.__iskwfields
        del self.__initfields
        del self.__isinitfields

    def _verify_fields(self):
        self.__extract_init()
        self.__merge_fields()
        self.__create_field_key()
        self.__clear_fields()


class EpisodeIdentifier(Identifier):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.episode = Field("episode", str)
        self.live = Field("live", bool)


if __name__ == "__main__":
    episode = Field("episode", str)
    live = Field("live", bool)
    identifier = EpisodeIdentifier()
    logger.info(identifier.field_key)