from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.regression_metrics import RegressionMetrics
from backend.app.ml.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)
from backend.app.ml.xgboost_return_regressor import (
    XGBoostReturnRegressor,
)


class XGBoostReturnRegressorEvaluator:
    @staticmethod
    def evaluate(
        model: XGBoostReturnRegressor,
        dataset: MLDataset,
    ) -> dict[int, RegressionMetrics]:
        XGBoostReturnRegressorEvaluator._validate_model(
            model
        )
        XGBoostReturnRegressorEvaluator._validate_dataset(
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
        model: XGBoostReturnRegressor,
    ) -> None:
        if not isinstance(
            model,
            XGBoostReturnRegressor,
        ):
            raise TypeError(
                "model must be an XGBoostReturnRegressor"
            )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )
