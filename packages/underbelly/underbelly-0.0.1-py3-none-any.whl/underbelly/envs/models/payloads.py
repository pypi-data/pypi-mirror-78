from enum import Enum
from underbelly.imports import *
from underbelly.envs.utils import *
from auto_all import start_all, end_all
from pydantic import Field

start_all(globals())


class CommandTypes(Enum):
    CREATE = 1
    READ = 2
    UPDATE = 3
    DELETE = 4
    LOCAL = 5
    RECORD = 6


class ConnectionTypes(Enum):
    REDIS = 1
    QUERYENGINE = 2


class IConnection(base_model, abc.ABC):
    conn_type: ConnectionTypes = ConnectionTypes.REDIS
    host: str = "localhost"
    port: int = 6379


class BasePayload(base_model, abc.ABC):
    entity: str
    is_metric: bool = False
    command_type: CommandTypes = CommandTypes.CREATE


class LocalPayload(BasePayload):
    # A payload to ask the local system what's locally there.
    command_type = CommandTypes.LOCAL
    identity_id: str
    question: dict


class IPayload(BasePayload):
    command_type = CommandTypes.CREATE
    labels: AnyDict
    record_time: float = Field(default_factory=time.time)
    reference_time: float = Field(default_factory=time.time)
    values: Optional[AnyDict] = {}

    def is_values(self):
        return bool(self.values)


class MetricItem(base_model):
    key: str
    time: int
    value: float


class MetricsPayload(IPayload):
    command_type = CommandTypes.RECORD
    is_metric: bool = True

    def get_metric_items(self):
        if not self.is_values(): raise ValueError("You need to have something")
        for k, v in self.values.items():
            timestamp = (self.reference_time * 1000)
            yield MetricItem(key=f"{self.entity}:{k}", value=v, time=timestamp)


end_all(globals())
