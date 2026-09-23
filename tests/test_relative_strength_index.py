import pytest

from backend.app.analysis.relative_strength_index import (
    RelativeStrengthIndex,
)


def test_relative_strength_index_returns_100_for_only_gains():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[10.0, 11.0, 12.0, 13.0],
        period=3,
    )

    assert result == pytest.approx(100.0)


def test_relative_strength_index_returns_zero_for_only_losses():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[13.0, 12.0, 11.0, 10.0],
        period=3,
    )

    assert result == pytest.approx(0.0)


def test_relative_strength_index_returns_50_for_flat_values():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[10.0, 10.0, 10.0, 10.0],
        period=3,
    )

    assert result == pytest.approx(50.0)


def test_relative_strength_index_calculates_mixed_changes():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[10.0, 12.0, 11.0, 13.0],
        period=3,
    )

    assert result == pytest.approx(80.0)


def test_relative_strength_index_applies_wilder_smoothing():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[10.0, 12.0, 11.0, 13.0, 12.0],
        period=3,
    )

    assert result == pytest.approx(61.53846153846154)


def test_relative_strength_index_supports_period_of_one():
    relative_strength_index = RelativeStrengthIndex()

    result = relative_strength_index.calculate(
        values=[10.0, 12.0],
        period=1,
    )

    assert result == pytest.approx(100.0)


def test_relative_strength_index_rejects_zero_period():
    relative_strength_index = RelativeStrengthIndex()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        relative_strength_index.calculate(
            values=[10.0, 11.0],
            period=0,
        )


def test_relative_strength_index_rejects_negative_period():
    relative_strength_index = RelativeStrengthIndex()

    with pytest.raises(
        ValueError,
        match="period must be greater than zero",
    ):
        relative_strength_index.calculate(
            values=[10.0, 11.0],
            period=-1,
        )


def test_relative_strength_index_rejects_insufficient_values():
    relative_strength_index = RelativeStrengthIndex()

    with pytest.raises(
        ValueError,
        match="values must contain at least period plus one elements",
    ):
        relative_strength_index.calculate(
            values=[10.0, 11.0, 12.0],
            period=3,
        )


def test_relative_strength_index_rejects_non_integer_period():
    relative_strength_index = RelativeStrengthIndex()

    with pytest.raises(
        TypeError,
        match="period must be an integer",
    ):
        relative_strength_index.calculate(
            values=[10.0, 11.0, 12.0, 13.0],
            period=2.5,
        )
