import math
from dataclasses import FrozenInstanceError

import pytest

from backend.app.predictions.prediction_outcome import PredictionOutcome


def create_prediction_outcome(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "horizon_minutes": 1,
        "evaluation_timestamp": 1_800_000_060_000,
        "evaluation_price": 0.51,
    }
    values.update(overrides)

    return PredictionOutcome(**values)


def test_prediction_outcome_preserves_observed_state():
    outcome = create_prediction_outcome()

    assert outcome.symbol == "FETUSDT"
    assert outcome.prediction_timestamp == 1_800_000_000_000
    assert outcome.reference_price == 0.50
    assert outcome.horizon_minutes == 1
    assert outcome.evaluation_timestamp == 1_800_000_060_000
    assert outcome.evaluation_price == 0.51


def test_prediction_outcome_calculates_positive_future_return():
    outcome = create_prediction_outcome(
        reference_price=0.50,
        evaluation_price=0.51,
    )

    assert outcome.future_return == pytest.approx(0.02)


def test_prediction_outcome_calculates_negative_future_return():
    outcome = create_prediction_outcome(
        reference_price=0.50,
        evaluation_price=0.49,
    )

    assert outcome.future_return == pytest.approx(-0.02)


def test_prediction_outcome_calculates_zero_future_return():
    outcome = create_prediction_outcome(
        reference_price=0.50,
        evaluation_price=0.50,
    )

    assert outcome.future_return == pytest.approx(0.0)


def test_prediction_outcome_is_immutable():
    outcome = create_prediction_outcome()

    with pytest.raises(FrozenInstanceError):
        outcome.evaluation_price = 0.52


@pytest.mark.parametrize(
    "symbol",
    [
        "",
        123,
        None,
    ],
)
def test_prediction_outcome_rejects_invalid_symbol(symbol):
    expected_exception = (
        ValueError
        if isinstance(symbol, str)
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_prediction_outcome(symbol=symbol)


@pytest.mark.parametrize(
    "prediction_timestamp",
    [
        -1,
        1.5,
        True,
        None,
    ],
)
def test_prediction_outcome_rejects_invalid_prediction_timestamp(
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
        create_prediction_outcome(
            prediction_timestamp=prediction_timestamp,
        )


@pytest.mark.parametrize(
    "reference_price",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_prediction_outcome_rejects_invalid_numeric_reference_price(
    reference_price,
):
    with pytest.raises(ValueError):
        create_prediction_outcome(
            reference_price=reference_price,
        )


@pytest.mark.parametrize(
    "reference_price",
    [
        "0.50",
        True,
        None,
    ],
)
def test_prediction_outcome_rejects_non_numeric_reference_price(
    reference_price,
):
    with pytest.raises(TypeError):
        create_prediction_outcome(
            reference_price=reference_price,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
    ],
)
def test_prediction_outcome_rejects_non_positive_horizon(
    horizon_minutes,
):
    with pytest.raises(ValueError):
        create_prediction_outcome(
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        1.5,
        True,
        None,
    ],
)
def test_prediction_outcome_rejects_invalid_horizon_type(
    horizon_minutes,
):
    with pytest.raises(TypeError):
        create_prediction_outcome(
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "evaluation_timestamp",
    [
        -1,
        1.5,
        True,
        None,
    ],
)
def test_prediction_outcome_rejects_invalid_evaluation_timestamp(
    evaluation_timestamp,
):
    expected_exception = (
        ValueError
        if (
            isinstance(evaluation_timestamp, int)
            and not isinstance(evaluation_timestamp, bool)
        )
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_prediction_outcome(
            evaluation_timestamp=evaluation_timestamp,
        )


def test_prediction_outcome_rejects_evaluation_before_horizon():
    with pytest.raises(ValueError):
        create_prediction_outcome(
            prediction_timestamp=1_800_000_000_000,
            horizon_minutes=1,
            evaluation_timestamp=1_800_000_059_999,
        )


def test_prediction_outcome_accepts_evaluation_at_exact_horizon():
    outcome = create_prediction_outcome(
        prediction_timestamp=1_800_000_000_000,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_000,
    )

    assert outcome.evaluation_timestamp == 1_800_000_060_000


def test_prediction_outcome_accepts_evaluation_after_horizon():
    outcome = create_prediction_outcome(
        prediction_timestamp=1_800_000_000_000,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_500,
    )

    assert outcome.evaluation_timestamp == 1_800_000_060_500


@pytest.mark.parametrize(
    "evaluation_price",
    [
        0.0,
        -1.0,
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_prediction_outcome_rejects_invalid_numeric_evaluation_price(
    evaluation_price,
):
    with pytest.raises(ValueError):
        create_prediction_outcome(
            evaluation_price=evaluation_price,
        )


@pytest.mark.parametrize(
    "evaluation_price",
    [
        "0.51",
        True,
        None,
    ],
)
def test_prediction_outcome_rejects_non_numeric_evaluation_price(
    evaluation_price,
):
    with pytest.raises(TypeError):
        create_prediction_outcome(
            evaluation_price=evaluation_price,
        )
