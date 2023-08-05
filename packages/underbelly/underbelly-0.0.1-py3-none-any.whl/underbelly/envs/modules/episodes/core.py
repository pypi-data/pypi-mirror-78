from underbelly.imports import *
from underbelly.envs.modules.schemas import *

start_all(globals())


class EpisodeIdentifier(Identifier):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.episode = Field("episode", str)
        self.live = Field("live", bool)


end_all(globals())