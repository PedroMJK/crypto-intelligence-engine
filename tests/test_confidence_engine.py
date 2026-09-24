import pytest

from backend.app.intelligence.confidence_engine import ConfidenceEngine


def test_confidence_engine_calculates_average_of_signals():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[0.8, 0.4, 0.3],
    )

    assert result == pytest.approx(0.5)


def test_confidence_engine_returns_high_strength():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[0.8, 1.0],
    )

    assert result == pytest.approx(0.9)


def test_confidence_engine_returns_low_strength():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[0.1, 0.3],
    )

    assert result == pytest.approx(0.2)


def test_confidence_engine_accepts_zero():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[0.0],
    )

    assert result == pytest.approx(0.0)


def test_confidence_engine_accepts_one():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[1.0],
    )

    assert result == pytest.approx(1.0)


def test_confidence_engine_accepts_single_signal():
    engine = ConfidenceEngine()

    result = engine.calculate(
        signals=[0.35],
    )

    assert result == pytest.approx(0.35)


def test_confidence_engine_rejects_non_list_signals():
    engine = ConfidenceEngine()

    with pytest.raises(
        TypeError,
        match="signals must be a list",
    ):
        engine.calculate(
            signals=(0.2, 0.4),
        )


def test_confidence_engine_rejects_empty_signals():
    engine = ConfidenceEngine()

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
def test_confidence_engine_rejects_non_numeric_signals(
    invalid_signal,
):
    engine = ConfidenceEngine()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        engine.calculate(
            signals=[0.2, invalid_signal],
        )


def test_confidence_engine_rejects_boolean_signal():
    engine = ConfidenceEngine()

    with pytest.raises(
        TypeError,
        match="signals must contain only numbers",
    ):
        engine.calculate(
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
def test_confidence_engine_rejects_out_of_range_signals(
    invalid_signal,
):
    engine = ConfidenceEngine()

    with pytest.raises(
        ValueError,
        match="signals must be between 0.0 and 1.0",
    ):
        engine.calculate(
            signals=[0.5, invalid_signal],
        )


def test_confidence_engine_does_not_modify_input():
    engine = ConfidenceEngine()
    signals = [0.6, 0.2, 0.4]
    original_signals = signals.copy()

    engine.calculate(
        signals=signals,
    )

    assert signals == original_signals


def test_confidence_engine_is_deterministic():
    engine = ConfidenceEngine()
    signals = [0.6, 0.2, 0.4]

    first_result = engine.calculate(
        signals=signals,
    )
    second_result = engine.calculate(
        signals=signals,
    )

    assert first_result == second_result
