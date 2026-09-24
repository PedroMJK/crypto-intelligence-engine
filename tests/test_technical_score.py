import pytest

from backend.app.analysis.technical_score import TechnicalScore


def test_technical_score_calculates_average_of_signals():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[0.6, 0.2, -0.2],
    )

    assert result == pytest.approx(0.2)


def test_technical_score_returns_positive_score():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[0.8, 0.4],
    )

    assert result == pytest.approx(0.6)


def test_technical_score_returns_negative_score():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[-0.8, -0.4],
    )

    assert result == pytest.approx(-0.6)


def test_technical_score_returns_zero_for_balanced_signals():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[-0.5, 0.5],
    )

    assert result == pytest.approx(0.0)


def test_technical_score_accepts_boundary_values():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[-1.0, 1.0],
    )

    assert result == pytest.approx(0.0)


def test_technical_score_accepts_single_signal():
    calculator = TechnicalScore()

    result = calculator.calculate(
        signals=[0.35],
    )

    assert result == pytest.approx(0.35)


def test_technical_score_rejects_non_list_signals():
    calculator = TechnicalScore()

    with pytest.raises(
        TypeError,
        match="signals must be a list",
    ):
        calculator.calculate(
            signals=(0.2, 0.4),
        )


def test_technical_score_rejects_empty_signals():
    calculator = TechnicalScore()

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
def test_technical_score_rejects_non_numeric_signals(
    invalid_signal,
):
    calculator = TechnicalScore()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        calculator.calculate(
            signals=[0.2, invalid_signal],
        )


def test_technical_score_rejects_boolean_signal():
    calculator = TechnicalScore()

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
        -1.01,
        1.01,
        -2.0,
        2.0,
    ],
)
def test_technical_score_rejects_out_of_range_signals(
    invalid_signal,
):
    calculator = TechnicalScore()

    with pytest.raises(
        ValueError,
        match="signals must be between -1.0 and 1.0",
    ):
        calculator.calculate(
            signals=[0.0, invalid_signal],
        )


def test_technical_score_does_not_modify_input():
    calculator = TechnicalScore()
    signals = [0.6, -0.2, 0.4]
    original_signals = signals.copy()

    calculator.calculate(
        signals=signals,
    )

    assert signals == original_signals


def test_technical_score_is_deterministic():
    calculator = TechnicalScore()
    signals = [0.6, -0.2, 0.4]

    first_result = calculator.calculate(
        signals=signals,
    )
    second_result = calculator.calculate(
        signals=signals,
    )

    assert first_result == second_result
