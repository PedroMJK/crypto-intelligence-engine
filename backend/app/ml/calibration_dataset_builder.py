import math
from typing import Protocol, runtime_checkable

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.calibration_sample import CalibrationSample
from backend.app.ml.ml_dataset import MLDataset
from backend.app.predictions.feature_snapshot import FeatureSnapshot


@runtime_checkable
class ReturnRegressor(Protocol):
    def predict(
        self,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        ...


class CalibrationDatasetBuilder:
    @staticmethod
    def build(
        model: ReturnRegressor,
        dataset: MLDataset,
    ) -> CalibrationDataset:
        CalibrationDatasetBuilder._validate_model(
            model
        )
        CalibrationDatasetBuilder._validate_dataset(
            dataset
        )

        samples = tuple(
            CalibrationDatasetBuilder._build_sample(
                model=model,
                sample=sample,
            )
            for sample in dataset.samples
        )

        return CalibrationDataset(
            samples=samples
        )

    @staticmethod
    def _build_sample(
        model: ReturnRegressor,
        sample,
    ) -> CalibrationSample:
        predicted_return = model.predict(
            features=sample.features,
            horizon_minutes=sample.horizon_minutes,
        )

        CalibrationDatasetBuilder._validate_prediction(
            predicted_return
        )

        return CalibrationSample(
            horizon_minutes=sample.horizon_minutes,
            predicted_return=predicted_return,
            observed_return=sample.target,
        )

    @staticmethod
    def _validate_model(
        model: ReturnRegressor,
    ) -> None:
        predict = getattr(
            model,
            "predict",
            None,
        )

        if not callable(predict):
            raise TypeError(
                "model must provide a callable predict method"
            )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(
            dataset,
            MLDataset,
        ):
            raise TypeError(
                "dataset must be an MLDataset"
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
