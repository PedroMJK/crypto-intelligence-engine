import pytest

from backend.app.intelligence.contradiction_engine import (
    ContradictionEngine,
)


def test_contradiction_engine_returns_zero_for_bullish_agreement():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[0.9, 0.8, 0.7],
    )

    assert result == pytest.approx(0.0)


def test_contradiction_engine_returns_zero_for_bearish_agreement():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[-0.9, -0.8, -0.7],
    )

    assert result == pytest.approx(0.0)


def test_contradiction_engine_returns_one_for_maximum_opposition():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[1.0, -1.0],
    )

    assert result == pytest.approx(1.0)


def test_contradiction_engine_accounts_for_signal_magnitude():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[0.1, -0.1],
    )

    assert result == pytest.approx(0.1)


def test_contradiction_engine_calculates_partial_contradiction():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[0.8, 0.6, -0.4],
    )

    assert result == pytest.approx(
        2 * (0.4 / 3),
    )


def test_contradiction_engine_accounts_for_neutral_signals():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[1.0, -1.0, 0.0, 0.0],
    )

    assert result == pytest.approx(0.5)


def test_contradiction_engine_returns_zero_for_neutral_signals():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[0.0, 0.0],
    )

    assert result == pytest.approx(0.0)


def test_contradiction_engine_returns_zero_for_direction_and_neutrality():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[0.9, 0.0],
    )

    assert result == pytest.approx(0.0)


def test_contradiction_engine_accepts_single_signal():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[-0.8],
    )

    assert result == pytest.approx(0.0)


def test_contradiction_engine_accepts_boundaries():
    engine = ContradictionEngine()

    result = engine.calculate(
        signals=[-1.0, 0.0, 1.0],
    )

    assert result == pytest.approx(
        2 / 3,
    )


def test_contradiction_engine_rejects_non_list_signals():
    engine = ContradictionEngine()

    with pytest.raises(
        TypeError,
        match="signals must be a list",
    ):
        engine.calculate(
            signals=(0.5, -0.5),
        )


def test_contradiction_engine_rejects_empty_signals():
    engine = ContradictionEngine()

    with pytest.raises(
        ValueError,
        match="signals must not be empty",
    ):
        engine.calculate(
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
def test_contradiction_engine_rejects_non_numeric_signals(
    invalid_signal,
):
    engine = ContradictionEngine()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        engine.calculate(
            signals=[0.5, invalid_signal],
        )


def test_contradiction_engine_rejects_boolean_signal():
    engine = ContradictionEngine()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        engine.calculate(
            signals=[0.5, True],
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
def test_contradiction_engine_rejects_out_of_range_signals(
    invalid_signal,
):
    engine = ContradictionEngine()

    with pytest.raises(
        ValueError,
        match="signals must be between -1.0 and 1.0",
    ):
        engine.calculate(
            signals=[0.5, invalid_signal],
        )


def test_contradiction_engine_does_not_modify_input():
    engine = ContradictionEngine()
    signals = [0.8, -0.4, 0.2]
    original_signals = signals.copy()

    engine.calculate(
        signals=signals,
    )

    assert signals == original_signals


def test_contradiction_engine_is_deterministic():
    engine = ContradictionEngine()
    signals = [0.8, -0.4, 0.2]

    first_result = engine.calculate(
        signals=signals,
    )
    second_result = engine.calculate(
        signals=signals,
    )

    assert first_result == second_result
