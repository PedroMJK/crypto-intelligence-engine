import pytest

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.calibration_sample import CalibrationSample


def create_sample(
    *,
    horizon_minutes: int = 15,
    predicted_return: float = 0.012,
    observed_return: float = 0.008,
) -> CalibrationSample:
    return CalibrationSample(
        horizon_minutes=horizon_minutes,
        predicted_return=predicted_return,
        observed_return=observed_return,
    )


def test_calibration_dataset_stores_samples_as_tuple():
    samples = [
        create_sample(),
        create_sample(
            horizon_minutes=30,
            predicted_return=-0.010,
            observed_return=-0.006,
        ),
    ]

    dataset = CalibrationDataset(
        samples=samples,
    )

    assert isinstance(
        dataset.samples,
        tuple,
    )
    assert dataset.samples == tuple(samples)


def test_calibration_dataset_accepts_tuple():
    samples = (
        create_sample(),
        create_sample(
            horizon_minutes=30,
        ),
    )

    dataset = CalibrationDataset(
        samples=samples,
    )

    assert dataset.samples == samples


def test_calibration_dataset_preserves_sample_order():
    first = create_sample(
        horizon_minutes=5,
        predicted_return=0.01,
    )
    second = create_sample(
        horizon_minutes=30,
        predicted_return=-0.02,
    )
    third = create_sample(
        horizon_minutes=5,
        predicted_return=0.03,
    )

    dataset = CalibrationDataset(
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


def test_calibration_dataset_preserves_duplicate_samples():
    sample = create_sample()

    dataset = CalibrationDataset(
        samples=[
            sample,
            sample,
        ]
    )

    assert dataset.samples == (
        sample,
        sample,
    )


def test_calibration_dataset_preserves_multiple_horizons():
    dataset = CalibrationDataset(
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


def test_calibration_dataset_is_immutable():
    dataset = CalibrationDataset(
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
def test_calibration_dataset_rejects_invalid_collection(
    samples,
):
    with pytest.raises(
        TypeError,
        match="samples must be a list or tuple",
    ):
        CalibrationDataset(
            samples=samples,
        )


@pytest.mark.parametrize(
    "samples",
    [
        [],
        (),
    ],
)
def test_calibration_dataset_rejects_empty_collection(
    samples,
):
    with pytest.raises(
        ValueError,
        match="samples must not be empty",
    ):
        CalibrationDataset(
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
def test_calibration_dataset_rejects_invalid_sample(
    invalid_sample,
):
    with pytest.raises(
        TypeError,
        match="all samples must be CalibrationSample",
    ):
        CalibrationDataset(
            samples=[
                create_sample(),
                invalid_sample,
            ]
        )


def test_calibration_dataset_defensively_freezes_input_list():
    samples = [
        create_sample(),
    ]

    dataset = CalibrationDataset(
        samples=samples,
    )

    samples.append(
        create_sample(
            horizon_minutes=30,
        )
    )

    assert len(dataset.samples) == 1
