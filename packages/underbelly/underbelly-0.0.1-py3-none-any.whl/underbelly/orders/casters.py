import uuid
from underbelly.orders import TradeType, Trade
from underbelly.orders.utils import camel_to_snake


class TradeCaster(object):
    requirements = [
        "symbol",
        "trade_type",
        "amount",
        "price",
    ]
    cast_vars = {
        "limit_buy": TradeType.LIMIT_BUY,
        "limit_sell": TradeType.LIMIT_SELL,
        "market_sell": TradeType.MARKET_SELL,
        "market_buy": TradeType.MARKET_BUY,
    }

    def extract_trade_type(self, trade_type):
        if isinstance(trade_type, TradeType):
            return trade_type
        _camel = camel_to_snake(trade_type)
        return self.cast_vars.get(_camel, TradeType.HOLD)

    def cast(self, **kwargs) -> 'Trade':
        is_valid = all(x in kwargs for x in self.requirements)
        if not is_valid:
            raise AttributeError(
                f"For the cast to be valid you need {self.requirements}"
            )
        ttype = kwargs.get("trade_type")
        symbol = kwargs.get("symbol", "BTC_USD")
        amount = kwargs.get("amount", 0.0)
        price = kwargs.get("price", 0.0)
        trade_type = self.extract_trade_type(ttype)
        trade = Trade(
            symbol=symbol, trade_type=trade_type, amount=amount, price=price
        )
        trade.orderid = kwargs.get("order_id", None)
        trade.userid = kwargs.get("user_id", uuid.uuid4().hex)
        trade.episode = kwargs.get("episode", uuid.uuid4().hex)
        trade.exchange = kwargs.get("exchange", "backtest")
        trade.live = kwargs.get("live", False)
        return trade


__all__ = ["TradeCaster"]