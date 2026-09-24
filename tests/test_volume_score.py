import pytest

from backend.app.analysis.volume_score import VolumeScore


def test_volume_score_calculates_average_of_signals():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[0.8, 0.4, 0.3],
    )

    assert result == pytest.approx(0.5)


def test_volume_score_returns_high_intensity():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[0.8, 1.0],
    )

    assert result == pytest.approx(0.9)


def test_volume_score_returns_low_intensity():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[0.1, 0.3],
    )

    assert result == pytest.approx(0.2)


def test_volume_score_accepts_zero():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[0.0],
    )

    assert result == pytest.approx(0.0)


def test_volume_score_accepts_one():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[1.0],
    )

    assert result == pytest.approx(1.0)


def test_volume_score_accepts_single_signal():
    calculator = VolumeScore()

    result = calculator.calculate(
        signals=[0.35],
    )

    assert result == pytest.approx(0.35)


def test_volume_score_rejects_non_list_signals():
    calculator = VolumeScore()

    with pytest.raises(
        TypeError,
        match="signals must be a list",
    ):
        calculator.calculate(
            signals=(0.2, 0.4),
        )


def test_volume_score_rejects_empty_signals():
    calculator = VolumeScore()

    with pytest.raises(
        ValueError,
        match="signals must not be empty",
    ):
        calculator.calculate(
            signals=[],
        )


@pytest.mark.parametrize(
    "invalid_signal",
    [
        "0.5",
        None,
        {},
        [],
    ],
)
def test_volume_score_rejects_non_numeric_signals(
    invalid_signal,
):
    calculator = VolumeScore()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        calculator.calculate(
            signals=[0.2, invalid_signal],
        )


def test_volume_score_rejects_boolean_signal():
    calculator = VolumeScore()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        calculator.calculate(
            signals=[0.2, True],
        )


@pytest.mark.parametrize(
    "invalid_signal",
    [
        -0.01,
        1.01,
        -1.0,
        2.0,
    ],
)
def test_volume_score_rejects_out_of_range_signals(
    invalid_signal,
):
    calculator = VolumeScore()

    with pytest.raises(
        ValueError,
        match="signals must be between 0.0 and 1.0",
    ):
        calculator.calculate(
            signals=[0.5, invalid_signal],
        )


def test_volume_score_does_not_modify_input():
    calculator = VolumeScore()
    signals = [0.6, 0.2, 0.4]
    original_signals = signals.copy()

    calculator.calculate(
        signals=signals,
    )

    assert signals == original_signals


def test_volume_score_is_deterministic():
    calculator = VolumeScore()
    signals = [0.6, 0.2, 0.4]

    first_result = calculator.calculate(
        signals=signals,
    )
    second_result = calculator.calculate(
        signals=signals,
    )

    assert first_result == second_result
