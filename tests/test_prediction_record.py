import math
from dataclasses import FrozenInstanceError

import pytest

from backend.app.predictions.prediction_record import PredictionRecord


def create_prediction_record(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.5821,
        "direction_score": 0.65,
    }
    values.update(overrides)

    return PredictionRecord(**values)


def test_prediction_record_preserves_prediction_snapshot():
    record = create_prediction_record()

    assert record.symbol == "FETUSDT"
    assert record.prediction_timestamp == 1_800_000_000_000
    assert record.reference_price == 0.5821
    assert record.direction_score == 0.65


def test_prediction_record_is_immutable():
    record = create_prediction_record()

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
def test_prediction_record_rejects_invalid_symbol(symbol):
    expected_exception = (
        ValueError
        if isinstance(symbol, str)
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_prediction_record(symbol=symbol)


@pytest.mark.parametrize(
    "prediction_timestamp",
    [
        -1,
        1.5,
        True,
        None,
    ],
)
def test_prediction_record_rejects_invalid_prediction_timestamp(
    prediction_timestamp,
):
    expected_exception = (
        ValueError
        if (
            isinstance(prediction_timestamp, int)
            and not isinstance(prediction_timestamp, bool)
        )
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_prediction_record(
            prediction_timestamp=prediction_timestamp,
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
def test_prediction_record_rejects_invalid_reference_price_value(
    reference_price,
):
    with pytest.raises(ValueError):
        create_prediction_record(
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
def test_prediction_record_rejects_non_numeric_reference_price(
    reference_price,
):
    with pytest.raises(TypeError):
        create_prediction_record(
            reference_price=reference_price,
        )


@pytest.mark.parametrize(
    "direction_score",
    [
        -1.01,
        1.01,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_prediction_record_rejects_invalid_direction_score_value(
    direction_score,
):
    with pytest.raises(ValueError):
        create_prediction_record(
            direction_score=direction_score,
        )


@pytest.mark.parametrize(
    "direction_score",
    [
        "0.65",
        True,
        None,
    ],
)
def test_prediction_record_rejects_non_numeric_direction_score(
    direction_score,
):
    with pytest.raises(TypeError):
        create_prediction_record(
            direction_score=direction_score,
        )


@pytest.mark.parametrize(
    "direction_score",
    [
        -1.0,
        0.0,
        1.0,
    ],
)
def test_prediction_record_accepts_direction_score_boundaries(
    direction_score,
):
    record = create_prediction_record(
        direction_score=direction_score,
    )

    assert record.direction_score == direction_score
