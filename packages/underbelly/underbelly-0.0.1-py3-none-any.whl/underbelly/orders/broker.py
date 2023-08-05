from uuid import uuid4
from loguru import logger
from underbelly import EnvModule
from underbelly.background import MetricSchema, PlaceholderDB
from underbelly.orders import Trade, executor, status


class Broker(EnvModule):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dependencies = {}
        self.schema = MetricSchema()
        self.database = PlaceholderDB()
        self.executor = executor.SimulatedExecutor()

    def set_identifiers(
        self,
        userid: str,
        episode: str,
        exchange: str = "backtest",
        live: bool = False
    ):
        self.schema.set_identifiers(
            userid=userid, episode=episode, exchange=exchange, live=live
        )

    def submit(self, trade: Trade) -> status.ExecutorStatus:
        if trade.is_order():
            raise ValueError(
                "You can't submit a trade that's already been submitted."
            )
        executor_status: status.ExecutorStatus = self.executor.submit(trade)
        return executor_status

    def check(self, trade: Trade):
        if not trade.is_order():
            raise ValueError(
                "You can't submit a trade that's already been submitted."
            )

    def cancel(self):
        pass

    def orders(self):
        pass

    def openned(self):
        pass

    def synchronized(self):
        pass