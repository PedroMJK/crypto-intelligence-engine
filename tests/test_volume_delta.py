import pytest

from backend.app.analysis.volume_delta import VolumeDelta


def test_volume_delta_returns_positive_delta():
    volume_delta = VolumeDelta()

    result = volume_delta.calculate(
        buy_volume=150.0,
        sell_volume=100.0,
    )

    assert result == 50.0


def test_volume_delta_returns_negative_delta():
    volume_delta = VolumeDelta()

    result = volume_delta.calculate(
        buy_volume=100.0,
        sell_volume=150.0,
    )

    assert result == -50.0


def test_volume_delta_returns_zero_for_equal_volumes():
    volume_delta = VolumeDelta()

    result = volume_delta.calculate(
        buy_volume=100.0,
        sell_volume=100.0,
    )

    assert result == 0.0


def test_volume_delta_accepts_zero_buy_volume():
    volume_delta = VolumeDelta()

    result = volume_delta.calculate(
        buy_volume=0.0,
        sell_volume=100.0,
    )

    assert result == -100.0


def test_volume_delta_accepts_zero_sell_volume():
    volume_delta = VolumeDelta()

    result = volume_delta.calculate(
        buy_volume=100.0,
        sell_volume=0.0,
    )

    assert result == 100.0


def test_volume_delta_rejects_negative_buy_volume():
    volume_delta = VolumeDelta()

    with pytest.raises(
        ValueError,
        match="buy_volume cannot be negative",
    ):
        volume_delta.calculate(
            buy_volume=-1.0,
            sell_volume=100.0,
        )


def test_volume_delta_rejects_negative_sell_volume():
    volume_delta = VolumeDelta()

    with pytest.raises(
        ValueError,
        match="sell_volume cannot be negative",
    ):
        volume_delta.calculate(
            buy_volume=100.0,
            sell_volume=-1.0,
        )
