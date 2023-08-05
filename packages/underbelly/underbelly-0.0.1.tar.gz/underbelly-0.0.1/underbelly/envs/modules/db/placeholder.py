# NOTE: You're spending too long on this. Come back and remove this parts later.
from redistimeseries.client import Client

from underbelly.imports import *
from underbelly.envs.models import *
from underbelly.envs.models import IPayload, LocalPayload
from underbelly.envs.modules.db import IDatabase
from underbelly.envs.utils import *


class PlaceholderDB(IDatabase):
    """Placeholder Database

    A dummy database

    Parameters
    ----------
    IDatabase : type
        Abstract database connection.
    """

    def __init__(self, conn_params: IConnection) -> None:
        super().__init__(conn_params)
        self.conn: Optional[Client] = None

    def initialize(self, info: IPayload):
        self.conn = Client(
            host=self.conn_params.host, port=self.conn_params.port
        )

        logger.debug(info.dict())

    def heartbeat(self, LocalPayload):
        logger.debug("Initializing command")

    def save(self, info: IPayload):
        if not info.is_metric:
            logger.success(info.dict())
            return
        if not info.is_values():
            return
        for k, v in info.values.items():
            key = f'{info.entity}:{k}'
            current_time = (int(info.reference_time * 100000))
            logger.warning(key)
            logger.success(current_time)
            self.conn.add(
                key=key, timestamp=current_time, value=v, labels=info.labels
            )
        # logger.debug(info.dict())

    def save_many(self, info: IPayload):
        logger.debug("Initializing command")

    def delete(self, info: IPayload):
        logger.debug("Initializing command")

    def latest(self, info: IPayload) -> dict:
        logger.debug("Initializing command")
        return dict()

    def latest_of(self, info: IPayload) -> list:
        # You get the latest of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field
        logger.debug("Initializing command")
        return []

    def latest_many(self, info: IPayload) -> list:
        # Get the latest of a single item.
        logger.debug("Initializing command")
        return []

    def latest_of_many(self, info: IPayload) -> list:
        # You get the last of multiple items.
        # E.g get the latest price for BTC, ETH, LINK will return a list of dicts for each field.
        logger.debug("Initializing command")
        return []

    def between(self, info: IPayload) -> list:
        logger.debug("Initializing command")
        return []

    def latestby(self, info: IPayload) -> dict:
        logger.debug("Initializing command")
        return {}

    def latestall(self, info: IPayload) -> list:
        logger.debug("Initializing command")
        return []

    def count(self, info: IPayload) -> int:
        logger.debug("Initializing command")
        return 0

    def deletefirst(self, info: IPayload):
        logger.debug("Initializing command")

    def get(self, info: IPayload):
        logger.debug("Initializing command")
        return dict

    def put(self, info: IPayload):
        logger.debug("Initializing command")

    def clear(self, info: IPayload):
        logger.debug("Initializing command")

    def lock(self, info: IPayload):
        logger.debug("Initializing command")
