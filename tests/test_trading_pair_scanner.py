import pytest

from backend.app.scanner.trading_pair_scanner import TradingPairScanner


@pytest.mark.asyncio
async def test_get_trading_pairs_returns_symbol_names():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "pair": "BTCUSDT",
                        "status": "TRADING",
                    },
                    {
                        "symbol": "ETHUSDT",
                        "pair": "ETHUSDT",
                        "status": "TRADING",
                    },
                ]
            }

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    result = await scanner.get_trading_pairs()

    assert result == ["BTCUSDT", "ETHUSDT"]


@pytest.mark.asyncio
async def test_get_trading_pairs_returns_empty_list_when_no_symbols_exist():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [],
            }

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    result = await scanner.get_trading_pairs()

    assert result == []
