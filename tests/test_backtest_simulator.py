from unittest.mock import patch

import pytest

from backend.app.backtesting.backtest_dataset import BacktestDataset
from backend.app.backtesting.backtest_sample import BacktestSample
from backend.app.backtesting.backtest_simulator import BacktestSimulator
from backend.app.backtesting.look_ahead_guard import LookAheadGuard
from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_metrics import PredictionMetrics
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


def create_sample(
    *,
    symbol="FETUSDT",
    timestamp=1_800_000_000_000,
    reference_price=0.50,
    direction_score=0.60,
    horizon_minutes=5,
    evaluation_price=0.525,
):
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
        evaluation_timestamp=(
            timestamp
            + horizon_minutes * 60_000
        ),
        evaluation_price=evaluation_price,
    )

    return BacktestSample(
        features=features,
        prediction=prediction,
        outcome=outcome,
    )


def test_backtest_simulator_returns_tuple():
    dataset = BacktestDataset(
        samples=[create_sample()],
    )

    result = BacktestSimulator.run(dataset)

    assert isinstance(result, tuple)


def test_backtest_simulator_returns_prediction_metrics():
    dataset = BacktestDataset(
        samples=[create_sample()],
    )

    result = BacktestSimulator.run(dataset)

    assert len(result) == 1
    assert isinstance(result[0], PredictionMetrics)


def test_backtest_simulator_calculates_expected_metrics():
    dataset = BacktestDataset(
        samples=[
            create_sample(
                direction_score=0.60,
                reference_price=0.50,
                evaluation_price=0.525,
            ),
        ],
    )

    result = BacktestSimulator.run(dataset)

    metrics = result[0]

    assert metrics.symbol == "FETUSDT"
    assert metrics.prediction_timestamp == 1_800_000_000_000
    assert metrics.horizon_minutes == 5
    assert metrics.direction_score == pytest.approx(0.60)
    assert metrics.future_return == pytest.approx(0.05)
    assert metrics.absolute_return == pytest.approx(0.05)
    assert metrics.directional_alignment == pytest.approx(0.03)


def test_backtest_simulator_preserves_sample_order():
    first = create_sample(
        timestamp=1_800_000_000_000,
        direction_score=0.60,
    )
    second = create_sample(
        timestamp=1_800_000_300_000,
        direction_score=-0.40,
    )

    dataset = BacktestDataset(
        samples=[first, second],
    )

    result = BacktestSimulator.run(dataset)

    assert result[0].prediction_timestamp == (
        first.prediction.prediction_timestamp
    )
    assert result[1].prediction_timestamp == (
        second.prediction.prediction_timestamp
    )


def test_backtest_simulator_evaluates_all_samples():
    dataset = BacktestDataset(
        samples=[
            create_sample(
                timestamp=1_800_000_000_000,
            ),
            create_sample(
                timestamp=1_800_000_300_000,
            ),
            create_sample(
                timestamp=1_800_000_600_000,
            ),
        ],
    )

    result = BacktestSimulator.run(dataset)

    assert len(result) == 3


def test_backtest_simulator_accepts_multiple_symbols():
    dataset = BacktestDataset(
        samples=[
            create_sample(
                symbol="FETUSDT",
            ),
            create_sample(
                symbol="BTCUSDT",
                timestamp=1_800_000_300_000,
                reference_price=60_000.0,
                evaluation_price=60_600.0,
            ),
        ],
    )

    result = BacktestSimulator.run(dataset)

    assert result[0].symbol == "FETUSDT"
    assert result[1].symbol == "BTCUSDT"


def test_backtest_simulator_accepts_multiple_horizons():
    dataset = BacktestDataset(
        samples=[
            create_sample(
                horizon_minutes=1,
                evaluation_price=0.51,
            ),
            create_sample(
                timestamp=1_800_000_300_000,
                horizon_minutes=30,
                evaluation_price=0.54,
            ),
        ],
    )

    result = BacktestSimulator.run(dataset)

    assert result[0].horizon_minutes == 1
    assert result[1].horizon_minutes == 30


def test_backtest_simulator_preserves_repeated_samples():
    sample = create_sample()

    dataset = BacktestDataset(
        samples=[sample, sample],
    )

    result = BacktestSimulator.run(dataset)

    assert len(result) == 2
    assert result[0] == result[1]


@pytest.mark.parametrize(
    "dataset",
    [
        None,
        123,
        True,
        "dataset",
        [],
        (),
        {},
    ],
)
def test_backtest_simulator_rejects_invalid_dataset(dataset):
    with pytest.raises(TypeError):
        BacktestSimulator.run(dataset)


def test_backtest_simulator_does_not_modify_dataset():
    first = create_sample()
    second = create_sample(
        timestamp=1_800_000_300_000,
    )

    dataset = BacktestDataset(
        samples=[first, second],
    )
    original_samples = dataset.samples

    BacktestSimulator.run(dataset)

    assert dataset.samples == original_samples
    assert dataset.samples[0] is first
    assert dataset.samples[1] is second


def test_backtest_simulator_validates_each_sample_with_look_ahead_guard():
    first = create_sample(
        timestamp=1_800_000_000_000,
    )
    second = create_sample(
        timestamp=1_800_000_300_000,
    )

    dataset = BacktestDataset(
        samples=[first, second],
    )

    with patch.object(
        LookAheadGuard,
        "validate",
        wraps=LookAheadGuard.validate,
    ) as validate:
        BacktestSimulator.run(dataset)

    assert validate.call_count == 2
    validate.assert_any_call(first)
    validate.assert_any_call(second)
