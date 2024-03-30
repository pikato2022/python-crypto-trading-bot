class Trade:
    def __init__(self, d, t, tn, q, p, s, i):
        self.id = d
        self.trade_ts = t
        self.trade_tnn = tn
        self.quantity = q
        self.price = p
        self.side = s # BUY or SELL
        self.instru_name = i