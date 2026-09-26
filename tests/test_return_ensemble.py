import math
from unittest.mock import Mock

import pytest

from backend.app.ml.return_ensemble import ReturnEnsemble
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_features() -> FeatureSnapshot:
    return FeatureSnapshot(
        symbol="BTCUSDT",
        feature_timestamp=1_700_000_000_000,
        features={
            "technical_score": 0.5,
            "flow_score": 0.4,
            "momentum_score": 0.3,
            "structure_score": 0.2,
            "direction_score": 0.4,
            "volume_score": 0.7,
            "confidence": 0.8,
            "contradiction": 0.1,
        },
    )


def create_model(
    predicted_return: float,
) -> Mock:
    model = Mock()
    model.predict.return_value = predicted_return

    return model


def test_return_ensemble_averages_model_predictions():
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.012),
            create_model(0.009),
            create_model(-0.003),
        ]
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=15,
    )

    assert prediction == pytest.approx(
        0.006
    )


def test_return_ensemble_supports_two_models():
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.02),
            create_model(0.01),
        ]
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=5,
    )

    assert prediction == pytest.approx(
        0.015
    )


def test_return_ensemble_supports_more_than_three_models():
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(0.02),
            create_model(0.03),
            create_model(0.04),
        ]
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=30,
    )

    assert prediction == pytest.approx(
        0.025
    )


def test_return_ensemble_calls_each_model_once():
    models = [
        create_model(0.01),
        create_model(0.02),
        create_model(0.03),
    ]

    ensemble = ReturnEnsemble(
        models=models
    )

    features = create_features()

    ensemble.predict(
        features=features,
        horizon_minutes=15,
    )

    for model in models:
        model.predict.assert_called_once_with(
            features=features,
            horizon_minutes=15,
        )


def test_return_ensemble_does_not_fit_models():
    models = [
        create_model(0.01),
        create_model(0.02),
        create_model(0.03),
    ]

    ensemble = ReturnEnsemble(
        models=models
    )

    ensemble.predict(
        features=create_features(),
        horizon_minutes=15,
    )

    for model in models:
        model.fit.assert_not_called()


def test_return_ensemble_preserves_negative_mean():
    ensemble = ReturnEnsemble(
        models=[
            create_model(-0.01),
            create_model(-0.02),
            create_model(0.00),
        ]
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=15,
    )

    assert prediction == pytest.approx(
        -0.01
    )


def test_return_ensemble_preserves_zero_mean():
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(-0.01),
        ]
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=15,
    )

    assert prediction == pytest.approx(
        0.0
    )


def test_return_ensemble_does_not_modify_features():
    features = create_features()

    original_features = dict(
        features.features
    )

    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(0.02),
        ]
    )

    ensemble.predict(
        features=features,
        horizon_minutes=15,
    )

    assert dict(features.features) == original_features


@pytest.mark.parametrize(
    "models",
    [
        None,
        "invalid",
        123,
        True,
        {},
    ],
)
def test_return_ensemble_rejects_invalid_models_collection(
    models,
):
    with pytest.raises(
        TypeError,
        match="models must be a list or tuple",
    ):
        ReturnEnsemble(
            models=models
        )


@pytest.mark.parametrize(
    "models",
    [
        [],
        [create_model(0.01)],
    ],
)
def test_return_ensemble_requires_at_least_two_models(
    models,
):
    with pytest.raises(
        ValueError,
        match="at least two models are required",
    ):
        ReturnEnsemble(
            models=models
        )


def test_return_ensemble_accepts_tuple_of_models():
    ensemble = ReturnEnsemble(
        models=(
            create_model(0.01),
            create_model(0.03),
        )
    )

    prediction = ensemble.predict(
        features=create_features(),
        horizon_minutes=15,
    )

    assert prediction == pytest.approx(
        0.02
    )


@pytest.mark.parametrize(
    "invalid_model",
    [
        None,
        "invalid",
        123,
        True,
        object(),
    ],
)
def test_return_ensemble_rejects_model_without_callable_predict(
    invalid_model,
):
    with pytest.raises(
        TypeError,
        match=(
            "each model must provide a callable "
            "predict method"
        ),
    ):
        ReturnEnsemble(
            models=[
                create_model(0.01),
                invalid_model,
            ]
        )


@pytest.mark.parametrize(
    "features",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_return_ensemble_rejects_invalid_features(
    features,
):
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(0.02),
        ]
    )

    with pytest.raises(
        TypeError,
        match="features must be a FeatureSnapshot",
    ):
        ensemble.predict(
            features=features,
            horizon_minutes=15,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        1.5,
        "15",
        True,
    ],
)
def test_return_ensemble_rejects_invalid_horizon_type(
    horizon_minutes,
):
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(0.02),
        ]
    )

    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        ensemble.predict(
            features=create_features(),
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
def test_return_ensemble_rejects_non_positive_horizon(
    horizon_minutes,
):
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(0.02),
        ]
    )

    with pytest.raises(
        ValueError,
        match=(
            "horizon_minutes must be greater than zero"
        ),
    ):
        ensemble.predict(
            features=create_features(),
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        "invalid",
        True,
    ],
)
def test_return_ensemble_rejects_non_numeric_model_prediction(
    prediction,
):
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(prediction),
        ]
    )

    with pytest.raises(
        TypeError,
        match="model prediction must be a number",
    ):
        ensemble.predict(
            features=create_features(),
            horizon_minutes=15,
        )


@pytest.mark.parametrize(
    "prediction",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_return_ensemble_rejects_non_finite_model_prediction(
    prediction,
):
    ensemble = ReturnEnsemble(
        models=[
            create_model(0.01),
            create_model(prediction),
        ]
    )

    with pytest.raises(
        ValueError,
        match="model prediction must be finite",
    ):
        ensemble.predict(
            features=create_features(),
            horizon_minutes=15,
        )
