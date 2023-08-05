from underbelly.envs.modules.episodes import EpisodeIdentifier
from underbelly.envs.modules.schemas import *
from underbelly.envs.utils import *
from underbelly.imports import *

start_all(globals())


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
        self.entity = "metrics"
        self.identitier = EpisodeIdentifier()
        self.is_watch = True

    def internal_info(self) -> dict:
        pred = None
        if self.predefined is not None:
            pred = self.predefined.definition()
        return {
            "name": self.entity,
            "identity": self.identitier.definition(),
            "predefined": pred,
            'is_watched': self.is_watch
        }

    def __initialize_internal_system(self):
        logger.debug(
            "Sending information about the schema to the lower-level system."
        )

    def _verify_fields(self):
        super()._verify_fields()
        self.__initialize_internal_system()
        # logger.debug("Checking that we have all of the schema objects.")


end_all(globals())

if __name__ == "__main__":
    MetricSchema()