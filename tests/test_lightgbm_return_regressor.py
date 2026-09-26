import math

import pytest

from backend.app.ml.lightgbm_return_regressor import (
    LightGBMReturnRegressor,
)
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_sample(
    *,
    feature_timestamp: int,
    horizon_minutes: int,
    target: float,
    features: dict[str, float] | None = None,
) -> MLSample:
    if features is None:
        features = {
            "technical_score": 0.60,
            "flow_score": -0.20,
            "momentum_score": 0.40,
            "structure_score": 0.10,
            "direction_score": 0.35,
            "volume_score": 0.80,
            "confidence": 0.70,
            "contradiction": 0.15,
        }

    return MLSample(
        features=FeatureSnapshot(
            symbol="FETUSDT",
            feature_timestamp=feature_timestamp,
            features=features,
        ),
        horizon_minutes=horizon_minutes,
        target=target,
        target_timestamp=(
            feature_timestamp
            + horizon_minutes * 60_000
        ),
    )


def create_feature_snapshot(
    *,
    feature_timestamp: int,
    features: dict[str, float] | None = None,
) -> FeatureSnapshot:
    if features is None:
        features = {
            "technical_score": 0.55,
            "flow_score": -0.10,
            "momentum_score": 0.30,
            "structure_score": 0.20,
            "direction_score": 0.40,
            "volume_score": 0.75,
            "confidence": 0.65,
            "contradiction": 0.10,
        }

    return FeatureSnapshot(
        symbol="FETUSDT",
        feature_timestamp=feature_timestamp,
        features=features,
    )


def test_lightgbm_return_regressor_fits_and_predicts_continuous_return():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                features={
                    "technical_score": 0.10,
                    "flow_score": 0.10,
                },
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.03,
                features={
                    "technical_score": 0.90,
                    "flow_score": 0.90,
                },
            ),
        ]
    )

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(dataset)

    prediction = model.predict(
        features=create_feature_snapshot(
            feature_timestamp=1_800_002_400_000,
            features={
                "technical_score": 0.80,
                "flow_score": 0.80,
            },
        ),
        horizon_minutes=5,
    )

    assert isinstance(prediction, float)
    assert math.isfinite(prediction)


def test_lightgbm_return_regressor_trains_independent_models_by_horizon():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.10,
                features={
                    "technical_score": 0.20,
                },
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.10,
                features={
                    "technical_score": 0.80,
                },
            ),
            create_sample(
                feature_timestamp=1_800_002_400_000,
                horizon_minutes=30,
                target=-0.10,
                features={
                    "technical_score": 0.20,
                },
            ),
            create_sample(
                feature_timestamp=1_800_004_800_000,
                horizon_minutes=30,
                target=-0.10,
                features={
                    "technical_score": 0.80,
                },
            ),
        ]
    )

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(dataset)

    features = create_feature_snapshot(
        feature_timestamp=1_800_007_200_000,
        features={
            "technical_score": 0.50,
        },
    )

    five_minute_prediction = model.predict(
        features=features,
        horizon_minutes=5,
    )
    thirty_minute_prediction = model.predict(
        features=features,
        horizon_minutes=30,
    )

    assert five_minute_prediction == pytest.approx(
        0.10,
        abs=1e-6,
    )
    assert thirty_minute_prediction == pytest.approx(
        -0.10,
        abs=1e-6,
    )


def test_lightgbm_return_regressor_uses_feature_names_consistently():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                features={
                    "technical_score": 0.20,
                    "flow_score": 0.30,
                },
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.02,
                features={
                    "flow_score": 0.70,
                    "technical_score": 0.80,
                },
            ),
        ]
    )

    model = LightGBMReturnRegressor(
        n_estimators=20,
        random_state=42,
    )
    model.fit(dataset)

    prediction = model.predict(
        features=create_feature_snapshot(
            feature_timestamp=1_800_002_400_000,
            features={
                "flow_score": 0.50,
                "technical_score": 0.50,
            },
        ),
        horizon_minutes=5,
    )

    assert isinstance(prediction, float)
    assert math.isfinite(prediction)


def test_lightgbm_return_regressor_rejects_inconsistent_training_feature_schema():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                features={
                    "technical_score": 0.20,
                    "flow_score": 0.30,
                },
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.02,
                features={
                    "technical_score": 0.80,
                    "momentum_score": 0.70,
                },
            ),
        ]
    )

    model = LightGBMReturnRegressor()

    with pytest.raises(
        ValueError,
        match="all training samples must use the same feature schema",
    ):
        model.fit(dataset)


