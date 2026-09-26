import pytest

from backend.app.ml.model_comparison_dataset import (
    ModelComparisonDataset,
)
from backend.app.ml.model_comparison_sample import (
    ModelComparisonSample,
)


def create_sample(
    *,
    horizon_minutes: int = 15,
    traditional_direction_score: float = 0.60,
    ml_predicted_return: float = 0.012,
    observed_return: float = 0.008,
) -> ModelComparisonSample:
    return ModelComparisonSample(
        horizon_minutes=horizon_minutes,
        traditional_direction_score=traditional_direction_score,
        ml_predicted_return=ml_predicted_return,
        observed_return=observed_return,
    )


def test_model_comparison_dataset_stores_samples_as_tuple():
    samples = [
        create_sample(),
        create_sample(
            horizon_minutes=30,
            traditional_direction_score=-0.40,
            ml_predicted_return=-0.01,
            observed_return=-0.02,
        ),
    ]

    dataset = ModelComparisonDataset(
        samples=samples,
    )

    assert isinstance(
        dataset.samples,
        tuple,
    )
    assert dataset.samples == tuple(samples)


def test_model_comparison_dataset_accepts_tuple():
    samples = (
        create_sample(),
        create_sample(
            horizon_minutes=30,
        ),
    )

    dataset = ModelComparisonDataset(
        samples=samples,
    )

    assert dataset.samples == samples


def test_model_comparison_dataset_preserves_order():
    first = create_sample(
        horizon_minutes=5,
    )
    second = create_sample(
        horizon_minutes=30,
    )
    third = create_sample(
        horizon_minutes=15,
    )

    dataset = ModelComparisonDataset(
        samples=[
            first,
            second,
            third,
        ]
    )

    assert dataset.samples == (
        first,
        second,
        third,
    )


def test_model_comparison_dataset_preserves_duplicates():
    sample = create_sample()

    dataset = ModelComparisonDataset(
        samples=[
            sample,
            sample,
        ]
    )

    assert dataset.samples == (
        sample,
        sample,
    )


def test_model_comparison_dataset_preserves_multiple_horizons():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
            ),
            create_sample(
                horizon_minutes=15,
            ),
            create_sample(
                horizon_minutes=30,
            ),
        ]
    )

    assert tuple(
        sample.horizon_minutes
        for sample in dataset.samples
    ) == (
        5,
        15,
        30,
    )


def test_model_comparison_dataset_is_immutable():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(),
        ]
    )

    with pytest.raises(AttributeError):
        dataset.samples = ()


@pytest.mark.parametrize(
    "samples",
    [
        None,
        "invalid",
        123,
        True,
        {},
        set(),
    ],
)
def test_model_comparison_dataset_rejects_invalid_collection(
    samples,
):
    with pytest.raises(
        TypeError,
        match="samples must be a list or tuple",
    ):
        ModelComparisonDataset(
            samples=samples,
        )


@pytest.mark.parametrize(
    "samples",
    [
        [],
        (),
    ],
)
def test_model_comparison_dataset_rejects_empty_collection(
    samples,
):
    with pytest.raises(
        ValueError,
        match="samples must not be empty",
    ):
        ModelComparisonDataset(
            samples=samples,
        )


@pytest.mark.parametrize(
    "invalid_sample",
    [
        None,
        "invalid",
        123,
        True,
        {},
    ],
)
def test_model_comparison_dataset_rejects_invalid_sample(
    invalid_sample,
):
    with pytest.raises(
        TypeError,
        match=(
            "all samples must be ModelComparisonSample"
        ),
    ):
        ModelComparisonDataset(
            samples=[
                create_sample(),
                invalid_sample,
            ]
        )


def test_model_comparison_dataset_defensively_freezes_input_list():
    samples = [
        create_sample(),
    ]

    dataset = ModelComparisonDataset(
        samples=samples,
    )

    samples.append(
        create_sample(
            horizon_minutes=30,
        )
    )

    assert len(dataset.samples) == 1
