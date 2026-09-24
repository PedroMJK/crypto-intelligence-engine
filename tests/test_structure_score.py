import pytest

from backend.app.analysis.structure_score import StructureScore


def test_structure_score_calculates_average_of_signals():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[0.8, 0.4, -0.3],
    )

    assert result == pytest.approx(0.3)


def test_structure_score_returns_positive_evidence():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[0.6, 0.8],
    )

    assert result == pytest.approx(0.7)


def test_structure_score_returns_negative_evidence():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[-0.6, -0.8],
    )

    assert result == pytest.approx(-0.7)


def test_structure_score_returns_zero_for_balanced_evidence():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[-0.5, 0.5],
    )

    assert result == pytest.approx(0.0)


def test_structure_score_accepts_negative_boundary():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[-1.0],
    )

    assert result == pytest.approx(-1.0)


def test_structure_score_accepts_positive_boundary():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[1.0],
    )

    assert result == pytest.approx(1.0)


def test_structure_score_accepts_single_signal():
    calculator = StructureScore()

    result = calculator.calculate(
        signals=[0.35],
    )

    assert result == pytest.approx(0.35)


def test_structure_score_rejects_non_list_signals():
    calculator = StructureScore()

    with pytest.raises(
        TypeError,
        match="signals must be a list",
    ):
        calculator.calculate(
            signals=(0.2, 0.4),
        )


def test_structure_score_rejects_empty_signals():
    calculator = StructureScore()

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
def test_structure_score_rejects_non_numeric_signals(
    invalid_signal,
):
    calculator = StructureScore()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        calculator.calculate(
            signals=[0.2, invalid_signal],
        )


def test_structure_score_rejects_boolean_signal():
    calculator = StructureScore()

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
def test_structure_score_rejects_out_of_range_signals(
    invalid_signal,
):
    calculator = StructureScore()

    with pytest.raises(
        ValueError,
        match="signals must be between -1.0 and 1.0",
    ):
        calculator.calculate(
            signals=[0.5, invalid_signal],
        )


def test_structure_score_does_not_modify_input():
    calculator = StructureScore()
    signals = [0.6, -0.2, 0.4]
    original_signals = signals.copy()

    calculator.calculate(
        signals=signals,
    )

    assert signals == original_signals


def test_structure_score_is_deterministic():
    calculator = StructureScore()
    signals = [0.6, -0.2, 0.4]

    first_result = calculator.calculate(
        signals=signals,
    )
    second_result = calculator.calculate(
        signals=signals,
    )

    assert first_result == second_result
