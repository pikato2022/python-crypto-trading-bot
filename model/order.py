from enum import StrEnum, auto


class Order:
    def __init__(self, price: float, isSell: bool, quantity: float) -> None:
        self.price = price
        self.isSell = isSell
        self.quantity = quantity


# LIMIT	timeInForce, quantity, price
# MARKET	quantity or quoteOrderQty
# STOP_LOSS	quantity, stopPrice or trailingDelta
# STOP_LOSS_LIMIT	timeInForce, quantity, price, stopPrice or trailingDelta
# TAKE_PROFIT	quantity, stopPrice or trailingDelta
# TAKE_PROFIT_LIMIT	timeInForce, quantity, price, stopPrice or trailingDelta
# LIMIT_MAKER	quantity, price


class BinanceTimeInForce(StrEnum):
    GTC = auto()
    IOC = auto()
    FOK = auto()


class OrderType(StrEnum):
    LIMIT = auto()
    MARKET = auto()
    STOP_LOSS = auto()
    STOP_LOSS_LIMIT = auto()
    TAKE_PROFIT = auto()
    TAKE_PROFIT_LIMIT = auto()
    LIMIT_MAKER = auto()


# symbol: str, side: str, type: str, **kwargs


class BinanceOrder(Order):
    def __init__(
        self,
        price: float,
        isSell: bool,
        quantity: float,
        type: OrderType,
        timeInforce: BinanceTimeInForce = None,
        symbol: str = "BTCUSDT",
    ) -> None:
        super().__init__(price, isSell, quantity)
        self.type = type
        self.timeInForce = timeInforce
        self.symbol = symbol

    def to_exchange_dict(self):
        side = "SELL" if self.isSell else "BUY"
        return {
            # "side": side,
            # "type": self.type.value,
            # "symbol": self.symbol,
            "price": self.price,
            "timeInForce": self.timeInForce.value,
            "quantity": self.quantity,
        }
