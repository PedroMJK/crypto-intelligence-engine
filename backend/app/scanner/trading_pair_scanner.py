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

    async def get_filtered_pairs(
        self,
        price_filter,
        liquidity_filter,
        volume_filter,
        activity_filter,
    ) -> list[dict]:
        trading_pairs = await self.get_trading_pairs()
        ticker_prices = await self.market_data_client.get_ticker_prices()
        book_tickers = await self.market_data_client.get_book_tickers()
        ticker_statistics = await self.market_data_client.get_ticker_statistics()

        trading_pair_symbols = set(trading_pairs)

        prices_by_symbol = {
            ticker["symbol"]: float(ticker["price"])
            for ticker in ticker_prices
            if ticker["symbol"] in trading_pair_symbols
        }

        books_by_symbol = {
            ticker["symbol"]: {
                "bid_price": float(ticker["bidPrice"]),
                "ask_price": float(ticker["askPrice"]),
            }
            for ticker in book_tickers
            if ticker["symbol"] in trading_pair_symbols
        }

        statistics_by_symbol = {
            ticker["symbol"]: {
                "quote_volume": float(ticker["quoteVolume"]),
                "trade_count": int(ticker["count"]),
            }
            for ticker in ticker_statistics
            if ticker["symbol"] in trading_pair_symbols
        }

        pairs = [
            {
                "symbol": symbol,
                "price": prices_by_symbol[symbol],
                "bid_price": books_by_symbol[symbol]["bid_price"],
                "ask_price": books_by_symbol[symbol]["ask_price"],
                "quote_volume": statistics_by_symbol[symbol]["quote_volume"],
                "trade_count": statistics_by_symbol[symbol]["trade_count"],
            }
            for symbol in trading_pairs
            if symbol in prices_by_symbol
            and symbol in books_by_symbol
            and symbol in statistics_by_symbol
        ]

        pairs = price_filter.filter(pairs)
        pairs = liquidity_filter.filter(pairs)
        pairs = volume_filter.filter(pairs)
        pairs = activity_filter.filter(pairs)

        return pairs

    async def get_ranked_pairs(
        self,
        price_filter,
        liquidity_filter,
        volume_filter,
        activity_filter,
        ranking,
    ) -> list[dict]:
        filtered_pairs = await self.get_filtered_pairs(
            price_filter=price_filter,
            liquidity_filter=liquidity_filter,
            volume_filter=volume_filter,
            activity_filter=activity_filter,
        )

        return ranking.rank(filtered_pairs)
