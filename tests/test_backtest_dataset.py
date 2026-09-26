import pytest

from backend.app.backtesting.backtest_dataset import BacktestDataset
from backend.app.backtesting.backtest_sample import BacktestSample
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


def test_backtest_dataset_preserves_samples():
    first = create_sample()
    second = create_sample(
        timestamp=1_800_000_300_000,
        reference_price=0.525,
        evaluation_price=0.53,
    )

    dataset = BacktestDataset(
        samples=[first, second],
    )

    assert dataset.samples == (first, second)


def test_backtest_dataset_exposes_samples_as_tuple():
    dataset = BacktestDataset(
        samples=[create_sample()],
    )

    assert isinstance(dataset.samples, tuple)


def test_backtest_dataset_defensively_copies_sample_list():
    first = create_sample()
    original = [first]

    dataset = BacktestDataset(
        samples=original,
    )

    original.append(
        create_sample(
            timestamp=1_800_000_300_000,
        )
    )

    assert dataset.samples == (first,)


def test_backtest_dataset_is_immutable():
    dataset = BacktestDataset(
        samples=[create_sample()],
    )

    with pytest.raises(AttributeError):
        dataset.samples = (create_sample(),)


@pytest.mark.parametrize(
    "samples",
    [
        None,
        123,
        True,
        "samples",
        {},
        set(),
    ],
)
def test_backtest_dataset_rejects_invalid_collection(samples):
    with pytest.raises(TypeError):
        BacktestDataset(samples=samples)


@pytest.mark.parametrize(
    "samples",
    [
        [],
        (),
    ],
)
def test_backtest_dataset_rejects_empty_collection(samples):
    with pytest.raises(ValueError):
        BacktestDataset(samples=samples)


@pytest.mark.parametrize(
    "invalid_sample",
    [
        None,
        123,
        True,
        "sample",
        {},
    ],
)
def test_backtest_dataset_rejects_invalid_sample(
    invalid_sample,
):
    with pytest.raises(TypeError):
        BacktestDataset(
            samples=[
                create_sample(),
                invalid_sample,
            ],
        )


def test_backtest_dataset_accepts_tuple_input():
    first = create_sample()
    second = create_sample(
        timestamp=1_800_000_300_000,
    )

    dataset = BacktestDataset(
        samples=(first, second),
    )

    assert dataset.samples == (first, second)


def test_backtest_dataset_preserves_input_order():
    later = create_sample(
        timestamp=1_800_000_300_000,
    )
    earlier = create_sample(
        timestamp=1_800_000_000_000,
    )

    dataset = BacktestDataset(
        samples=[later, earlier],
    )

    assert dataset.samples == (later, earlier)


def test_backtest_dataset_accepts_multiple_symbols():
    fet = create_sample(
        symbol="FETUSDT",
    )
    btc = create_sample(
        symbol="BTCUSDT",
        reference_price=60_000.0,
        evaluation_price=60_500.0,
    )

    dataset = BacktestDataset(
        samples=[fet, btc],
    )

    assert dataset.samples == (fet, btc)


def test_backtest_dataset_accepts_multiple_horizons():
    one_minute = create_sample(
        horizon_minutes=1,
    )
    thirty_minutes = create_sample(
        timestamp=1_800_000_300_000,
        horizon_minutes=30,
    )

    dataset = BacktestDataset(
        samples=[
            one_minute,
            thirty_minutes,
        ],
    )

    assert (
        dataset.samples[0].outcome.horizon_minutes
        == 1
    )
    assert (
        dataset.samples[1].outcome.horizon_minutes
        == 30
    )


def test_backtest_dataset_preserves_repeated_samples():
    sample = create_sample()

    dataset = BacktestDataset(
        samples=[sample, sample],
    )

    assert dataset.samples == (sample, sample)
