import pytest

from backend.app.analysis.buy_sell_ratio import BuySellRatio


def test_buy_sell_ratio_calculates_ratio():
    buy_sell_ratio = BuySellRatio()

    result = buy_sell_ratio.calculate(
        buy_volume=150.0,
        sell_volume=100.0,
    )

    assert result == 1.5


def test_buy_sell_ratio_returns_one_for_equal_volumes():
    buy_sell_ratio = BuySellRatio()

    result = buy_sell_ratio.calculate(
        buy_volume=100.0,
        sell_volume=100.0,
    )

    assert result == 1.0


def test_buy_sell_ratio_returns_zero_when_buy_volume_is_zero():
    buy_sell_ratio = BuySellRatio()

    result = buy_sell_ratio.calculate(
        buy_volume=0.0,
        sell_volume=100.0,
    )

    assert result == 0.0


def test_buy_sell_ratio_rejects_negative_buy_volume():
    buy_sell_ratio = BuySellRatio()

    with pytest.raises(
        ValueError,
        match="buy_volume cannot be negative",
    ):
        buy_sell_ratio.calculate(
            buy_volume=-1.0,
            sell_volume=100.0,
        )


def test_buy_sell_ratio_rejects_negative_sell_volume():
    buy_sell_ratio = BuySellRatio()

    with pytest.raises(
        ValueError,
        match="sell_volume cannot be negative",
    ):
        buy_sell_ratio.calculate(
            buy_volume=100.0,
            sell_volume=-1.0,
        )


def test_buy_sell_ratio_rejects_zero_sell_volume():
    buy_sell_ratio = BuySellRatio()

    with pytest.raises(
        ValueError,
        match="sell_volume must be greater than zero",
    ):
        buy_sell_ratio.calculate(
            buy_volume=100.0,
            sell_volume=0.0,
        )
