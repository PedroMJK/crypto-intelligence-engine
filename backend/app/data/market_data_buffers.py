from backend.app.data.market_data_buffer import MarketDataBuffer


class MarketDataBuffers:
    def __init__(self, max_size: int):
        self.trade = MarketDataBuffer(max_size=max_size)
        self.ticker = MarketDataBuffer(max_size=max_size)
        self.candle = MarketDataBuffer(max_size=max_size)
        self.order_book = MarketDataBuffer(max_size=max_size)
