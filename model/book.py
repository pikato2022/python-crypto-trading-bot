class Book:
    def __init__(self, asks, bids):
        self.asks = asks
        self.bid = bids

class TradeRequest:
    def __init__(self, price, quantity, numOfOrder, isAsk = True):
        self.price = price
        self.quantity = quantity
        self.numOfOrder = numOfOrder
        self.isAsk = isAsk
    