import pytest

from backend.app.scanner.liquidity_filter import LiquidityFilter


def test_liquidity_filter_returns_pairs_within_maximum_spread():
    liquidity_filter = LiquidityFilter(
        max_spread_ratio=0.01,
    )

    pairs = [
        {
            "symbol": "LIQUIDUSDT",
            "bid_price": 0.499,
            "ask_price": 0.501,
        },
        {
            "symbol": "ILLIQUIDUSDT",
            "bid_price": 0.45,
            "ask_price": 0.55,
        },
    ]

    result = liquidity_filter.filter(pairs)

    assert result == [
        {
            "symbol": "LIQUIDUSDT",
            "bid_price": 0.499,
            "ask_price": 0.501,
        }
    ]


def test_liquidity_filter_includes_pair_at_maximum_spread():
    liquidity_filter = LiquidityFilter(
        max_spread_ratio=0.01,
    )

    pairs = [
        {
            "symbol": "BOUNDARYUSDT",
            "bid_price": 0.995,
            "ask_price": 1.005,
        },
    ]

    result = liquidity_filter.filter(pairs)

    assert result == [
        {
            "symbol": "BOUNDARYUSDT",
            "bid_price": 0.995,
            "ask_price": 1.005,
        }
    ]


def test_liquidity_filter_rejects_negative_maximum_spread():
    with pytest.raises(
        ValueError,
        match="max_spread_ratio cannot be negative",
    ):
        LiquidityFilter(
            max_spread_ratio=-0.01,
        )


def test_liquidity_filter_rejects_non_positive_prices():
    liquidity_filter = LiquidityFilter(
        max_spread_ratio=0.01,
    )

    pairs = [
        {
            "symbol": "INVALIDUSDT",
            "bid_price": 0.0,
            "ask_price": 0.0,
        },
    ]

    with pytest.raises(
        ValueError,
        match="bid_price and ask_price must be greater than zero",
    ):
        liquidity_filter.filter(pairs)


def test_liquidity_filter_rejects_ask_price_below_bid_price():
    liquidity_filter = LiquidityFilter(
        max_spread_ratio=0.01,
    )

    pairs = [
        {
            "symbol": "INVALIDUSDT",
            "bid_price": 1.01,
            "ask_price": 0.99,
        },
    ]

    with pytest.raises(
        ValueError,
        match="ask_price cannot be lower than bid_price",
    ):
        liquidity_filter.filter(pairs)
