import pytest

from backend.app.scanner.price_filter import PriceFilter


def test_price_filter_returns_pairs_within_price_range():
    price_filter = PriceFilter(
        min_price=0.10,
        max_price=1.00,
    )

    pairs = [
        {"symbol": "ADAUSDT", "price": 0.50},
        {"symbol": "XRPUSDT", "price": 1.50},
    ]

    result = price_filter.filter(pairs)

    assert result == [
        {"symbol": "ADAUSDT", "price": 0.50},
    ]


def test_price_filter_excludes_pairs_below_minimum_price():
    price_filter = PriceFilter(
        min_price=0.10,
        max_price=1.00,
    )

    pairs = [
        {"symbol": "LOWUSDT", "price": 0.05},
        {"symbol": "ADAUSDT", "price": 0.50},
    ]

    result = price_filter.filter(pairs)

    assert result == [
        {"symbol": "ADAUSDT", "price": 0.50},
    ]


def test_price_filter_includes_pairs_at_price_boundaries():
    price_filter = PriceFilter(
        min_price=0.10,
        max_price=1.00,
    )

    pairs = [
        {"symbol": "MINUSDT", "price": 0.10},
        {"symbol": "MAXUSDT", "price": 1.00},
    ]

    result = price_filter.filter(pairs)

    assert result == [
        {"symbol": "MINUSDT", "price": 0.10},
        {"symbol": "MAXUSDT", "price": 1.00},
    ]


def test_price_filter_rejects_minimum_price_greater_than_maximum_price():
    with pytest.raises(
        ValueError,
        match="min_price cannot be greater than max_price",
    ):
        PriceFilter(
            min_price=1.00,
            max_price=0.10,
        )
