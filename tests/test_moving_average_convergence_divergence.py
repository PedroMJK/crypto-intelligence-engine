import pytest

from backend.app.analysis.moving_average_convergence_divergence import (
    MovingAverageConvergenceDivergence,
)


def test_moving_average_convergence_divergence_calculates_components():
    macd = MovingAverageConvergenceDivergence()

    result = macd.calculate(
        values=[10.0, 12.0, 11.0, 15.0, 14.0, 18.0],
        fast_period=2,
        slow_period=3,
        signal_period=2,
    )

    assert result["macd"] == pytest.approx(0.8796296296296298)
    assert result["signal"] == pytest.approx(0.7098765432098767)
    assert result["histogram"] == pytest.approx(
        0.16975308641975306
    )


def test_moving_average_convergence_divergence_handles_equal_ema_distance():
    macd = MovingAverageConvergenceDivergence()

    result = macd.calculate(
        values=[10.0, 12.0, 14.0, 16.0],
        fast_period=2,
        slow_period=3,
        signal_period=2,
    )

    assert result["macd"] == pytest.approx(1.0)
    assert result["signal"] == pytest.approx(1.0)
    assert result["histogram"] == pytest.approx(0.0)


def test_moving_average_convergence_divergence_rejects_equal_periods():
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        ValueError,
        match="fast_period must be less than slow_period",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            fast_period=3,
            slow_period=3,
            signal_period=1,
        )


def test_moving_average_convergence_divergence_rejects_fast_period_above_slow():
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        ValueError,
        match="fast_period must be less than slow_period",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            fast_period=3,
            slow_period=2,
            signal_period=1,
        )


@pytest.mark.parametrize(
    "period_name, fast_period, slow_period, signal_period",
    [
        ("fast_period", 0, 3, 2),
        ("slow_period", 2, 0, 1),
        ("signal_period", 2, 3, 0),
    ],
)
def test_moving_average_convergence_divergence_rejects_zero_period(
    period_name,
    fast_period,
    slow_period,
    signal_period,
):
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        ValueError,
        match=f"{period_name} must be greater than zero",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
        )


@pytest.mark.parametrize(
    "period_name, fast_period, slow_period, signal_period",
    [
        ("fast_period", -1, 3, 2),
        ("slow_period", 2, -1, 1),
        ("signal_period", 2, 3, -1),
    ],
)
def test_moving_average_convergence_divergence_rejects_negative_period(
    period_name,
    fast_period,
    slow_period,
    signal_period,
):
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        ValueError,
        match=f"{period_name} must be greater than zero",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
        )


@pytest.mark.parametrize(
    "period_name, fast_period, slow_period, signal_period",
    [
        ("fast_period", 2.5, 3, 1),
        ("slow_period", 2, 3.5, 1),
        ("signal_period", 2, 3, 1.5),
    ],
)
def test_moving_average_convergence_divergence_rejects_non_integer_period(
    period_name,
    fast_period,
    slow_period,
    signal_period,
):
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        TypeError,
        match=f"{period_name} must be an integer",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            fast_period=fast_period,
            slow_period=slow_period,
            signal_period=signal_period,
        )


def test_moving_average_convergence_divergence_rejects_insufficient_values():
    macd = MovingAverageConvergenceDivergence()

    with pytest.raises(
        ValueError,
        match="values do not contain enough elements",
    ):
        macd.calculate(
            values=[10.0, 11.0, 12.0],
            fast_period=2,
            slow_period=3,
            signal_period=2,
        )
