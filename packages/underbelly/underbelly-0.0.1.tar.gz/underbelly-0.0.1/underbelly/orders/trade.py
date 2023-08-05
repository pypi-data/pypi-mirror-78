import uuid
from typing import Optional

from loguru import logger
from underbelly.orders import TradeType
from underbelly.orders.utils import split


class TradeCaster(object):
    requirements = ["symbol", "trade_type", "amount", "price"]
    cast_vars = {
        "limit_buy": TradeType.LIMIT_BUY,
        "limit_sell": TradeType.LIMIT_SELL,
        "market_sell": TradeType.MARKET_SELL,
        "market_buy": TradeType.MARKET_BUY,
    }

    def extract_trade_type(self, trade_type):
        return self.cast_vars.get(trade_type, TradeType.HOLD)

    def cast(self, **kwargs):
        is_valid = all(x in kwargs for x in self.requirements)
        if not is_valid:
            raise AttributeError(
                f"For the cast to be valid you need {self.requirements}"
            )
        _trade_type = kwargs.get("trade_type")
        symbol = kwargs.get("symbol", "BTC_USD")
        trade_type = self.extract_trade_type(_trade_type)
        amount = kwargs.get("amount", 0.0)
        price = kwargs.get("price", 0.0)

        trade = Trade(
            symbol=symbol, trade_type=trade_type, amount=amount, price=price
        )


class Trade(object):
    """A trade object for use within trading environments."""

    def __init__(
        self, symbol: str, trade_type: 'TradeType', amount: float, price: float
    ):
        """
        Arguments:
            symbol: The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc).
            trade_type: The type of trade executed (0 = HOLD, 1=LIMIT_BUY, 2=MARKET_BUY, 3=LIMIT_SELL, 4=MARKET_SELL).
            amount: The amount of the instrument in the trade (shares, satoshis, contracts, etc).
            price: The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD").
            exchange: The exchange we're adding the trade into.
            commission: 
        """
        self._base: Optional[str] = None
        self._quote: Optional[str] = None
        self._symbol = symbol
        self._trade_type = trade_type
        self._amount = amount
        self._price = price

        # Use these variables to
        self._exchange: Optional[str] = None
        self._episode: Optional[str] = None
        self._commission: Optional[str] = None
        self._userid: Optional[str] = None
        self._islive: bool = False
        self._order_id: Optional[str] = None
        self._slippage: float = 0.0
        self.split_trade()

    def copy(self) -> 'Trade':
        """Return a copy of the current trade object."""
        return Trade(
            symbol=self._symbol,
            trade_type=self._trade_type,
            amount=self._amount,
            price=self._price
        )

    @property
    def symbol(self) -> str:
        """The exchange symbol of the instrument in the trade (AAPL, ETH/USD, NQ1!, etc)."""
        return self._symbol

    @symbol.setter
    def symbol(self, symbol: str):
        self._symbol = symbol

    @property
    def trade_type(self) -> 'TradeType':
        """The type of trade ("buy", "sell", "hold", etc)."""
        return self._trade_type

    @trade_type.setter
    def trade_type(self, trade_type: 'TradeType'):
        self._trade_type = trade_type

    @property
    def amount(self) -> float:
        """The amount of the instrument in the trade (shares, satoshis, contracts, etc)."""
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        self._amount = amount

    @property
    def price(self) -> float:
        """The price paid per instrument in terms of the base instrument (e.g. 10000 represents $10,000.00 if the `base_instrument` is "USD")."""
        return float(self._price)

    @price.setter
    def price(self, price: float):
        self._price = price

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, _base: str):
        self._base = _base

    @property
    def quote(self):
        return self._quote

    @quote.setter
    def quote(self, _quote: str):
        self._quote = _quote

    @property
    def is_hold(self) -> bool:
        """
        Returns:
            Whether the trade type is non-existent (i.e. hold).
        """
        return self._trade_type.is_hold

    @property
    def is_buy(self) -> bool:
        """
        Returns:
            Whether the trade type is a buy offer.
        """
        return self._trade_type.is_buy

    @property
    def is_sell(self) -> bool:
        """
        Returns:
            Whether the trade type is a sell offer.
        """
        return self._trade_type.is_sell

    @property
    def exchange(self):
        if self._exchange is None:
            raise AttributeError("Exchange hasn't been set")
        return self._exchange

    @exchange.setter
    def exchange(self, _exchange: str):
        self._exchange = _exchange

    @property
    def episode(self):
        if self._episode is None:
            raise AttributeError("Episode hasn't been set")
        return self._episode

    @episode.setter
    def episode(self, _episode: str):
        self._episode = _episode

    @property
    def userid(self):
        if self._userid is None:
            raise AttributeError("User id not set")
        return self._userid

    @userid.setter
    def userid(self, user_id):
        self._userid = user_id

    @property
    def live(self) -> bool:
        return self._islive

    @live.setter
    def live(self, _live: bool):
        self._live = _live

    @property
    def orderid(self):
        return self._order_id

    @orderid.setter
    def orderid(self, _order_id: str):
        self._order_id = _order_id

    def is_pair(self):
        return self.base is not None and self.quote is not None

    def split_trade(self):
        pair = split(['_', '/', ':', ','], self._symbol)
        if len(pair) == 2:
            self.base = pair[0]
            self.quote = pair[1]

    def is_backtest(self):
        is_fake_exchange = self.exchange in ['backtest', 'faake_exchange']
        is_live = (self.live == False)
        is_episode = (self.episode is not "live")
        return is_fake_exchange and (is_live or (is_episode))

    def is_order(self) -> bool:
        return self.orderid is not None

    @property
    def slippage(self) -> float:
        return self._slippage

    @slippage.setter
    def slippage(self, _slippage):
        self._slippage = _slippage

    def __str__(self) -> str:
        action_name = "BUY"
        if self.is_sell:
            action_name = "SELL"
        elif self.is_hold:
            action_name = "HOLD"

        return_string = f"<Trade: {action_name}, symbol:{self.symbol}, amount:{self.amount}, price: {self.price}>"
        return return_string
