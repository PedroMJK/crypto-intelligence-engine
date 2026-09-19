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
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "ETHUSDT",
                        "pair": "ETHUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
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


@pytest.mark.asyncio
async def test_get_trading_pairs_excludes_symbols_that_are_not_trading():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "pair": "BTCUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "ETHUSDT",
                        "pair": "ETHUSDT",
                        "status": "BREAK",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                ]
            }

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    result = await scanner.get_trading_pairs()

    assert result == ["BTCUSDT"]


@pytest.mark.asyncio
async def test_get_trading_pairs_excludes_non_perpetual_contracts():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "pair": "BTCUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "ETHUSDT_261225",
                        "pair": "ETHUSDT",
                        "status": "TRADING",
                        "contractType": "CURRENT_QUARTER",
                        "quoteAsset": "USDT",
                    },
                ]
            }

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    result = await scanner.get_trading_pairs()

    assert result == ["BTCUSDT"]


@pytest.mark.asyncio
async def test_get_trading_pairs_excludes_non_usdt_pairs():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "BTCUSDT",
                        "pair": "BTCUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "BTCUSDC",
                        "pair": "BTCUSDC",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDC",
                    },
                ]
            }

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    result = await scanner.get_trading_pairs()

    assert result == ["BTCUSDT"]
