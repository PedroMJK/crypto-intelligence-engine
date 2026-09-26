from dataclasses import FrozenInstanceError

import pytest

from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_ml_sample(
    *,
    symbol="FETUSDT",
    feature_timestamp=1_800_000_000_000,
    horizon_minutes=15,
    target=0.05,
):
    return MLSample(
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
        horizon_minutes=horizon_minutes,
        target=target,
    )


def test_ml_dataset_accepts_list_of_samples():
    samples = [
        create_ml_sample(),
        create_ml_sample(
            feature_timestamp=1_800_000_300_000,
        ),
    ]

    dataset = MLDataset(samples=samples)

    assert len(dataset.samples) == 2


def test_ml_dataset_accepts_tuple_of_samples():
    samples = (
        create_ml_sample(),
        create_ml_sample(
            feature_timestamp=1_800_000_300_000,
        ),
    )

    dataset = MLDataset(samples=samples)

    assert len(dataset.samples) == 2


def test_ml_dataset_freezes_samples_as_tuple():
    samples = [
        create_ml_sample(),
        create_ml_sample(
            feature_timestamp=1_800_000_300_000,
        ),
    ]

    dataset = MLDataset(samples=samples)

    assert isinstance(dataset.samples, tuple)


def test_ml_dataset_preserves_sample_instances():
    first = create_ml_sample()
    second = create_ml_sample(
        feature_timestamp=1_800_000_300_000,
    )

    dataset = MLDataset(
        samples=[first, second],
    )

    assert dataset.samples[0] is first
    assert dataset.samples[1] is second


def test_ml_dataset_preserves_sample_order():
    first = create_ml_sample(
        symbol="BTCUSDT",
        feature_timestamp=1_800_000_600_000,
    )
    second = create_ml_sample(
        symbol="FETUSDT",
        feature_timestamp=1_800_000_000_000,
    )
    third = create_ml_sample(
        symbol="ETHUSDT",
        feature_timestamp=1_800_000_300_000,
    )

    dataset = MLDataset(
        samples=[
            first,
            second,
            third,
        ],
    )

    assert dataset.samples == (
        first,
        second,
        third,
    )


def test_ml_dataset_preserves_duplicate_samples():
    sample = create_ml_sample()

    dataset = MLDataset(
        samples=[
            sample,
            sample,
        ],
    )

    assert dataset.samples == (
        sample,
        sample,
    )


def test_ml_dataset_accepts_multiple_symbols():
    dataset = MLDataset(
        samples=[
            create_ml_sample(
                symbol="FETUSDT",
            ),
            create_ml_sample(
                symbol="BTCUSDT",
                feature_timestamp=1_800_000_300_000,
            ),
        ],
    )

    assert tuple(
        sample.features.symbol
        for sample in dataset.samples
    ) == (
        "FETUSDT",
        "BTCUSDT",
    )


def test_ml_dataset_accepts_multiple_horizons():
    dataset = MLDataset(
        samples=[
            create_ml_sample(
                horizon_minutes=5,
            ),
            create_ml_sample(
                feature_timestamp=1_800_000_300_000,
                horizon_minutes=30,
            ),
        ],
    )

    assert tuple(
        sample.horizon_minutes
        for sample in dataset.samples
    ) == (
        5,
        30,
    )


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
def test_ml_dataset_rejects_invalid_collection(
    samples,
):
    with pytest.raises(TypeError):
        MLDataset(samples=samples)


@pytest.mark.parametrize(
    "samples",
    [
        [],
        (),
    ],
)
def test_ml_dataset_rejects_empty_collection(
    samples,
):
    with pytest.raises(ValueError):
        MLDataset(samples=samples)


@pytest.mark.parametrize(
    "invalid_sample",
    [
        None,
        123,
        True,
        "sample",
        {},
        [],
        (),
    ],
)
def test_ml_dataset_rejects_invalid_sample(
    invalid_sample,
):
    with pytest.raises(TypeError):
        MLDataset(
            samples=[
                create_ml_sample(),
                invalid_sample,
            ],
        )


def test_ml_dataset_is_frozen():
    dataset = MLDataset(
        samples=[
            create_ml_sample(),
        ],
    )

    with pytest.raises(FrozenInstanceError):
        dataset.samples = ()
