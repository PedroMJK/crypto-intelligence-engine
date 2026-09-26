from backend.app.ml.mean_return_baseline import MeanReturnBaseline
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.regression_metrics import RegressionMetrics
from backend.app.ml.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)


class MeanReturnBaselineEvaluator:
    @staticmethod
    def evaluate(
        baseline: MeanReturnBaseline,
        dataset: MLDataset,
    ) -> dict[int, RegressionMetrics]:
        MeanReturnBaselineEvaluator._validate_baseline(
            baseline
        )
        MeanReturnBaselineEvaluator._validate_dataset(
            dataset
        )

        targets_by_horizon: dict[
            int,
            list[float],
        ] = {}

        for sample in dataset.samples:
            targets_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample.target)

        metrics_by_horizon: dict[
            int,
            RegressionMetrics,
        ] = {}

        for (
            horizon_minutes,
            targets,
        ) in targets_by_horizon.items():
            prediction = baseline.predict(
                horizon_minutes=horizon_minutes,
            )

            predictions = [
                prediction
                for _ in targets
            ]

            metrics_by_horizon[
                horizon_minutes
            ] = RegressionMetricsCalculator.calculate(
                actual=targets,
                predicted=predictions,
            )

        return metrics_by_horizon

    @staticmethod
    def _validate_baseline(
        baseline: MeanReturnBaseline,
    ) -> None:
        if not isinstance(
            baseline,
            MeanReturnBaseline,
        ):
            raise TypeError(
                "baseline must be a MeanReturnBaseline"
            )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )
