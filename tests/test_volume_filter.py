import pytest

from backend.app.scanner.volume_filter import VolumeFilter


def test_volume_filter_returns_pairs_above_minimum_quote_volume():
    volume_filter = VolumeFilter(
        min_quote_volume=1_000_000.0,
    )

    pairs = [
        {
            "symbol": "HIGHVOLUMEUSDT",
            "quote_volume": 5_000_000.0,
        },
        {
            "symbol": "LOWVOLUMEUSDT",
            "quote_volume": 250_000.0,
        },
    ]

    result = volume_filter.filter(pairs)

    assert result == [
        {
            "symbol": "HIGHVOLUMEUSDT",
            "quote_volume": 5_000_000.0,
        }
    ]


def test_volume_filter_includes_pair_at_minimum_quote_volume():
    volume_filter = VolumeFilter(
        min_quote_volume=1_000_000.0,
    )

    pairs = [
        {
            "symbol": "BOUNDARYUSDT",
            "quote_volume": 1_000_000.0,
        },
    ]

    result = volume_filter.filter(pairs)

    assert result == [
        {
            "symbol": "BOUNDARYUSDT",
            "quote_volume": 1_000_000.0,
        }
    ]


def test_volume_filter_rejects_negative_minimum_quote_volume():
    with pytest.raises(
        ValueError,
        match="min_quote_volume cannot be negative",
    ):
        VolumeFilter(
            min_quote_volume=-1.0,
        )


def test_volume_filter_rejects_negative_quote_volume():
    volume_filter = VolumeFilter(
        min_quote_volume=1_000_000.0,
    )

    pairs = [
        {
            "symbol": "INVALIDUSDT",
            "quote_volume": -1.0,
        },
    ]

    with pytest.raises(
        ValueError,
        match="quote_volume cannot be negative",
    ):
        volume_filter.filter(pairs)
