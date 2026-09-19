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
