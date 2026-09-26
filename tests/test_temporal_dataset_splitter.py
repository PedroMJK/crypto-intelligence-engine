import pytest

from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.ml.temporal_dataset_splitter import (
    TemporalDatasetSplitter,
)
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_sample(
    feature_timestamp: int,
    *,
    symbol: str = "FETUSDT",
    horizon_minutes: int = 15,
    target: float = 0.01,
) -> MLSample:
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


def create_dataset(
    sample_count: int = 10,
) -> MLDataset:
    base_timestamp = 1_800_000_000_000

    samples = [
        create_sample(
            base_timestamp + index * 60_000,
        )
        for index in range(sample_count)
    ]

    return MLDataset(samples=samples)


def test_split_returns_expected_partition_sizes():
    dataset = create_dataset()

    result = TemporalDatasetSplitter.split(
        dataset=dataset,
        train_ratio=0.60,
        validation_ratio=0.20,
        test_ratio=0.20,
    )

    assert len(result.train.samples) == 6
    assert len(result.validation.samples) == 2
    assert len(result.test.samples) == 2


def test_split_preserves_sample_instances():
    dataset = create_dataset()

    result = TemporalDatasetSplitter.split(
        dataset=dataset,
        train_ratio=0.60,
        validation_ratio=0.20,
        test_ratio=0.20,
    )

    assert result.train.samples == dataset.samples[:6]
    assert result.validation.samples == dataset.samples[6:8]
    assert result.test.samples == dataset.samples[8:]


def test_split_preserves_temporal_boundaries():
    dataset = create_dataset()

    result = TemporalDatasetSplitter.split(
        dataset=dataset,
        train_ratio=0.60,
        validation_ratio=0.20,
        test_ratio=0.20,
    )

    train_last_timestamp = (
        result.train.samples[-1].features.feature_timestamp
    )
    validation_first_timestamp = (
        result.validation.samples[0].features.feature_timestamp
    )
    validation_last_timestamp = (
        result.validation.samples[-1].features.feature_timestamp
    )
    test_first_timestamp = (
        result.test.samples[0].features.feature_timestamp
    )

    assert train_last_timestamp < validation_first_timestamp
    assert validation_last_timestamp < test_first_timestamp


def test_split_does_not_modify_original_dataset():
    dataset = create_dataset()
    original_samples = dataset.samples

    TemporalDatasetSplitter.split(
        dataset=dataset,
        train_ratio=0.60,
        validation_ratio=0.20,
        test_ratio=0.20,
    )

    assert dataset.samples is original_samples


def test_split_rejects_dataset_out_of_temporal_order():
    dataset = MLDataset(
        samples=[
            create_sample(1_800_000_000_000),
            create_sample(1_800_000_120_000),
            create_sample(1_800_000_060_000),
            create_sample(1_800_000_180_000),
        ]
    )

    with pytest.raises(
        ValueError,
        match="dataset samples must be in chronological order",
    ):
        TemporalDatasetSplitter.split(
            dataset=dataset,
            train_ratio=0.50,
            validation_ratio=0.25,
            test_ratio=0.25,
        )


@pytest.mark.parametrize(
    "invalid_dataset",
    [
        None,
        123,
        True,
        "dataset",
        {},
        [],
        (),
    ],
)
def test_split_rejects_invalid_dataset(
    invalid_dataset,
):
    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        TemporalDatasetSplitter.split(
            dataset=invalid_dataset,
            train_ratio=0.60,
            validation_ratio=0.20,
            test_ratio=0.20,
        )


@pytest.mark.parametrize(
    "ratio_name",
    [
        "train_ratio",
        "validation_ratio",
        "test_ratio",
    ],
)
@pytest.mark.parametrize(
    "invalid_ratio",
    [
        None,
        "0.20",
        True,
        [],
        {},
    ],
)
def test_split_rejects_non_numeric_ratio(
    ratio_name,
    invalid_ratio,
):
    ratios = {
        "train_ratio": 0.60,
        "validation_ratio": 0.20,
        "test_ratio": 0.20,
    }
    ratios[ratio_name] = invalid_ratio

    with pytest.raises(TypeError):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(),
            **ratios,
        )


