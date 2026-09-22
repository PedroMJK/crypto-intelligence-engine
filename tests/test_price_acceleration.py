import pytest

from backend.app.analysis.price_acceleration import PriceAcceleration


def test_price_acceleration_calculates_positive_acceleration():
    price_acceleration = PriceAcceleration()

    result = price_acceleration.calculate(
        previous_velocity=0.01,
        current_velocity=0.03,
        window_seconds=2.0,
    )

    assert result == pytest.approx(0.01)


def test_price_acceleration_calculates_negative_acceleration():
    price_acceleration = PriceAcceleration()

    result = price_acceleration.calculate(
        previous_velocity=0.03,
        current_velocity=0.01,
        window_seconds=2.0,
    )

    assert result == pytest.approx(-0.01)


def test_price_acceleration_returns_zero_when_velocity_does_not_change():
    price_acceleration = PriceAcceleration()

    result = price_acceleration.calculate(
        previous_velocity=0.02,
        current_velocity=0.02,
        window_seconds=2.0,
    )

    assert result == 0.0


def test_price_acceleration_supports_negative_velocities():
    price_acceleration = PriceAcceleration()

    result = price_acceleration.calculate(
        previous_velocity=-0.03,
        current_velocity=-0.01,
        window_seconds=2.0,
    )

    assert result == pytest.approx(0.01)


def test_price_acceleration_rejects_zero_window():
    price_acceleration = PriceAcceleration()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        price_acceleration.calculate(
            previous_velocity=0.01,
            current_velocity=0.03,
            window_seconds=0.0,
        )


def test_price_acceleration_rejects_negative_window():
    price_acceleration = PriceAcceleration()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        price_acceleration.calculate(
            previous_velocity=0.01,
            current_velocity=0.03,
            window_seconds=-1.0,
        )
