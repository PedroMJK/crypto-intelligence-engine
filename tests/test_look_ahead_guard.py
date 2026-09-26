import pytest

from backend.app.backtesting.backtest_sample import BacktestSample
from backend.app.backtesting.look_ahead_guard import LookAheadGuard
from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


def create_sample(
    *,
    symbol="FETUSDT",
    timestamp=1_800_000_000_000,
    reference_price=0.50,
    direction_score=0.60,
    horizon_minutes=5,
    evaluation_timestamp=None,
    evaluation_price=0.525,
):
    if evaluation_timestamp is None:
        evaluation_timestamp = (
            timestamp
            + horizon_minutes * 60_000
        )

    features = FeatureSnapshot(
        symbol=symbol,
        feature_timestamp=timestamp,
        features={
            "technical_score": 0.40,
            "flow_score": -0.20,
            "volume_score": 0.70,
        },
    )

    prediction = PredictionRecord(
        symbol=symbol,
        prediction_timestamp=timestamp,
        reference_price=reference_price,
        direction_score=direction_score,
    )

    outcome = PredictionOutcome(
        symbol=symbol,
        prediction_timestamp=timestamp,
        reference_price=reference_price,
        horizon_minutes=horizon_minutes,
        evaluation_timestamp=evaluation_timestamp,
        evaluation_price=evaluation_price,
    )

    return BacktestSample(
        features=features,
        prediction=prediction,
        outcome=outcome,
    )


def test_look_ahead_guard_accepts_valid_sample():
    sample = create_sample()

    result = LookAheadGuard.validate(sample)

    assert result is None


@pytest.mark.parametrize(
    "sample",
    [
        None,
        123,
        True,
        "sample",
        [],
        (),
        {},
    ],
)
def test_look_ahead_guard_rejects_invalid_sample(sample):
    with pytest.raises(TypeError):
        LookAheadGuard.validate(sample)


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        1,
        5,
        15,
        30,
    ],
)
def test_look_ahead_guard_accepts_supported_horizons(
    horizon_minutes,
):
    sample = create_sample(
        horizon_minutes=horizon_minutes,
    )

    LookAheadGuard.validate(sample)


def test_look_ahead_guard_accepts_evaluation_after_minimum_horizon():
    timestamp = 1_800_000_000_000

    sample = create_sample(
        timestamp=timestamp,
        horizon_minutes=5,
        evaluation_timestamp=(
            timestamp
            + 5 * 60_000
            + 1
        ),
    )

    LookAheadGuard.validate(sample)


def test_look_ahead_guard_preserves_sample():
    sample = create_sample()

    original_features = sample.features
    original_prediction = sample.prediction
    original_outcome = sample.outcome

    LookAheadGuard.validate(sample)

    assert sample.features is original_features
    assert sample.prediction is original_prediction
    assert sample.outcome is original_outcome