@pytest.mark.parametrize(
    "ratio_name",
    [
        "train_ratio",
        "validation_ratio",
        "test_ratio",
    ],
)
@pytest.mark.parametrize(
    "invalid_ratio",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_split_rejects_non_finite_ratio(
    ratio_name,
    invalid_ratio,
):
    ratios = {
        "train_ratio": 0.60,
        "validation_ratio": 0.20,
        "test_ratio": 0.20,
    }
    ratios[ratio_name] = invalid_ratio

    with pytest.raises(ValueError):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(),
            **ratios,
        )


@pytest.mark.parametrize(
    "ratio_name",
    [
        "train_ratio",
        "validation_ratio",
        "test_ratio",
    ],
)
@pytest.mark.parametrize(
    "invalid_ratio",
    [
        0.0,
        -0.10,
    ],
)
def test_split_rejects_non_positive_ratio(
    ratio_name,
    invalid_ratio,
):
    ratios = {
        "train_ratio": 0.60,
        "validation_ratio": 0.20,
        "test_ratio": 0.20,
    }
    ratios[ratio_name] = invalid_ratio

    with pytest.raises(ValueError):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(),
            **ratios,
        )


@pytest.mark.parametrize(
    (
        "train_ratio",
        "validation_ratio",
        "test_ratio",
    ),
    [
        (0.50, 0.20, 0.20),
        (0.70, 0.20, 0.20),
    ],
)
def test_split_rejects_ratios_that_do_not_sum_to_one(
    train_ratio,
    validation_ratio,
    test_ratio,
):
    with pytest.raises(
        ValueError,
        match="ratios must sum to one",
    ):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(),
            train_ratio=train_ratio,
            validation_ratio=validation_ratio,
            test_ratio=test_ratio,
        )


def test_split_rejects_ratios_that_create_empty_train():
    with pytest.raises(
        ValueError,
        match="split partitions must not be empty",
    ):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(
                sample_count=3,
            ),
            train_ratio=0.10,
            validation_ratio=0.40,
            test_ratio=0.50,
        )


def test_split_rejects_ratios_that_create_empty_validation():
    with pytest.raises(
        ValueError,
        match="split partitions must not be empty",
    ):
        TemporalDatasetSplitter.split(
            dataset=create_dataset(
                sample_count=3,
            ),
            train_ratio=0.50,
            validation_ratio=0.10,
            test_ratio=0.40,
        )
def test_split_allows_equal_timestamps_within_partition():
    dataset = MLDataset(
        samples=[
            create_sample(1_800_000_000_000),
            create_sample(1_800_000_000_000),
            create_sample(1_800_000_060_000),
            create_sample(1_800_000_120_000),
            create_sample(1_800_000_180_000),
            create_sample(1_800_000_240_000),
        ]
    )

    result = TemporalDatasetSplitter.split(
        dataset=dataset,
        train_ratio=0.50,
        validation_ratio=0.25,
        test_ratio=0.25,
    )

    assert (
        result.train.samples[0].features.feature_timestamp
        == result.train.samples[1].features.feature_timestamp
    )


def test_split_rejects_equal_timestamp_across_train_validation_boundary():
    dataset = MLDataset(
        samples=[
            create_sample(1_800_000_000_000),
            create_sample(1_800_000_060_000),
            create_sample(1_800_000_120_000),
            create_sample(1_800_000_120_000),
            create_sample(1_800_000_180_000),
            create_sample(1_800_000_240_000),
            create_sample(1_800_000_300_000),
            create_sample(1_800_000_360_000),
        ]
    )

    with pytest.raises(
        ValueError,
        match="split boundaries must be strictly chronological",
    ):
        TemporalDatasetSplitter.split(
            dataset=dataset,
            train_ratio=0.50,
            validation_ratio=0.25,
            test_ratio=0.25,
        )
def test_split_rejects_equal_timestamp_across_train_validation_boundary():
    dataset = MLDataset(
        samples=[
            create_sample(1_800_000_000_000),
            create_sample(1_800_000_060_000),
            create_sample(1_800_000_120_000),
            create_sample(1_800_000_180_000),
            create_sample(1_800_000_180_000),
            create_sample(1_800_000_240_000),
            create_sample(1_800_000_300_000),
            create_sample(1_800_000_360_000),
        ]
    )

    with pytest.raises(
        ValueError,
        match="split boundaries must be strictly chronological",
    ):
        TemporalDatasetSplitter.split(
            dataset=dataset,
            train_ratio=0.50,
            validation_ratio=0.25,
            test_ratio=0.25,
        )
