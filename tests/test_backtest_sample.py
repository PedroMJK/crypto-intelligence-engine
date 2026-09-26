import pytest

from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord
from backend.app.backtesting.backtest_sample import BacktestSample


def create_feature_snapshot(**overrides):
    values = {
        "symbol": "FETUSDT",
        "feature_timestamp": 1_800_000_000_000,
        "features": {
            "technical_score": 0.40,
            "flow_score": -0.20,
            "volume_score": 0.70,
        },
    }
    values.update(overrides)

    return FeatureSnapshot(**values)


def create_prediction(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "direction_score": 0.60,
    }
    values.update(overrides)

    return PredictionRecord(**values)


def create_outcome(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "horizon_minutes": 5,
        "evaluation_timestamp": 1_800_000_300_000,
        "evaluation_price": 0.525,
    }
    values.update(overrides)

    return PredictionOutcome(**values)


def create_sample(
    feature_snapshot=None,
    prediction=None,
    outcome=None,
):
    return BacktestSample(
        features=(
            feature_snapshot
            if feature_snapshot is not None
            else create_feature_snapshot()
        ),
        prediction=(
            prediction
            if prediction is not None
            else create_prediction()
        ),
        outcome=(
            outcome
            if outcome is not None
            else create_outcome()
        ),
    )


def test_backtest_sample_preserves_components():
    features = create_feature_snapshot()
    prediction = create_prediction()
    outcome = create_outcome()

    sample = create_sample(
        feature_snapshot=features,
        prediction=prediction,
        outcome=outcome,
    )

    assert sample.features is features
    assert sample.prediction is prediction
    assert sample.outcome is outcome


def test_backtest_sample_is_immutable():
    sample = create_sample()

    with pytest.raises(AttributeError):
        sample.prediction = create_prediction()


@pytest.mark.parametrize(
    "features",
    [
        None,
        123,
        True,
        "features",
        {},
    ],
)
def test_backtest_sample_rejects_invalid_features(features):
    with pytest.raises(TypeError):
        BacktestSample(
            features=features,
            prediction=create_prediction(),
            outcome=create_outcome(),
        )


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        123,
        True,
        "prediction",
        {},
    ],
)
def test_backtest_sample_rejects_invalid_prediction(prediction):
    with pytest.raises(TypeError):
        BacktestSample(
            features=create_feature_snapshot(),
            prediction=prediction,
            outcome=create_outcome(),
        )


@pytest.mark.parametrize(
    "outcome",
    [
        None,
        123,
        True,
        "outcome",
        {},
    ],
)
def test_backtest_sample_rejects_invalid_outcome(outcome):
    with pytest.raises(TypeError):
        BacktestSample(
            features=create_feature_snapshot(),
            prediction=create_prediction(),
            outcome=outcome,
        )


def test_backtest_sample_rejects_feature_prediction_symbol_mismatch():
    with pytest.raises(ValueError):
        create_sample(
            feature_snapshot=create_feature_snapshot(
                symbol="BTCUSDT",
            ),
        )


def test_backtest_sample_rejects_prediction_outcome_symbol_mismatch():
    with pytest.raises(ValueError):
        create_sample(
            outcome=create_outcome(
                symbol="BTCUSDT",
            ),
        )


def test_backtest_sample_rejects_feature_prediction_timestamp_mismatch():
    with pytest.raises(ValueError):
        create_sample(
            feature_snapshot=create_feature_snapshot(
                feature_timestamp=1_800_000_001_000,
            ),
        )


def test_backtest_sample_rejects_prediction_outcome_timestamp_mismatch():
    with pytest.raises(ValueError):
        create_sample(
            outcome=create_outcome(
                prediction_timestamp=1_800_000_001_000,
                evaluation_timestamp=1_800_000_301_000,
            ),
        )


def test_backtest_sample_rejects_reference_price_mismatch():
    with pytest.raises(ValueError):
        create_sample(
            outcome=create_outcome(
                reference_price=0.51,
            ),
        )


def test_backtest_sample_accepts_different_outcome_horizons():
    one_minute = create_sample(
        outcome=create_outcome(
            horizon_minutes=1,
            evaluation_timestamp=1_800_000_060_000,
        ),
    )
    thirty_minutes = create_sample(
        outcome=create_outcome(
            horizon_minutes=30,
            evaluation_timestamp=1_800_001_800_000,
        ),
    )

    assert one_minute.outcome.horizon_minutes == 1
    assert thirty_minutes.outcome.horizon_minutes == 30


def test_backtest_sample_preserves_future_outcome_separately_from_features():
    sample = create_sample()

    assert "future_return" not in sample.features.features
    assert sample.outcome.future_return == pytest.approx(0.05)
