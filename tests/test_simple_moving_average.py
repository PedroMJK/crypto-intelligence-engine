import pytest

from backend.app.analysis.simple_moving_average import SimpleMovingAverage


def test_simple_moving_average_calculates_average_for_period():
    simple_moving_average = SimpleMovingAverage()

    result = simple_moving_average.calculate(
        values=[10.0, 12.0, 14.0],
        period=3,
    )

    assert result == pytest.approx(12.0)


def test_simple_moving_average_uses_latest_values_for_period():
    simple_moving_average = SimpleMovingAverage()

    result = simple_moving_average.calculate(
        values=[10.0, 12.0, 14.0, 16.0, 18.0],
        period=3,
    )

    assert result == pytest.approx(16.0)


def test_simple_moving_average_supports_period_of_one():
    simple_moving_average = SimpleMovingAverage()

    result = simple_moving_average.calculate(
        values=[10.0, 12.0, 14.0],
        period=1,
    )

    assert result == pytest.approx(14.0)


def test_simple_moving_average_rejects_zero_period():
    simple_moving_average = SimpleMovingAverage()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        simple_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=0,
        )


def test_simple_moving_average_rejects_negative_period():
    simple_moving_average = SimpleMovingAverage()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        simple_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=-1,
        )


def test_simple_moving_average_rejects_period_larger_than_values():
    simple_moving_average = SimpleMovingAverage()

    with pytest.raises(
        ValueError,
        match="values must contain at least period elements",
    ):
        simple_moving_average.calculate(
            values=[10.0, 12.0],
            period=3,
        )


def test_simple_moving_average_rejects_non_integer_period():
    simple_moving_average = SimpleMovingAverage()

    with pytest.raises(
        TypeError,
        match="period must be an integer",
    ):
        simple_moving_average.calculate(
            values=[10.0, 12.0, 14.0],
            period=2.5,
        )
