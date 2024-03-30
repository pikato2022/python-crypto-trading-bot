class Instrument:
    def __init__(self, symbol, type, display_name, base_ccy, quote_ccy, quote_decimals, 
                 quantity_decimals, price_tick_size, qty_tick_size, 
                 max_leverage, tradable, expiry_timestamp_ms, underlying_symbol):
        self.symbol = symbol
        self.type = type
        self.display_name = display_name
        self.base_ccy = base_ccy
        self.quote_ccy = quote_ccy
        self.quote_decimals = quote_decimals
        self.quantity_decimals = quantity_decimals
        self.price_tick_size = price_tick_size
        self.qty_tick_size = qty_tick_size
        self.max_leverage = max_leverage
        self.tradable = tradable
        self.expiry_timestamp_ms = expiry_timestamp_ms
        self.underlying_symbol = underlying_symbol
