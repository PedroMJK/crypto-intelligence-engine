import pytest

from backend.app.scanner.liquidity_filter import LiquidityFilter
from backend.app.scanner.price_filter import PriceFilter
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


@pytest.mark.asyncio
async def test_get_pairs_by_price_filters_relevant_trading_pairs():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "LOWUSDT",
                        "pair": "LOWUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "MIDUSDT",
                        "pair": "MIDUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "HIGHUSDT",
                        "pair": "HIGHUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "OTHERUSDC",
                        "pair": "OTHERUSDC",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDC",
                    },
                ]
            }

        async def get_ticker_prices(self):
            return [
                {"symbol": "LOWUSDT", "price": "0.05"},
                {"symbol": "MIDUSDT", "price": "0.50"},
                {"symbol": "HIGHUSDT", "price": "2.00"},
                {"symbol": "OTHERUSDC", "price": "0.50"},
            ]

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    price_filter = PriceFilter(
        min_price=0.10,
        max_price=1.00,
    )

    result = await scanner.get_pairs_by_price(price_filter)

    assert result == [
        {
            "symbol": "MIDUSDT",
            "price": 0.50,
        }
    ]


@pytest.mark.asyncio
async def test_get_pairs_by_liquidity_filters_relevant_trading_pairs():
    class FakeMarketDataClient:
        async def get_exchange_info(self):
            return {
                "symbols": [
                    {
                        "symbol": "LIQUIDUSDT",
                        "pair": "LIQUIDUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "ILLIQUIDUSDT",
                        "pair": "ILLIQUIDUSDT",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDT",
                    },
                    {
                        "symbol": "OTHERUSDC",
                        "pair": "OTHERUSDC",
                        "status": "TRADING",
                        "contractType": "PERPETUAL",
                        "quoteAsset": "USDC",
                    },
                ]
            }

        async def get_book_tickers(self):
            return [
                {
                    "symbol": "LIQUIDUSDT",
                    "bidPrice": "0.499",
                    "askPrice": "0.501",
                },
                {
                    "symbol": "ILLIQUIDUSDT",
                    "bidPrice": "0.45",
                    "askPrice": "0.55",
                },
                {
                    "symbol": "OTHERUSDC",
                    "bidPrice": "0.499",
                    "askPrice": "0.501",
                },
            ]

    scanner = TradingPairScanner(
        market_data_client=FakeMarketDataClient(),
    )

    liquidity_filter = LiquidityFilter(
        max_spread_ratio=0.01,
    )

    result = await scanner.get_pairs_by_liquidity(liquidity_filter)

    assert result == [
        {
            "symbol": "LIQUIDUSDT",
            "bid_price": 0.499,
            "ask_price": 0.501,
        }
    ]
