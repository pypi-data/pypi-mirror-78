from uuid import uuid4
from loguru import logger
from underbelly import EnvModule
from underbelly.envs import MetricSchema, PlaceholderDB
from underbelly.orders import Trade, status


class Executor(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = MetricSchema()
        self.database = PlaceholderDB()

    def submit(self, trade: Trade):
        raise NotImplementedError


class SimulatedExecutor(Executor):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = MetricSchema()
        self.database = PlaceholderDB()

    def submit(self, trade: Trade):
        return status.ExecutorStatus()