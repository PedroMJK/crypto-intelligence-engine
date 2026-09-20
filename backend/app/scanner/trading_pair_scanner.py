class TradingPairScanner:
    def __init__(self, market_data_client):
        self.market_data_client = market_data_client

    async def get_trading_pairs(self) -> list[str]:
        exchange_info = await self.market_data_client.get_exchange_info()

        return [
            symbol["symbol"]
            for symbol in exchange_info["symbols"]
            if symbol["status"] == "TRADING"
            and symbol["contractType"] == "PERPETUAL"
            and symbol["quoteAsset"] == "USDT"
        ]

    async def get_pairs_by_price(self, price_filter) -> list[dict]:
        trading_pairs = await self.get_trading_pairs()
        ticker_prices = await self.market_data_client.get_ticker_prices()

        trading_pair_symbols = set(trading_pairs)

        pairs_with_prices = [
            {
                "symbol": ticker["symbol"],
                "price": float(ticker["price"]),
            }
            for ticker in ticker_prices
            if ticker["symbol"] in trading_pair_symbols
        ]

        return price_filter.filter(pairs_with_prices)

    async def get_pairs_by_liquidity(self, liquidity_filter) -> list[dict]:
        trading_pairs = await self.get_trading_pairs()
        book_tickers = await self.market_data_client.get_book_tickers()

        trading_pair_symbols = set(trading_pairs)

        pairs_with_book_prices = [
            {
                "symbol": ticker["symbol"],
                "bid_price": float(ticker["bidPrice"]),
                "ask_price": float(ticker["askPrice"]),
            }
            for ticker in book_tickers
            if ticker["symbol"] in trading_pair_symbols
        ]

        return liquidity_filter.filter(pairs_with_book_prices)

    async def get_pairs_by_volume(self, volume_filter) -> list[dict]:
        trading_pairs = await self.get_trading_pairs()
        ticker_statistics = await self.market_data_client.get_ticker_statistics()

        trading_pair_symbols = set(trading_pairs)

        pairs_with_volumes = [
            {
                "symbol": ticker["symbol"],
                "quote_volume": float(ticker["quoteVolume"]),
            }
            for ticker in ticker_statistics
            if ticker["symbol"] in trading_pair_symbols
        ]

        return volume_filter.filter(pairs_with_volumes)

    async def get_pairs_by_activity(self, activity_filter) -> list[dict]:
        trading_pairs = await self.get_trading_pairs()
        ticker_statistics = await self.market_data_client.get_ticker_statistics()

        trading_pair_symbols = set(trading_pairs)

        pairs_with_activity = [
            {
                "symbol": ticker["symbol"],
                "trade_count": int(ticker["count"]),
            }
            for ticker in ticker_statistics
            if ticker["symbol"] in trading_pair_symbols
        ]

        return activity_filter.filter(pairs_with_activity)
