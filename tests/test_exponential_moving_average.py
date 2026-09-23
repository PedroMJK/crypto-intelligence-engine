import pytest

from backend.app.analysis.exponential_moving_average import (
    ExponentialMovingAverage,
)


def test_exponential_moving_average_equals_initial_average_for_exact_period():
    exponential_moving_average = ExponentialMovingAverage()

    result = exponential_moving_average.calculate(
        values=[10.0, 12.0, 14.0],
        period=3,
    )

    assert result == pytest.approx(12.0)


def test_exponential_moving_average_applies_weight_to_new_values():
    exponential_moving_average = ExponentialMovingAverage()

    result = exponential_moving_average.calculate(
        values=[10.0, 12.0, 14.0, 16.0, 18.0],
        period=3,
    )

    assert result == pytest.approx(16.0)


def test_exponential_moving_average_supports_period_of_one():
    exponential_moving_average = ExponentialMovingAverage()

    result = exponential_moving_average.calculate(
        values=[10.0, 12.0, 14.0],
        period=1,
    )

    assert result == pytest.approx(14.0)


def test_exponential_moving_average_rejects_zero_period():
    exponential_moving_average = ExponentialMovingAverage()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        exponential_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=0,
        )


def test_exponential_moving_average_rejects_negative_period():
    exponential_moving_average = ExponentialMovingAverage()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        exponential_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=-1,
        )


def test_exponential_moving_average_rejects_period_larger_than_values():
    exponential_moving_average = ExponentialMovingAverage()

    with pytest.raises(
        ValueError,
        match="values must contain at least period elements",
    ):
        exponential_moving_average.calculate(
            values=[10.0, 12.0],
            period=3,
        )


def test_exponential_moving_average_rejects_non_integer_period():
    exponential_moving_average = ExponentialMovingAverage()

    with pytest.raises(
        TypeError,
        match="period must be an integer",
    ):
        exponential_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=2.5,
        )
