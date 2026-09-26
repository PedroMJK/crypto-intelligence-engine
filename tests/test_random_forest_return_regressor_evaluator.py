import math

import pytest

from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.ml.random_forest_return_regressor import (
    RandomForestReturnRegressor,
)
from backend.app.ml.random_forest_return_regressor_evaluator import (
    RandomForestReturnRegressorEvaluator,
)
from backend.app.ml.regression_metrics import RegressionMetrics
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_sample(
    *,
    feature_timestamp: int,
    horizon_minutes: int,
    target: float,
    feature_value: float,
) -> MLSample:
    return MLSample(
        features=FeatureSnapshot(
            symbol="FETUSDT",
            feature_timestamp=feature_timestamp,
            features={
                "technical_score": feature_value,
            },
        ),
        horizon_minutes=horizon_minutes,
        target=target,
        target_timestamp=(
            feature_timestamp
            + horizon_minutes * 60_000
        ),
    )


def test_random_forest_return_regressor_evaluator_calculates_metrics_by_horizon():
    training_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=0.20,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=0.80,
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=30,
                target=-0.10,
                feature_value=0.20,
            ),
            create_sample(
                feature_timestamp=1_800_004_800_000,
                horizon_minutes=30,
                target=-0.10,
                feature_value=0.80,
            ),
        ]
    )
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_007_200_000,
                horizon_minutes=5,
                target=0.08,
                feature_value=0.30,
            ),
            create_sample(
                feature_timestamp=1_800_008_400_000,
                horizon_minutes=5,
                target=0.12,
                feature_value=0.70,
            ),
            create_sample(
                feature_timestamp=1_800_009_600_000,
                horizon_minutes=30,
                target=-0.08,
                feature_value=0.30,
            ),
            create_sample(
                feature_timestamp=1_800_012_000_000,
                horizon_minutes=30,
                target=-0.12,
                feature_value=0.70,
            ),
        ]
    )

    model = RandomForestReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    metrics_by_horizon = (
        RandomForestReturnRegressorEvaluator.evaluate(
            model=model,
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
        0.0004
    )
    assert five_minute_metrics.rmse == pytest.approx(
        0.02
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


def test_random_forest_return_regressor_evaluator_uses_sample_features():
    training_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=-0.10,
                feature_value=0.00,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=-0.10,
                feature_value=0.10,
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=0.90,
            ),
            create_sample(
                feature_timestamp=1_800_003_600_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=1.00,
            ),
        ]
    )

    model = RandomForestReturnRegressor(
        n_estimators=100,
        random_state=42,
    )
    model.fit(training_dataset)

    low_feature_prediction = model.predict(
        features=FeatureSnapshot(
            symbol="FETUSDT",
            feature_timestamp=1_800_004_800_000,
            features={
                "technical_score": 0.05,
            },
        ),
        horizon_minutes=5,
    )
    high_feature_prediction = model.predict(
        features=FeatureSnapshot(
            symbol="FETUSDT",
            feature_timestamp=1_800_006_000_000,
            features={
                "technical_score": 0.95,
            },
        ),
        horizon_minutes=5,
    )

    assert math.isfinite(
        low_feature_prediction
    )
    assert math.isfinite(
        high_feature_prediction
    )
    assert (
        low_feature_prediction
        < high_feature_prediction
    )


def test_random_forest_return_regressor_evaluator_does_not_refit_model():
    training_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=0.20,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.10,
                feature_value=0.80,
            ),
        ]
    )
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=5,
                target=-0.50,
                feature_value=0.50,
            ),
        ]
    )

    model = RandomForestReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    prediction_before = model.predict(
        features=evaluation_dataset.samples[
            0
        ].features,
        horizon_minutes=5,
    )

    RandomForestReturnRegressorEvaluator.evaluate(
        model=model,
        dataset=evaluation_dataset,
    )

    prediction_after = model.predict(
        features=evaluation_dataset.samples[
            0
        ].features,
        horizon_minutes=5,
    )

    assert prediction_before == pytest.approx(
        0.10
    )
    assert prediction_after == pytest.approx(
        prediction_before
    )


@pytest.mark.parametrize(
    "model",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_random_forest_return_regressor_evaluator_rejects_invalid_model(
    model,
):
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                feature_value=0.50,
            ),
        ]
    )

    with pytest.raises(
        TypeError,
        match="model must be a RandomForestReturnRegressor",
    ):
        RandomForestReturnRegressorEvaluator.evaluate(
            model=model,
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
def test_random_forest_return_regressor_evaluator_rejects_invalid_dataset(
    dataset,
):
    model = RandomForestReturnRegressor()

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        RandomForestReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=dataset,
        )


def test_random_forest_return_regressor_evaluator_rejects_unfitted_model():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                feature_value=0.50,
            ),
        ]
    )

    model = RandomForestReturnRegressor()

    with pytest.raises(
        RuntimeError,
        match="model must be fitted before prediction",
    ):
        RandomForestReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=dataset,
        )


def test_random_forest_return_regressor_evaluator_rejects_unseen_horizon():
    training_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                feature_value=0.20,
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.02,
                feature_value=0.80,
            ),
        ]
    )
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_003_600_000,
                horizon_minutes=30,
                target=-0.01,
                feature_value=0.50,
            ),
        ]
    )

    model = RandomForestReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes was not observed during training",
    ):
        RandomForestReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=evaluation_dataset,
        )
