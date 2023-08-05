from underbelly.imports import *
from underbelly.envs.utils import *
from toolz.curried import valfilter

from underbelly.envs.modules.schemas import Identifier
from underbelly.envs.modules.schemas import Field
from underbelly.envs.modules.episodes import EpisodeIdentifier
from underbelly.valid import IDependenciesAbstract


class ISchema(IDependenciesAbstract, abc.ABC):
    _dependencies: AnyDict = {
        'entity': str, 'identitier': Identifier
    }
    dependencies: dict = {}

    def __init__(
        self,
        entity: Optional[str] = None,
        depenencies: Optional[AnyDict] = None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(*args, **kwargs)

        if entity is not None: self.entity = entity
        if not is_falsy(depenencies): self.depenencies = depenencies

        self.is_watch: bool = False # determines if the data is going to a real-time log database like influxdb and redistimeseries
        self.predefined: Optional[Identifier] = None

        self.set_predefined(merge(self.__dict__, kwargs))

    def set_predefined(self, pred):
        predefined = valfilter(lambda x: isinstance(x, Field), pred)
        self.is_predefined = (not is_falsy(predefined))
        if self.is_predefined:
            self.predefined = Identifier(**predefined)

    def set_ids(self, **kwargs):
        defn = self.identitier.definition()
        is_valid, identifiable = is_match_key_dict(defn, kwargs, is_any=True)
        logger.info(bool_msg("set identifiers", is_valid))

        if is_valid:
            logger.warning(
                "Setting a current session Sending current identifiers"
            )
            logger.warning(identifiable)

    def _verify_fields(self):
        super()._verify_fields()


class MetricSchema(ISchema):
    is_predefined = False

    def __init__(
        self,
        entity: Optional[str] = None,
        depenencies: Optional[AnyDict] = None,
        *args,
        **kwargs
    ) -> None:
        super().__init__(entity, depenencies, *args, **kwargs)
        self.entity = "placeholder"
        self.identitier = EpisodeIdentifier()

    def internal_info(self) -> dict:
        pred = None
        if self.is_predefined and self.predefined is not None:
            pred = self.predefined.definition()
        return {
            "name": self.entity,
            "identity": self.identitier.definition(),
            "predefined": pred
        }

    def __initialize_internal_system(self):
        logger.debug(
            "Sending information about the schema to the lower-level system."
        )

    def _verify_fields(self):
        super()._verify_fields()
        self.__initialize_internal_system()
        # logger.debug("Checking that we have all of the schema objects.")


if __name__ == "__main__":
    with logger.catch():
        user = Field("user", str)
        exchange = Field("exchange", str)
        placeholder = MetricSchema(user=user, exchange=exchange)
        placeholder.set_ids(**{"eat": "shit"})
        placeholder.set_ids(**{
            "episode": uuid.uuid4().hex, "live": False
        })
