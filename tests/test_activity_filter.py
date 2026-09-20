import pytest

from backend.app.scanner.activity_filter import ActivityFilter


def test_activity_filter_returns_pairs_above_minimum_trade_count():
    activity_filter = ActivityFilter(
        min_trade_count=1_000,
    )

    pairs = [
        {
            "symbol": "ACTIVEUSDT",
            "trade_count": 5_000,
        },
        {
            "symbol": "INACTIVEUSDT",
            "trade_count": 250,
        },
    ]

    result = activity_filter.filter(pairs)

    assert result == [
        {
            "symbol": "ACTIVEUSDT",
            "trade_count": 5_000,
        }
    ]


def test_activity_filter_includes_pair_at_minimum_trade_count():
    activity_filter = ActivityFilter(
        min_trade_count=1_000,
    )

    pairs = [
        {
            "symbol": "BOUNDARYUSDT",
            "trade_count": 1_000,
        },
    ]

    result = activity_filter.filter(pairs)

    assert result == [
        {
            "symbol": "BOUNDARYUSDT",
            "trade_count": 1_000,
        }
    ]


def test_activity_filter_rejects_negative_minimum_trade_count():
    with pytest.raises(
        ValueError,
        match="min_trade_count cannot be negative",
    ):
        ActivityFilter(
            min_trade_count=-1,
        )


def test_activity_filter_rejects_negative_trade_count():
    activity_filter = ActivityFilter(
        min_trade_count=1_000,
    )

    pairs = [
        {
            "symbol": "INVALIDUSDT",
            "trade_count": -1,
        },
    ]

    with pytest.raises(
        ValueError,
        match="trade_count cannot be negative",
    ):
        activity_filter.filter(pairs)
