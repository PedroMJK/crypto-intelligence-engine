import math

import pytest

from backend.app.intelligence.ensemble_engine import (
    EnsembleEngine,
    EnsembleResult,
)


def test_ensemble_engine_aggregates_bullish_direction():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.1,
    )

    assert result.direction_score == pytest.approx(0.6)


def test_ensemble_engine_aggregates_bearish_direction():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=-0.8,
        flow_score=-0.6,
        momentum_score=-0.4,
        structure_score=-0.6,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.1,
    )

    assert result.direction_score == pytest.approx(-0.6)


def test_ensemble_engine_returns_neutral_direction_for_balanced_scores():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.8,
        flow_score=-0.8,
        momentum_score=0.6,
        structure_score=-0.6,
        volume_score=0.8,
        confidence=0.9,
        contradiction=0.8,
    )

    assert result.direction_score == pytest.approx(0.0)


def test_ensemble_engine_returns_neutral_direction_for_neutral_scores():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.0,
        flow_score=0.0,
        momentum_score=0.0,
        structure_score=0.0,
        volume_score=0.5,
        confidence=0.5,
        contradiction=0.0,
    )

    assert result.direction_score == pytest.approx(0.0)


def test_ensemble_engine_preserves_volume_score():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.5,
        flow_score=0.5,
        momentum_score=0.5,
        structure_score=0.5,
        volume_score=0.9,
        confidence=0.7,
        contradiction=0.2,
    )

    assert result.volume_score == pytest.approx(0.9)


def test_ensemble_engine_preserves_confidence():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.5,
        flow_score=0.5,
        momentum_score=0.5,
        structure_score=0.5,
        volume_score=0.8,
        confidence=0.75,
        contradiction=0.2,
    )

    assert result.confidence == pytest.approx(0.75)


def test_ensemble_engine_preserves_contradiction():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.5,
        flow_score=0.5,
        momentum_score=0.5,
        structure_score=0.5,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.35,
    )

    assert result.contradiction == pytest.approx(0.35)


def test_volume_score_does_not_change_direction():
    engine = EnsembleEngine()

    low_volume = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.0,
        confidence=0.7,
        contradiction=0.1,
    )

    high_volume = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=1.0,
        confidence=0.7,
        contradiction=0.1,
    )

    assert low_volume.direction_score == high_volume.direction_score


def test_confidence_does_not_change_direction():
    engine = EnsembleEngine()

    low_confidence = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.8,
        confidence=0.0,
        contradiction=0.1,
    )

    high_confidence = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.8,
        confidence=1.0,
        contradiction=0.1,
    )

    assert low_confidence.direction_score == high_confidence.direction_score


def test_contradiction_does_not_change_direction():
    engine = EnsembleEngine()

    low_contradiction = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.0,
    )

    high_contradiction = engine.calculate(
        technical_score=0.8,
        flow_score=0.6,
        momentum_score=0.4,
        structure_score=0.6,
        volume_score=0.8,
        confidence=0.7,
        contradiction=1.0,
    )

    assert (
        low_contradiction.direction_score
        == high_contradiction.direction_score
    )


def test_ensemble_engine_accepts_valid_boundaries():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=-1.0,
        flow_score=1.0,
        momentum_score=-1.0,
        structure_score=1.0,
        volume_score=1.0,
        confidence=0.0,
        contradiction=1.0,
    )

    assert result.direction_score == pytest.approx(0.0)
    assert result.volume_score == pytest.approx(1.0)
    assert result.confidence == pytest.approx(0.0)
    assert result.contradiction == pytest.approx(1.0)


@pytest.mark.parametrize(
    "field_name",
    [
        "technical_score",
        "flow_score",
        "momentum_score",
        "structure_score",
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        -1.01,
        1.01,
    ],
)
def test_ensemble_engine_rejects_directional_scores_out_of_range(
    field_name,
    invalid_value,
):
    engine = EnsembleEngine()

    values = {
        "technical_score": 0.5,
        "flow_score": 0.5,
        "momentum_score": 0.5,
        "structure_score": 0.5,
        "volume_score": 0.5,
        "confidence": 0.5,
        "contradiction": 0.5,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be between -1.0 and 1.0",
    ):
        engine.calculate(**values)


@pytest.mark.parametrize(
    "field_name",
    [
        "volume_score",
        "confidence",
        "contradiction",
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        -0.01,
        1.01,
    ],
)
def test_ensemble_engine_rejects_non_directional_scores_out_of_range(
    field_name,
    invalid_value,
):
    engine = EnsembleEngine()

    values = {
        "technical_score": 0.5,
        "flow_score": 0.5,
        "momentum_score": 0.5,
        "structure_score": 0.5,
        "volume_score": 0.5,
        "confidence": 0.5,
        "contradiction": 0.5,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be between 0.0 and 1.0",
    ):
        engine.calculate(**values)


@pytest.mark.parametrize(
    "field_name",
    [
        "technical_score",
        "flow_score",
        "momentum_score",
        "structure_score",
        "volume_score",
        "confidence",
        "contradiction",
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        "0.5",
        None,
        [],
        {},
        True,
    ],
)
def test_ensemble_engine_rejects_non_numeric_values(
    field_name,
    invalid_value,
):
    engine = EnsembleEngine()

    values = {
        "technical_score": 0.5,
        "flow_score": 0.5,
        "momentum_score": 0.5,
        "structure_score": 0.5,
        "volume_score": 0.5,
        "confidence": 0.5,
        "contradiction": 0.5,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        TypeError,
        match=rf"{field_name} must be a number",
    ):
        engine.calculate(**values)


@pytest.mark.parametrize(
    "field_name",
    [
        "technical_score",
        "flow_score",
        "momentum_score",
        "structure_score",
        "volume_score",
        "confidence",
        "contradiction",
    ],
)
@pytest.mark.parametrize(
    "invalid_value",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_ensemble_engine_rejects_non_finite_values(
    field_name,
    invalid_value,
):
    engine = EnsembleEngine()

    values = {
        "technical_score": 0.5,
        "flow_score": 0.5,
        "momentum_score": 0.5,
        "structure_score": 0.5,
        "volume_score": 0.5,
        "confidence": 0.5,
        "contradiction": 0.5,
    }
    values[field_name] = invalid_value

    with pytest.raises(
        ValueError,
        match=rf"{field_name} must be finite",
    ):
        engine.calculate(**values)


def test_ensemble_engine_returns_ensemble_result():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.5,
        flow_score=0.4,
        momentum_score=0.3,
        structure_score=0.2,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.1,
    )

    assert isinstance(result, EnsembleResult)


def test_ensemble_result_is_immutable():
    engine = EnsembleEngine()

    result = engine.calculate(
        technical_score=0.5,
        flow_score=0.4,
        momentum_score=0.3,
        structure_score=0.2,
        volume_score=0.8,
        confidence=0.7,
        contradiction=0.1,
    )

    with pytest.raises(AttributeError):
        result.direction_score = 1.0


def test_ensemble_engine_is_deterministic():
    engine = EnsembleEngine()

    values = {
        "technical_score": 0.8,
        "flow_score": 0.6,
        "momentum_score": 0.4,
        "structure_score": 0.2,
        "volume_score": 0.9,
        "confidence": 0.7,
        "contradiction": 0.1,
    }

    first_result = engine.calculate(**values)
    second_result = engine.calculate(**values)

    assert first_result == second_result
