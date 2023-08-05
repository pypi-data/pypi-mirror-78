import abc, enum, typing
import uuid
from underbelly.orders import Trade
"""Status

This file has all of the response classes. 

Everytime you call an API one of these should be retured. It's an OOP version of the the json information we get back.
"""


class ResponseCode(enum.Enum):
    SUCCESS = 200
    ERROR = 400


class Status(abc.ABC):

    def __init__(self, res_code: int = 200, data={}) -> None:
        self.response_code = ResponseCode(res_code)
        self.fit_data(data)

    def fit_data(self, data={}):
        raise NotImplementedError


class ExecutorStatus(Status):

    def __init__(self, res_code: int = 200, data={}) -> None:
        super().__init__(res_code, data)

    @property
    def orderid(self) -> str:
        return self._order_id

    def fit_data(self, data={}):
        self._order_id = uuid.uuid4().hex


class BrokerStatus(Status):

    def __init__(self, res_code: int = 200, data={}) -> None:
        super().__init__(res_code, data)
        self._trades: typing.List[Trade] = []

    @property
    def is_trades(self) -> int:
        return len(self._trades)

    def fit_data(self, data={}):
        raise NotImplementedError

    def trades(self):
        return self._trades


__all__ = ['ExecutorStatus']