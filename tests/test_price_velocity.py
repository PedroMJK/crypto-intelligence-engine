import pytest

from backend.app.analysis.price_velocity import PriceVelocity


def test_price_velocity_calculates_positive_velocity():
    price_velocity = PriceVelocity()

    result = price_velocity.calculate(
        previous_price=100.0,
        current_price=105.0,
        window_seconds=5.0,
    )

    assert result == pytest.approx(0.01)


def test_price_velocity_calculates_negative_velocity():
    price_velocity = PriceVelocity()

    result = price_velocity.calculate(
        previous_price=100.0,
        current_price=95.0,
        window_seconds=5.0,
    )

    assert result == pytest.approx(-0.01)


def test_price_velocity_returns_zero_when_price_does_not_change():
    price_velocity = PriceVelocity()

    result = price_velocity.calculate(
        previous_price=100.0,
        current_price=100.0,
        window_seconds=5.0,
    )

    assert result == 0.0


def test_price_velocity_rejects_zero_previous_price():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="previous_price must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=0.0,
            current_price=100.0,
            window_seconds=5.0,
        )


def test_price_velocity_rejects_negative_previous_price():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="previous_price must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=-100.0,
            current_price=100.0,
            window_seconds=5.0,
        )


def test_price_velocity_rejects_zero_current_price():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="current_price must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=100.0,
            current_price=0.0,
            window_seconds=5.0,
        )


def test_price_velocity_rejects_negative_current_price():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="current_price must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=100.0,
            current_price=-100.0,
            window_seconds=5.0,
        )


def test_price_velocity_rejects_zero_window():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=100.0,
            current_price=105.0,
            window_seconds=0.0,
        )


def test_price_velocity_rejects_negative_window():
    price_velocity = PriceVelocity()

    with pytest.raises(
        ValueError,
        match="window_seconds must be greater than zero",
    ):
        price_velocity.calculate(
            previous_price=100.0,
            current_price=105.0,
            window_seconds=-1.0,
        )
