import pytest

from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_dataset_preparer import MLDatasetPreparer
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_outcome import PredictionOutcome


def create_feature_snapshot(
    *,
    symbol="FETUSDT",
    feature_timestamp=1_800_000_000_000,
):
    return FeatureSnapshot(
        symbol=symbol,
        feature_timestamp=feature_timestamp,
        features={
            "technical_score": 0.60,
            "flow_score": -0.20,
            "momentum_score": 0.40,
            "structure_score": 0.10,
            "direction_score": 0.35,
            "volume_score": 0.80,
            "confidence": 0.70,
            "contradiction": 0.15,
        },
    )


def create_prediction_outcome(
    *,
    symbol="FETUSDT",
    prediction_timestamp=1_800_000_000_000,
    reference_price=0.40,
    horizon_minutes=15,
    evaluation_timestamp=1_800_000_900_000,
    evaluation_price=0.42,
):
    return PredictionOutcome(
        symbol=symbol,
        prediction_timestamp=prediction_timestamp,
        reference_price=reference_price,
        horizon_minutes=horizon_minutes,
        evaluation_timestamp=evaluation_timestamp,
        evaluation_price=evaluation_price,
    )


def test_ml_dataset_preparer_returns_ml_sample():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome()

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert isinstance(result, MLSample)


def test_ml_dataset_preparer_preserves_feature_snapshot():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome()

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert result.features is features


def test_ml_dataset_preparer_uses_outcome_horizon():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome(
        horizon_minutes=30,
        evaluation_timestamp=1_800_001_800_000,
    )

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert result.horizon_minutes == 30


def test_ml_dataset_preparer_uses_future_return_as_target():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome(
        reference_price=0.40,
        evaluation_price=0.42,
    )

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert result.target == pytest.approx(0.05)
    assert result.target == outcome.future_return


def test_ml_dataset_preparer_uses_evaluation_timestamp_as_target_timestamp():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome(
        evaluation_timestamp=1_800_001_200_000,
    )

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert (
        result.target_timestamp
        == outcome.evaluation_timestamp
    )


def test_ml_dataset_preparer_preserves_negative_future_return():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome(
        reference_price=0.40,
        evaluation_price=0.36,
    )

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert result.target == pytest.approx(-0.10)


def test_ml_dataset_preparer_preserves_zero_future_return():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome(
        reference_price=0.40,
        evaluation_price=0.40,
    )

    result = MLDatasetPreparer.prepare_sample(
        features,
        outcome,
    )

    assert result.target == 0.0


def test_ml_dataset_preparer_rejects_symbol_mismatch():
    features = create_feature_snapshot(
        symbol="FETUSDT",
    )
    outcome = create_prediction_outcome(
        symbol="BTCUSDT",
    )

    with pytest.raises(ValueError):
        MLDatasetPreparer.prepare_sample(
            features,
            outcome,
        )


def test_ml_dataset_preparer_rejects_timestamp_mismatch():
    features = create_feature_snapshot(
        feature_timestamp=1_800_000_000_000,
    )
    outcome = create_prediction_outcome(
        prediction_timestamp=1_800_000_300_000,
        evaluation_timestamp=1_800_001_200_000,
    )

    with pytest.raises(ValueError):
        MLDatasetPreparer.prepare_sample(
            features,
            outcome,
        )


@pytest.mark.parametrize(
    "features",
    [
        None,
        123,
        True,
        "features",
        {},
        [],
        (),
    ],
)
def test_ml_dataset_preparer_rejects_invalid_feature_snapshot(
    features,
):
    with pytest.raises(TypeError):
        MLDatasetPreparer.prepare_sample(
            features,
            create_prediction_outcome(),
        )


@pytest.mark.parametrize(
    "outcome",
    [
        None,
        123,
        True,
        "outcome",
        {},
        [],
        (),
    ],
)
def test_ml_dataset_preparer_rejects_invalid_prediction_outcome(
    outcome,
):
    with pytest.raises(TypeError):
        MLDatasetPreparer.prepare_sample(
            create_feature_snapshot(),
            outcome,
        )


