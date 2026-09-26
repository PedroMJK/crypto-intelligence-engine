import pytest

from backend.app.ml.mean_return_baseline import MeanReturnBaseline
from backend.app.ml.mean_return_baseline_evaluator import (
    MeanReturnBaselineEvaluator,
)
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.ml.regression_metrics import RegressionMetrics
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


def test_mean_return_baseline_evaluator_calculates_metrics_by_horizon():
    training_dataset = MLDataset(
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
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_007_200_000,
                horizon_minutes=5,
                target=0.01,
            ),
            create_sample(
                feature_timestamp=1_800_008_400_000,
                horizon_minutes=5,
                target=0.05,
            ),
            create_sample(
                feature_timestamp=1_800_009_600_000,
                horizon_minutes=30,
                target=-0.01,
            ),
            create_sample(
                feature_timestamp=1_800_012_000_000,
                horizon_minutes=30,
                target=-0.05,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(training_dataset)

    metrics_by_horizon = (
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=evaluation_dataset,
        )
    )

    assert set(metrics_by_horizon) == {
        5,
        30,
    }

    five_minute_metrics = metrics_by_horizon[5]
    thirty_minute_metrics = metrics_by_horizon[30]

    assert isinstance(
        five_minute_metrics,
        RegressionMetrics,
    )
    assert isinstance(
        thirty_minute_metrics,
        RegressionMetrics,
    )
    assert five_minute_metrics.mae == pytest.approx(
        0.02
    )
    assert five_minute_metrics.mse == pytest.approx(
        0.0005
    )
    assert five_minute_metrics.rmse == pytest.approx(
        0.0005 ** 0.5
    )

    assert thirty_minute_metrics.mae == pytest.approx(
        0.02
    )
    assert thirty_minute_metrics.mse == pytest.approx(
        0.0004
    )
    assert thirty_minute_metrics.rmse == pytest.approx(
        0.02
    )


def test_mean_return_baseline_evaluator_uses_training_mean_without_refitting():
    training_dataset = MLDataset(
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
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_003_600_000,
                horizon_minutes=15,
                target=0.10,
            ),
            create_sample(
                feature_timestamp=1_800_004_800_000,
                horizon_minutes=15,
                target=0.10,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(training_dataset)

    metrics_by_horizon = (
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=evaluation_dataset,
        )
    )

    metrics = metrics_by_horizon[15]

    assert metrics.mae == pytest.approx(
        0.08
    )
    assert metrics.mse == pytest.approx(
        0.0064
    )
    assert metrics.rmse == pytest.approx(
        0.08
    )

    assert baseline.predict(
        horizon_minutes=15,
    ) == pytest.approx(
        0.02
    )


@pytest.mark.parametrize(
    "baseline",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_mean_return_baseline_evaluator_rejects_invalid_baseline(
    baseline,
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

    with pytest.raises(
        TypeError,
        match="baseline must be a MeanReturnBaseline",
    ):
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=dataset,
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
def test_mean_return_baseline_evaluator_rejects_invalid_dataset(
    dataset,
):
    baseline = MeanReturnBaseline()

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=dataset,
        )


def test_mean_return_baseline_evaluator_rejects_unfitted_baseline():
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

    with pytest.raises(
        RuntimeError,
        match="baseline must be fitted before prediction",
    ):
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=dataset,
        )


def test_mean_return_baseline_evaluator_rejects_unseen_horizon():
    training_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
            ),
        ]
    )
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=30,
                target=-0.01,
            ),
        ]
    )

    baseline = MeanReturnBaseline()
    baseline.fit(training_dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes was not observed during training",
    ):
        MeanReturnBaselineEvaluator.evaluate(
            baseline=baseline,
            dataset=evaluation_dataset,
        )
