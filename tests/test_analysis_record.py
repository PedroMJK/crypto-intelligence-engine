import math
from dataclasses import FrozenInstanceError

import pytest

from backend.app.predictions.analysis_record import AnalysisRecord


def create_analysis_record(**overrides):
    values = {
        "symbol": "FETUSDT",
        "reference_timestamp": 1_800_000_000_000,
        "reference_price": 0.5821,
        "technical_score": 0.6,
        "flow_score": 0.7,
        "momentum_score": 0.5,
        "structure_score": 0.8,
        "direction_score": 0.65,
        "volume_score": 0.75,
        "confidence": 0.7,
        "contradiction": 0.1,
    }
    values.update(overrides)

    return AnalysisRecord(**values)


def test_analysis_record_preserves_analysis_snapshot():
    record = create_analysis_record()

    assert record.symbol == "FETUSDT"
    assert record.reference_timestamp == 1_800_000_000_000
    assert record.reference_price == 0.5821
    assert record.technical_score == 0.6
    assert record.flow_score == 0.7
    assert record.momentum_score == 0.5
    assert record.structure_score == 0.8
    assert record.direction_score == 0.65
    assert record.volume_score == 0.75
    assert record.confidence == 0.7
    assert record.contradiction == 0.1


def test_analysis_record_is_immutable():
    record = create_analysis_record()

    with pytest.raises(FrozenInstanceError):
        record.direction_score = 0.9


@pytest.mark.parametrize(
    "symbol",
    [
        "",
        123,
        None,
    ],
)
def test_analysis_record_rejects_invalid_symbol(symbol):
    expected_exception = (
        ValueError
        if isinstance(symbol, str)
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_analysis_record(symbol=symbol)


@pytest.mark.parametrize(
    "reference_timestamp",
    [
        -1,
        1.5,
        True,
        None,
    ],
)
def test_analysis_record_rejects_invalid_reference_timestamp(
    reference_timestamp,
):
    expected_exception = (
        ValueError
        if (
            isinstance(reference_timestamp, int)
            and not isinstance(reference_timestamp, bool)
        )
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_analysis_record(
            reference_timestamp=reference_timestamp,
        )


@pytest.mark.parametrize(
    "reference_price",
    [
        0.0,
        -0.1,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_analysis_record_rejects_invalid_reference_price_value(
    reference_price,
):
    with pytest.raises(ValueError):
        create_analysis_record(
            reference_price=reference_price,
        )


@pytest.mark.parametrize(
    "reference_price",
    [
        "0.5821",
        True,
        None,
    ],
)
def test_analysis_record_rejects_non_numeric_reference_price(
    reference_price,
):
    with pytest.raises(TypeError):
        create_analysis_record(
            reference_price=reference_price,
        )


@pytest.mark.parametrize(
    "score_name",
    [
        "technical_score",
        "flow_score",
        "momentum_score",
        "structure_score",
        "direction_score",
    ],
)
@pytest.mark.parametrize(
    "score_value",
    [
        -1.01,
        1.01,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_analysis_record_rejects_invalid_directional_score_values(
    score_name,
    score_value,
):
    with pytest.raises(ValueError):
        create_analysis_record(
            **{score_name: score_value},
        )


@pytest.mark.parametrize(
    "score_name",
    [
        "technical_score",
        "flow_score",
        "momentum_score",
        "structure_score",
        "direction_score",
    ],
)
@pytest.mark.parametrize(
    "score_value",
    [
        "0.5",
        True,
        None,
    ],
)
def test_analysis_record_rejects_non_numeric_directional_scores(
    score_name,
    score_value,
):
    with pytest.raises(TypeError):
        create_analysis_record(
            **{score_name: score_value},
        )


@pytest.mark.parametrize(
    "score_name",
    [
        "volume_score",
        "confidence",
        "contradiction",
    ],
)
@pytest.mark.parametrize(
    "score_value",
    [
        -0.01,
        1.01,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_analysis_record_rejects_invalid_non_directional_score_values(
    score_name,
    score_value,
):
    with pytest.raises(ValueError):
        create_analysis_record(
            **{score_name: score_value},
        )


@pytest.mark.parametrize(
    "score_name",
    [
        "volume_score",
        "confidence",
        "contradiction",
    ],
)
@pytest.mark.parametrize(
    "score_value",
    [
        "0.5",
        True,
        None,
    ],
)
def test_analysis_record_rejects_non_numeric_non_directional_scores(
    score_name,
    score_value,
):
    with pytest.raises(TypeError):
        create_analysis_record(
            **{score_name: score_value},
        )