def test_lightgbm_return_regressor_rejects_incompatible_prediction_feature_schema():
    dataset = MLDataset(
        samples=[
            create_sample(
                feature_timestamp=1_800_000_000_000,
                horizon_minutes=5,
                target=0.01,
                features={
                    "technical_score": 0.20,
                    "flow_score": 0.30,
                },
            ),
            create_sample(
                feature_timestamp=1_800_001_200_000,
                horizon_minutes=5,
                target=0.02,
                features={
                    "technical_score": 0.80,
                    "flow_score": 0.70,
                },
            ),
        ]
    )

    model = LightGBMReturnRegressor()
    model.fit(dataset)

    with pytest.raises(
        ValueError,
        match="prediction feature schema must match training feature schema",
    ):
        model.predict(
            features=create_feature_snapshot(
                feature_timestamp=1_800_002_400_000,
                features={
                    "technical_score": 0.50,
                    "momentum_score": 0.50,
                },
            ),
            horizon_minutes=5,
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
def test_lightgbm_return_regressor_rejects_invalid_training_dataset(
    dataset,
):
    model = LightGBMReturnRegressor()

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        model.fit(dataset)


def test_lightgbm_return_regressor_rejects_prediction_before_fit():
    model = LightGBMReturnRegressor()

    with pytest.raises(
        RuntimeError,
        match="model must be fitted before prediction",
    ):
        model.predict(
            features=create_feature_snapshot(
                feature_timestamp=1_800_000_000_000,
            ),
            horizon_minutes=5,
        )


def test_lightgbm_return_regressor_rejects_unseen_horizon():
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
                target=0.02,
            ),
        ]
    )

    model = LightGBMReturnRegressor()
    model.fit(dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes was not observed during training",
    ):
        model.predict(
            features=create_feature_snapshot(
                feature_timestamp=1_800_002_400_000,
            ),
            horizon_minutes=30,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        5.0,
        "5",
        True,
    ],
)
def test_lightgbm_return_regressor_rejects_invalid_horizon_type(
    horizon_minutes,
):
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
                target=0.02,
            ),
        ]
    )

    model = LightGBMReturnRegressor()
    model.fit(dataset)

    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        model.predict(
            features=create_feature_snapshot(
                feature_timestamp=1_800_001_200_000,
            ),
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
        -30,
    ],
)
def test_lightgbm_return_regressor_rejects_non_positive_horizon(
    horizon_minutes,
):
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
                target=0.02,
            ),
        ]
    )

    model = LightGBMReturnRegressor()
    model.fit(dataset)

    with pytest.raises(
        ValueError,
        match="horizon_minutes must be greater than zero",
    ):
        model.predict(
            features=create_feature_snapshot(
                feature_timestamp=1_800_001_200_000,
            ),
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "features",
    [
        None,
        {},
        "invalid",
        123,
        True,
    ],
)
def test_lightgbm_return_regressor_rejects_invalid_prediction_features(
    features,
):
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
                target=0.02,
            ),
        ]
    )

    model = LightGBMReturnRegressor()
    model.fit(dataset)

    with pytest.raises(
        TypeError,
        match="features must be a FeatureSnapshot",
    ):
        model.predict(
            features=features,
            horizon_minutes=5,
        )


@pytest.mark.parametrize(
    "n_estimators",
    [
        0,
        -1,
        -100,
    ],
)
def test_lightgbm_return_regressor_rejects_non_positive_n_estimators(
    n_estimators,
):
    with pytest.raises(
        ValueError,
        match="n_estimators must be greater than zero",
    ):
        LightGBMReturnRegressor(
            n_estimators=n_estimators,
        )


@pytest.mark.parametrize(
    "n_estimators",
    [
        None,
        10.5,
        "100",
        True,
    ],
)
def test_lightgbm_return_regressor_rejects_invalid_n_estimators_type(
    n_estimators,
):
    with pytest.raises(
        TypeError,
        match="n_estimators must be an int",
    ):
        LightGBMReturnRegressor(
            n_estimators=n_estimators,
        )


@pytest.mark.parametrize(
    "random_state",
    [
        42.5,
        "42",
        True,
    ],
)
def test_lightgbm_return_regressor_rejects_invalid_random_state(
    random_state,
):
    with pytest.raises(
        TypeError,
        match="random_state must be an int or None",
    ):
        LightGBMReturnRegressor(
            random_state=random_state,
        )


def test_lightgbm_return_regressor_accepts_none_random_state():
    model = LightGBMReturnRegressor(
        random_state=None,
    )

    assert isinstance(
        model,
        LightGBMReturnRegressor,
    )
