import pytest

from backend.app.analysis.sell_volume import SellVolume


def test_sell_volume_returns_quantity_for_aggressive_sell():
    sell_volume = SellVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "120.5",
        "m": True,
    }

    result = sell_volume.calculate(trade)

    assert result == 120.5


def test_sell_volume_returns_zero_for_aggressive_buy():
    sell_volume = SellVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "120.5",
        "m": False,
    }

    result = sell_volume.calculate(trade)

    assert result == 0.0


def test_sell_volume_rejects_negative_quantity():
    sell_volume = SellVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "-1.0",
        "m": True,
    }

    with pytest.raises(
        ValueError,
        match="trade quantity cannot be negative",
    ):
        sell_volume.calculate(trade)


def test_sell_volume_accepts_zero_quantity():
    sell_volume = SellVolume()

    trade = {
        "e": "aggTrade",
        "s": "TESTUSDT",
        "p": "0.2500",
        "q": "0",
        "m": True,
    }

    result = sell_volume.calculate(trade)

    assert result == 0.0
