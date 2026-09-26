from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.random_forest_return_regressor import (
    RandomForestReturnRegressor,
)
from backend.app.ml.regression_metrics import RegressionMetrics
from backend.app.ml.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)


class RandomForestReturnRegressorEvaluator:
    @staticmethod
    def evaluate(
        model: RandomForestReturnRegressor,
        dataset: MLDataset,
    ) -> dict[int, RegressionMetrics]:
        RandomForestReturnRegressorEvaluator._validate_model(
            model
        )
        RandomForestReturnRegressorEvaluator._validate_dataset(
            dataset
        )

        actual_by_horizon: dict[
            int,
            list[float],
        ] = {}
        predicted_by_horizon: dict[
            int,
            list[float],
        ] = {}

        for sample in dataset.samples:
            prediction = model.predict(
                features=sample.features,
                horizon_minutes=sample.horizon_minutes,
            )

            actual_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample.target)

            predicted_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(prediction)

        metrics_by_horizon: dict[
            int,
            RegressionMetrics,
        ] = {}

        for (
            horizon_minutes,
            actual,
        ) in actual_by_horizon.items():
            metrics_by_horizon[
                horizon_minutes
            ] = RegressionMetricsCalculator.calculate(
                actual=actual,
                predicted=predicted_by_horizon[
                    horizon_minutes
                ],
            )

        return metrics_by_horizon

    @staticmethod
    def _validate_model(
        model: RandomForestReturnRegressor,
    ) -> None:
        if not isinstance(
            model,
            RandomForestReturnRegressor,
        ):
            raise TypeError(
                "model must be a RandomForestReturnRegressor"
            )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )
