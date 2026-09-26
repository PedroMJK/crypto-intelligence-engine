from dataclasses import FrozenInstanceError

import pytest

from backend.app.ml.dataset_split import DatasetSplit
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_ml_dataset(
    *,
    symbol="FETUSDT",
    feature_timestamp=1_800_000_000_000,
):
    sample = MLSample(
        features=FeatureSnapshot(
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
        ),
        horizon_minutes=15,
        target=0.05,
        target_timestamp=(
            feature_timestamp
            + 15 * 60_000
        ),
    )

    return MLDataset(
        samples=[sample],
    )


def test_dataset_split_preserves_train_dataset():
    train = create_ml_dataset()
    validation = create_ml_dataset(
        feature_timestamp=1_800_000_300_000,
    )
    test = create_ml_dataset(
        feature_timestamp=1_800_000_600_000,
    )

    split = DatasetSplit(
        train=train,
        validation=validation,
        test=test,
    )

    assert split.train is train


def test_dataset_split_preserves_validation_dataset():
    train = create_ml_dataset()
    validation = create_ml_dataset(
        feature_timestamp=1_800_000_300_000,
    )
    test = create_ml_dataset(
        feature_timestamp=1_800_000_600_000,
    )

    split = DatasetSplit(
        train=train,
        validation=validation,
        test=test,
    )

    assert split.validation is validation


def test_dataset_split_preserves_test_dataset():
    train = create_ml_dataset()
    validation = create_ml_dataset(
        feature_timestamp=1_800_000_300_000,
    )
    test = create_ml_dataset(
        feature_timestamp=1_800_000_600_000,
    )

    split = DatasetSplit(
        train=train,
        validation=validation,
        test=test,
    )

    assert split.test is test


@pytest.mark.parametrize(
    "invalid_train",
    [
        None,
        123,
        True,
        "train",
        {},
        [],
        (),
    ],
)
def test_dataset_split_rejects_invalid_train(
    invalid_train,
):
    with pytest.raises(TypeError):
        DatasetSplit(
            train=invalid_train,
            validation=create_ml_dataset(
                feature_timestamp=1_800_000_300_000,
            ),
            test=create_ml_dataset(
                feature_timestamp=1_800_000_600_000,
            ),
        )


@pytest.mark.parametrize(
    "invalid_validation",
    [
        None,
        123,
        True,
        "validation",
        {},
        [],
        (),
    ],
)
def test_dataset_split_rejects_invalid_validation(
    invalid_validation,
):
    with pytest.raises(TypeError):
        DatasetSplit(
            train=create_ml_dataset(),
            validation=invalid_validation,
            test=create_ml_dataset(
                feature_timestamp=1_800_000_600_000,
            ),
        )


@pytest.mark.parametrize(
    "invalid_test",
    [
        None,
        123,
        True,
        "test",
        {},
        [],
        (),
    ],
)
def test_dataset_split_rejects_invalid_test(
    invalid_test,
):
    with pytest.raises(TypeError):
        DatasetSplit(
            train=create_ml_dataset(),
            validation=create_ml_dataset(
                feature_timestamp=1_800_000_300_000,
            ),
            test=invalid_test,
        )


def test_dataset_split_is_frozen():
    split = DatasetSplit(
        train=create_ml_dataset(),
        validation=create_ml_dataset(
            feature_timestamp=1_800_000_300_000,
        ),
        test=create_ml_dataset(
            feature_timestamp=1_800_000_600_000,
        ),
    )

    with pytest.raises(FrozenInstanceError):
        split.train = create_ml_dataset()
