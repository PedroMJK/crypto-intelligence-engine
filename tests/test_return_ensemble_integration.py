import pytest

from backend.app.ml.lightgbm_return_regressor import (
    LightGBMReturnRegressor,
)
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.ml.random_forest_return_regressor import (
    RandomForestReturnRegressor,
)
from backend.app.ml.return_ensemble import ReturnEnsemble
from backend.app.ml.xgboost_return_regressor import (
    XGBoostReturnRegressor,
)
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_features(
    *,
    timestamp: int,
    direction_score: float,
    momentum_score: float,
) -> FeatureSnapshot:
    return FeatureSnapshot(
        symbol="BTCUSDT",
        feature_timestamp=timestamp,
        features={
            "technical_score": direction_score,
            "flow_score": direction_score,
            "momentum_score": momentum_score,
            "structure_score": direction_score,
            "direction_score": direction_score,
            "volume_score": 0.7,
            "confidence": 0.8,
            "contradiction": 0.1,
        },
    )


def create_training_dataset() -> MLDataset:
    samples = []

    for index in range(12):
        timestamp = (
            1_700_000_000_000
            + index * 60_000
        )

        direction_score = (
            0.6
            if index % 2 == 0
            else -0.6
        )

        momentum_score = (
            0.4
            if index % 2 == 0
            else -0.4
        )

        target = (
            0.01
            if index % 2 == 0
            else -0.01
        )

        samples.append(
            MLSample(
                features=create_features(
                    timestamp=timestamp,
                    direction_score=direction_score,
                    momentum_score=momentum_score,
                ),
                horizon_minutes=15,
                target=target,
                target_timestamp=(
                    timestamp
                    + 15 * 60_000
                ),
            )
        )

    return MLDataset(
        samples=samples
    )


def create_trained_ensemble() -> ReturnEnsemble:
    dataset = create_training_dataset()

    random_forest = RandomForestReturnRegressor()
    xgboost = XGBoostReturnRegressor()
    lightgbm = LightGBMReturnRegressor()

    random_forest.fit(dataset)
    xgboost.fit(dataset)
    lightgbm.fit(dataset)

    return ReturnEnsemble(
        models=[
            random_forest,
            xgboost,
            lightgbm,
        ]
    )


def test_return_ensemble_integrates_real_regressors():
    ensemble = create_trained_ensemble()

    features = create_features(
        timestamp=1_700_001_000_000,
        direction_score=0.5,
        momentum_score=0.3,
    )

    prediction = ensemble.predict(
        features=features,
        horizon_minutes=15,
    )

    assert isinstance(
        prediction,
        float,
    )


def test_return_ensemble_matches_mean_of_real_regressor_predictions():
    dataset = create_training_dataset()

    random_forest = RandomForestReturnRegressor()
    xgboost = XGBoostReturnRegressor()
    lightgbm = LightGBMReturnRegressor()

    models = [
        random_forest,
        xgboost,
        lightgbm,
    ]

    for model in models:
        model.fit(dataset)

    ensemble = ReturnEnsemble(
        models=models
    )

    features = create_features(
        timestamp=1_700_001_000_000,
        direction_score=0.5,
        momentum_score=0.3,
    )

    individual_predictions = [
        model.predict(
            features=features,
            horizon_minutes=15,
        )
        for model in models
    ]

    ensemble_prediction = ensemble.predict(
        features=features,
        horizon_minutes=15,
    )

    expected_prediction = (
        sum(individual_predictions)
        / len(individual_predictions)
    )

    assert ensemble_prediction == pytest.approx(
        expected_prediction
    )


def test_return_ensemble_preserves_horizon_specific_model_contract():
    ensemble = create_trained_ensemble()

    features = create_features(
        timestamp=1_700_001_000_000,
        direction_score=0.5,
        momentum_score=0.3,
    )

    with pytest.raises(ValueError):
        ensemble.predict(
            features=features,
            horizon_minutes=30,
        )