def test_ml_dataset_preparer_prepares_dataset():
    first_features = create_feature_snapshot()
    first_outcome = create_prediction_outcome()

    second_features = create_feature_snapshot(
        symbol="BTCUSDT",
        feature_timestamp=1_800_000_300_000,
    )
    second_outcome = create_prediction_outcome(
        symbol="BTCUSDT",
        prediction_timestamp=1_800_000_300_000,
        reference_price=50_000.0,
        horizon_minutes=30,
        evaluation_timestamp=1_800_002_100_000,
        evaluation_price=51_000.0,
    )

    dataset = MLDatasetPreparer.prepare_dataset(
        [
            (first_features, first_outcome),
            (second_features, second_outcome),
        ]
    )

    assert isinstance(dataset, MLDataset)
    assert len(dataset.samples) == 2


def test_ml_dataset_preparer_preserves_dataset_order():
    first_features = create_feature_snapshot(
        symbol="BTCUSDT",
    )
    first_outcome = create_prediction_outcome(
        symbol="BTCUSDT",
    )

    second_features = create_feature_snapshot(
        symbol="FETUSDT",
        feature_timestamp=1_800_000_300_000,
    )
    second_outcome = create_prediction_outcome(
        symbol="FETUSDT",
        prediction_timestamp=1_800_000_300_000,
        evaluation_timestamp=1_800_001_200_000,
    )

    dataset = MLDatasetPreparer.prepare_dataset(
        [
            (first_features, first_outcome),
            (second_features, second_outcome),
        ]
    )

    assert dataset.samples[0].features is first_features
    assert dataset.samples[1].features is second_features


def test_ml_dataset_preparer_preserves_multiple_horizons():
    first_features = create_feature_snapshot()
    first_outcome = create_prediction_outcome(
        horizon_minutes=5,
        evaluation_timestamp=1_800_000_300_000,
    )

    second_features = create_feature_snapshot(
        feature_timestamp=1_800_000_300_000,
    )
    second_outcome = create_prediction_outcome(
        prediction_timestamp=1_800_000_300_000,
        horizon_minutes=30,
        evaluation_timestamp=1_800_002_100_000,
    )

    dataset = MLDatasetPreparer.prepare_dataset(
        [
            (first_features, first_outcome),
            (second_features, second_outcome),
        ]
    )

    assert tuple(
        sample.horizon_minutes
        for sample in dataset.samples
    ) == (
        5,
        30,
    )


def test_ml_dataset_preparer_preserves_duplicate_pairs():
    features = create_feature_snapshot()
    outcome = create_prediction_outcome()

    dataset = MLDatasetPreparer.prepare_dataset(
        [
            (features, outcome),
            (features, outcome),
        ]
    )

    assert len(dataset.samples) == 2
    assert dataset.samples[0].features is features
    assert dataset.samples[1].features is features


@pytest.mark.parametrize(
    "pairs",
    [
        None,
        123,
        True,
        "pairs",
        {},
        set(),
    ],
)
def test_ml_dataset_preparer_rejects_invalid_pair_collection(
    pairs,
):
    with pytest.raises(TypeError):
        MLDatasetPreparer.prepare_dataset(pairs)


@pytest.mark.parametrize(
    "pairs",
    [
        [],
        (),
    ],
)
def test_ml_dataset_preparer_rejects_empty_pair_collection(
    pairs,
):
    with pytest.raises(ValueError):
        MLDatasetPreparer.prepare_dataset(pairs)


@pytest.mark.parametrize(
    "invalid_pair",
    [
        None,
        123,
        True,
        "pair",
        {},
        [],
        (),
        (create_feature_snapshot(),),
        (
            create_feature_snapshot(),
            create_prediction_outcome(),
            create_prediction_outcome(),
        ),
    ],
)
def test_ml_dataset_preparer_rejects_invalid_pair(
    invalid_pair,
):
    with pytest.raises(TypeError):
        MLDatasetPreparer.prepare_dataset(
            [invalid_pair]
        )


def test_ml_dataset_preparer_reuses_sample_validation():
    features = create_feature_snapshot(
        symbol="FETUSDT",
    )
    outcome = create_prediction_outcome(
        symbol="BTCUSDT",
    )

    with pytest.raises(ValueError):
        MLDatasetPreparer.prepare_dataset(
            [
                (features, outcome),
            ]
        )
