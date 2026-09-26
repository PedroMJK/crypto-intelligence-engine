import pytest

from backend.app.predictions.outcome_evaluator import OutcomeEvaluator
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


def create_prediction(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "direction_score": 0.65,
    }
    values.update(overrides)

    return PredictionRecord(**values)


def test_outcome_evaluator_creates_prediction_outcome():
    prediction = create_prediction()

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_000,
        evaluation_price=0.51,
    )

    assert isinstance(outcome, PredictionOutcome)


def test_outcome_evaluator_preserves_prediction_identity_data():
    prediction = create_prediction()

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_000,
        evaluation_price=0.51,
    )

    assert outcome.symbol == prediction.symbol
    assert (
        outcome.prediction_timestamp
        == prediction.prediction_timestamp
    )
    assert outcome.reference_price == prediction.reference_price


def test_outcome_evaluator_preserves_evaluation_data():
    prediction = create_prediction()

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_500,
        evaluation_price=0.51,
    )

    assert outcome.horizon_minutes == 1
    assert outcome.evaluation_timestamp == 1_800_000_060_500
    assert outcome.evaluation_price == 0.51


def test_outcome_evaluator_returns_calculated_future_return():
    prediction = create_prediction(
        reference_price=0.50,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=1,
        evaluation_timestamp=1_800_000_060_000,
        evaluation_price=0.51,
    )

    assert outcome.future_return == pytest.approx(0.02)


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        {},
        "FETUSDT",
        123,
        True,
    ],
)
def test_outcome_evaluator_rejects_non_prediction_record(
    prediction,
):
    with pytest.raises(TypeError):
        OutcomeEvaluator.evaluate(
            prediction=prediction,
            horizon_minutes=1,
            evaluation_timestamp=1_800_000_060_000,
            evaluation_price=0.51,
        )


def test_outcome_evaluator_delegates_outcome_validation():
    prediction = create_prediction()

    with pytest.raises(ValueError):
        OutcomeEvaluator.evaluate(
            prediction=prediction,
            horizon_minutes=1,
            evaluation_timestamp=1_800_000_059_999,
            evaluation_price=0.51,
        )


def test_outcome_evaluator_creates_five_minute_outcome():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
        reference_price=0.50,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=5,
        evaluation_timestamp=1_800_000_300_000,
        evaluation_price=0.525,
    )

    assert outcome.horizon_minutes == 5
    assert outcome.evaluation_timestamp == 1_800_000_300_000
    assert outcome.evaluation_price == 0.525
    assert outcome.future_return == pytest.approx(0.05)


def test_outcome_evaluator_rejects_five_minute_evaluation_before_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    with pytest.raises(ValueError):
        OutcomeEvaluator.evaluate(
            prediction=prediction,
            horizon_minutes=5,
            evaluation_timestamp=1_800_000_299_999,
            evaluation_price=0.51,
        )


def test_outcome_evaluator_accepts_five_minute_evaluation_after_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=5,
        evaluation_timestamp=1_800_000_300_500,
        evaluation_price=0.51,
    )

    assert outcome.horizon_minutes == 5
    assert outcome.evaluation_timestamp == 1_800_000_300_500


def test_outcome_evaluator_creates_fifteen_minute_outcome():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
        reference_price=0.50,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=15,
        evaluation_timestamp=1_800_000_900_000,
        evaluation_price=0.55,
    )

    assert outcome.horizon_minutes == 15
    assert outcome.evaluation_timestamp == 1_800_000_900_000
    assert outcome.evaluation_price == 0.55
    assert outcome.future_return == pytest.approx(0.10)


def test_outcome_evaluator_rejects_fifteen_minute_evaluation_before_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    with pytest.raises(ValueError):
        OutcomeEvaluator.evaluate(
            prediction=prediction,
            horizon_minutes=15,
            evaluation_timestamp=1_800_000_899_999,
            evaluation_price=0.51,
        )


def test_outcome_evaluator_accepts_fifteen_minute_evaluation_after_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=15,
        evaluation_timestamp=1_800_000_900_500,
        evaluation_price=0.51,
    )

    assert outcome.horizon_minutes == 15
    assert outcome.evaluation_timestamp == 1_800_000_900_500


def test_outcome_evaluator_creates_thirty_minute_outcome():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
        reference_price=0.50,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=30,
        evaluation_timestamp=1_800_001_800_000,
        evaluation_price=0.575,
    )

    assert outcome.horizon_minutes == 30
    assert outcome.evaluation_timestamp == 1_800_001_800_000
    assert outcome.evaluation_price == 0.575
    assert outcome.future_return == pytest.approx(0.15)


def test_outcome_evaluator_rejects_thirty_minute_evaluation_before_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    with pytest.raises(ValueError):
        OutcomeEvaluator.evaluate(
            prediction=prediction,
            horizon_minutes=30,
            evaluation_timestamp=1_800_001_799_999,
            evaluation_price=0.51,
        )


def test_outcome_evaluator_accepts_thirty_minute_evaluation_after_horizon():
    prediction = create_prediction(
        prediction_timestamp=1_800_000_000_000,
    )

    outcome = OutcomeEvaluator.evaluate(
        prediction=prediction,
        horizon_minutes=30,
        evaluation_timestamp=1_800_001_800_500,
        evaluation_price=0.51,
    )

    assert outcome.horizon_minutes == 30
    assert outcome.evaluation_timestamp == 1_800_001_800_500
