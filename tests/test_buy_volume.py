import pytest

from backend.app.analysis.buy_volume import BuyVolume


def test_buy_volume_returns_quantity_for_aggressive_buy():
    buy_volume = BuyVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "120.5",
        "m": False,
    }

    result = buy_volume.calculate(trade)

    assert result == 120.5


def test_buy_volume_returns_zero_for_aggressive_sell():
    buy_volume = BuyVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "120.5",
        "m": True,
    }

    result = buy_volume.calculate(trade)

    assert result == 0.0


def test_buy_volume_rejects_negative_quantity():
    buy_volume = BuyVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "-1.0",
        "m": False,
    }

    with pytest.raises(
        ValueError,
        match="trade quantity cannot be negative",
    ):
        buy_volume.calculate(trade)


def test_buy_volume_accepts_zero_quantity():
    buy_volume = BuyVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "0",
        "m": False,
    }

    result = buy_volume.calculate(trade)

    assert result == 0.0
