import pytest

from backend.app.ml.mean_return_baseline import MeanReturnBaseline
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_sample(
    *,
    feature_timestamp: int,
    horizon_minutes: int,
    target: float,
) -> MLSample:
    return MLSample(
        features=FeatureSnapshot(
            symbol="FETUSDT",
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
        target_timestamp=(
            feature_timestamp
            + horizon_minutes * 60_000
        ),
    )


def test_mean_return_baseline_predicts_training_mean():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=15,
                target=0.01,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=15,
                target=0.03,
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=15,
                target=0.05,
            ),
        ]
    )

    baseline = MeanReturnBaseline()

    baseline.fit(dataset)

    prediction = baseline.predict(
        horizon_minutes=15,
    )

    assert prediction == pytest.approx(0.03)


def test_mean_return_baseline_learns_independent_mean_per_horizon():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.03,
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=30,
                target=-0.02,
            ),
            create_sample(
                feature_timestamp=1_800_004_800_000,
                horizon_minutes=30,
                target=-0.04,
            ),
        ]
    )

    baseline = MeanReturnBaseline()

    baseline.fit(dataset)

    five_minute_prediction = baseline.predict(
        horizon_minutes=5,
    )
    thirty_minute_prediction = baseline.predict(
        horizon_minutes=30,
    )

    assert five_minute_prediction == pytest.approx(
        0.02
    )
    assert thirty_minute_prediction == pytest.approx(
        -0.03
    )


@pytest.mark.parametrize(
    "dataset",
    [
        None,
        [],
        (),
        "invalid",
        123,
        True,
    ],
)
def test_mean_return_baseline_rejects_invalid_training_dataset(
    dataset,
):
    baseline = MeanReturnBaseline()

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        baseline.fit(dataset)


def test_mean_return_baseline_rejects_prediction_before_fit():
    baseline = MeanReturnBaseline()

    with pytest.raises(
        RuntimeError,
        match="baseline must be fitted before prediction",
    ):
        baseline.predict(
            horizon_minutes=15,
        )


def test_mean_return_baseline_rejects_unseen_horizon():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=15,
                target=0.01,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=15,
                target=0.03,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes was not observed during training",
    ):
        baseline.predict(
            horizon_minutes=30,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        15.0,
        "15",
        True,
        False,
    ],
)
def test_mean_return_baseline_rejects_invalid_horizon_type(
    horizon_minutes,
):
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=15,
                target=0.01,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(dataset)

    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        baseline.predict(
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
        -15,
    ],
)
def test_mean_return_baseline_rejects_non_positive_horizon(
    horizon_minutes,
):
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=15,
                target=0.01,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes must be greater than zero",
    ):
        baseline.predict(
            horizon_minutes=horizon_minutes,
        )
