import math

import pytest

from backend.app.ml.lightgbm_return_regressor import (
    LightGBMReturnRegressor,
)
from backend.app.ml.lightgbm_return_regressor_evaluator import (
    LightGBMReturnRegressorEvaluator,
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


def test_lightgbm_return_regressor_evaluator_calculates_metrics_by_horizon():
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

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    metrics_by_horizon = (
        LightGBMReturnRegressorEvaluator.evaluate(
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
        0.02,
        abs=1e-6,
    )
    assert five_minute_metrics.mse == pytest.approx(
        0.0004,
        abs=1e-6,
    )
    assert five_minute_metrics.rmse == pytest.approx(
        0.02,
        abs=1e-6,
    )

    assert thirty_minute_metrics.mae == pytest.approx(
        0.02,
        abs=1e-6,
    )
    assert thirty_minute_metrics.mse == pytest.approx(
        0.0004,
        abs=1e-6,
    )
    assert thirty_minute_metrics.rmse == pytest.approx(
        0.02,
        abs=1e-6,
    )


def test_lightgbm_return_regressor_evaluator_returns_finite_metrics():
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
                target=-0.05,
                feature_value=0.10,
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=5,
                target=0.05,
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
    evaluation_dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_004_800_000,
                horizon_minutes=5,
                target=-0.04,
                feature_value=0.20,
            ),
            create_sample(
                feature_timestamp=1_800_006_000_000,
                horizon_minutes=5,
                target=0.04,
                feature_value=0.80,
            ),
        ]
    )

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    metrics_by_horizon = (
        LightGBMReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=evaluation_dataset,
        )
    )

    metrics = metrics_by_horizon[5]

    assert math.isfinite(metrics.mae)
    assert math.isfinite(metrics.mse)
    assert math.isfinite(metrics.rmse)


def test_lightgbm_return_regressor_evaluator_does_not_refit_model():
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

    model = LightGBMReturnRegressor(
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

    LightGBMReturnRegressorEvaluator.evaluate(
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
        prediction_after,
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
def test_lightgbm_return_regressor_evaluator_rejects_invalid_model(
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
        match="model must be a LightGBMReturnRegressor",
    ):
        LightGBMReturnRegressorEvaluator.evaluate(
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
def test_lightgbm_return_regressor_evaluator_rejects_invalid_dataset(
    dataset,
):
    model = LightGBMReturnRegressor()

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        LightGBMReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=dataset,
        )


def test_lightgbm_return_regressor_evaluator_rejects_unfitted_model():
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

    model = LightGBMReturnRegressor()

    with pytest.raises(
        RuntimeError,
        match="model must be fitted before prediction",
    ):
        LightGBMReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=dataset,
        )


def test_lightgbm_return_regressor_evaluator_rejects_unseen_horizon():
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

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(training_dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes was not observed during training",
    ):
        LightGBMReturnRegressorEvaluator.evaluate(
            model=model,
            dataset=evaluation_dataset,
        )
