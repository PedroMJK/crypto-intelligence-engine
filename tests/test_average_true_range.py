import pytest

from backend.app.analysis.average_true_range import AverageTrueRange


def test_average_true_range_calculates_initial_average():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate(
        highs=[12.0, 13.0, 15.0],
        lows=[10.0, 11.0, 12.0],
        closes=[11.0, 12.0, 14.0],
        period=3,
    )

    assert result == pytest.approx(7.0 / 3.0)


def test_average_true_range_uses_previous_close_for_upward_gap():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate(
        highs=[10.0, 12.0],
        lows=[9.0, 11.0],
        closes=[9.5, 11.5],
        period=2,
    )

    assert result == pytest.approx(1.75)


def test_average_true_range_uses_previous_close_for_downward_gap():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate(
        highs=[12.0, 10.0],
        lows=[11.0, 9.0],
        closes=[11.5, 9.5],
        period=2,
    )

    assert result == pytest.approx(1.75)


def test_average_true_range_applies_wilder_smoothing():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate(
        highs=[12.0, 13.0, 15.0, 16.0],
        lows=[10.0, 11.0, 12.0, 13.0],
        closes=[11.0, 12.0, 14.0, 15.0],
        period=3,
    )

    assert result == pytest.approx(23.0 / 9.0)


def test_average_true_range_supports_period_of_one():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate(
        highs=[12.0, 15.0],
        lows=[10.0, 13.0],
        closes=[11.0, 14.0],
        period=1,
    )

    assert result == pytest.approx(4.0)


def test_average_true_range_rejects_zero_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        average_true_range.calculate(
            highs=[12.0],
            lows=[10.0],
            closes=[11.0],
            period=0,
        )


def test_average_true_range_rejects_negative_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        average_true_range.calculate(
            highs=[12.0],
            lows=[10.0],
            closes=[11.0],
            period=-1,
        )


def test_average_true_range_rejects_non_integer_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        TypeError,
        match="period must be an integer",
    ):
        average_true_range.calculate(
            highs=[12.0, 13.0],
            lows=[10.0, 11.0],
            closes=[11.0, 12.0],
            period=1.5,
        )


def test_average_true_range_rejects_different_series_lengths():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="highs, lows, and closes must have the same length",
    ):
        average_true_range.calculate(
            highs=[12.0, 13.0],
            lows=[10.0],
            closes=[11.0, 12.0],
            period=1,
        )


def test_average_true_range_rejects_insufficient_values():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="price series must contain at least period elements",
    ):
        average_true_range.calculate(
            highs=[12.0, 13.0],
            lows=[10.0, 11.0],
            closes=[11.0, 12.0],
            period=3,
        )


def test_average_true_range_rejects_high_below_low():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="high cannot be lower than low",
    ):
        average_true_range.calculate(
            highs=[12.0, 10.0],
            lows=[10.0, 11.0],
            closes=[11.0, 10.5],
            period=2,
        )


def test_average_true_range_calculates_series():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate_series(
        highs=[12.0, 13.0, 15.0, 16.0, 18.0],
        lows=[10.0, 11.0, 12.0, 13.0, 15.0],
        closes=[11.0, 12.0, 14.0, 15.0, 17.0],
        period=3,
    )

    assert result == pytest.approx(
        [
            7.0 / 3.0,
            23.0 / 9.0,
            73.0 / 27.0,
        ]
    )


def test_average_true_range_series_returns_single_initial_atr():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate_series(
        highs=[12.0, 13.0, 15.0],
        lows=[10.0, 11.0, 12.0],
        closes=[11.0, 12.0, 14.0],
        period=3,
    )

    assert result == pytest.approx(
        [
            7.0 / 3.0,
        ]
    )


def test_average_true_range_series_supports_period_of_one():
    average_true_range = AverageTrueRange()

    result = average_true_range.calculate_series(
        highs=[12.0, 15.0, 16.0],
        lows=[10.0, 13.0, 14.0],
        closes=[11.0, 14.0, 15.0],
        period=1,
    )

    assert result == pytest.approx(
        [
            2.0,
            4.0,
            2.0,
        ]
    )


def test_average_true_range_series_rejects_zero_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        average_true_range.calculate_series(
            highs=[12.0],
            lows=[10.0],
            closes=[11.0],
            period=0,
        )


def test_average_true_range_series_rejects_negative_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        average_true_range.calculate_series(
            highs=[12.0],
            lows=[10.0],
            closes=[11.0],
            period=-1,
        )


def test_average_true_range_series_rejects_non_integer_period():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        TypeError,
        match="period must be an integer",
    ):
        average_true_range.calculate_series(
            highs=[12.0, 13.0],
            lows=[10.0, 11.0],
            closes=[11.0, 12.0],
            period=1.5,
        )


def test_average_true_range_series_rejects_different_series_lengths():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="highs, lows, and closes must have the same length",
    ):
        average_true_range.calculate_series(
            highs=[12.0, 13.0],
            lows=[10.0],
            closes=[11.0, 12.0],
            period=1,
        )


def test_average_true_range_series_rejects_insufficient_values():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="price series must contain at least period elements",
    ):
        average_true_range.calculate_series(
            highs=[12.0, 13.0],
            lows=[10.0, 11.0],
            closes=[11.0, 12.0],
            period=3,
        )


def test_average_true_range_series_rejects_high_below_low():
    average_true_range = AverageTrueRange()

    with pytest.raises(
        ValueError,
        match="high cannot be lower than low",
    ):
        average_true_range.calculate_series(
            highs=[12.0, 10.0],
            lows=[10.0, 11.0],
            closes=[11.0, 10.5],
            period=2,
        )
