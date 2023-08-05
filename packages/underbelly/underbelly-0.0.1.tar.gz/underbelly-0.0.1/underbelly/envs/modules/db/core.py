from underbelly.envs.utils import *
from underbelly.imports import *
from underbelly.envs.models import IPayload, IConnection, LocalPayload

start_all(globals())


class IDatabase(abc.ABC):
    """Database Abstract

    Will use to hold general functions and functionality for the updateself.
    
    
    It will also have better features as time progresses. All to speed up the system.
    """

    def __init__(self, conn_params: IConnection) -> None:
        self.conn_params = conn_params

    def initialize(self, info: IPayload):
        # Send connction information to lower layer
        raise NotImplementedError

    def heartbeat(self, LocalPayload):
        raise NotImplementedError

    def save(self, info: IPayload):
        raise NotImplementedError

    def save_many(self, info: IPayload):
        raise NotImplementedError

    def delete(self, info: IPayload):
        raise NotImplementedError

    def latest(self, info: IPayload) -> dict:
        raise NotImplementedError

    def latestmany(self, info: IPayload):
        raise NotImplementedError

    def between(self, info: IPayload) -> list:
        raise NotImplementedError

    def latestby(self, info: IPayload) -> dict:
        raise NotImplementedError

    def latestall(self, info: IPayload):
        raise NotImplementedError

    def count(self, info: IPayload) -> int:
        raise NotImplementedError

    def deletefirst(self, info: IPayload):
        raise NotImplementedError

    def get(self, info: IPayload):
        raise NotImplementedError

    def put(self, info: IPayload):
        raise NotImplementedError

    def clear(self, info: IPayload):
        raise NotImplementedError

    def lock(self, info: IPayload):
        raise NotImplementedError


end_all(globals())

__all__ = ['IDatabase']