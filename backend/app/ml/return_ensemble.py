import math
from typing import Protocol

from backend.app.predictions.feature_snapshot import FeatureSnapshot


class ReturnRegressor(Protocol):
    def predict(
        self,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        ...


class ReturnEnsemble:
    def __init__(
        self,
        models: list[ReturnRegressor]
        | tuple[ReturnRegressor, ...],
    ) -> None:
        self._validate_models(models)
        self._models = tuple(models)

    def predict(
        self,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        self._validate_features(features)
        self._validate_horizon_minutes(
            horizon_minutes
        )

        predictions = tuple(
            self._predict_model(
                model=model,
                features=features,
                horizon_minutes=horizon_minutes,
            )
            for model in self._models
        )

        return sum(predictions) / len(predictions)

    @staticmethod
    def _predict_model(
        model: ReturnRegressor,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        prediction = model.predict(
            features=features,
            horizon_minutes=horizon_minutes,
        )

        ReturnEnsemble._validate_prediction(
            prediction
        )

        return prediction

    @staticmethod
    def _validate_models(
        models: list[ReturnRegressor]
        | tuple[ReturnRegressor, ...],
    ) -> None:
        if not isinstance(
            models,
            (list, tuple),
        ):
            raise TypeError(
                "models must be a list or tuple"
            )

        if len(models) < 2:
            raise ValueError(
                "at least two models are required"
            )

        for model in models:
            predict = getattr(
                model,
                "predict",
                None,
            )

            if not callable(predict):
                raise TypeError(
                    "each model must provide a callable "
                    "predict method"
                )

    @staticmethod
    def _validate_features(
        features: FeatureSnapshot,
    ) -> None:
        if not isinstance(
            features,
            FeatureSnapshot,
        ):
            raise TypeError(
                "features must be a FeatureSnapshot"
            )

    @staticmethod
    def _validate_horizon_minutes(
        horizon_minutes: int,
    ) -> None:
        if (
            isinstance(horizon_minutes, bool)
            or not isinstance(
                horizon_minutes,
                int,
            )
        ):
            raise TypeError(
                "horizon_minutes must be an int"
            )

        if horizon_minutes <= 0:
            raise ValueError(
                "horizon_minutes must be greater than zero"
            )

    @staticmethod
    def _validate_prediction(
        prediction: float,
    ) -> None:
        if (
            isinstance(prediction, bool)
            or not isinstance(
                prediction,
                (int, float),
            )
        ):
            raise TypeError(
                "model prediction must be a number"
            )

        if not math.isfinite(prediction):
            raise ValueError(
                "model prediction must be finite"
            )
