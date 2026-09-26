from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.predictions.prediction_metrics import PredictionMetrics


class DirectionalClassifier:
    @staticmethod
    def classify(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> DirectionalClassification:
        DirectionalClassifier._validate_collection(metrics)

        true_positive = 0
        false_positive = 0
        true_negative = 0
        false_negative = 0

        for metric in metrics:
            if (
                metric.direction_score > 0
                and metric.future_return > 0
            ):
                true_positive += 1
            elif (
                metric.direction_score > 0
                and metric.future_return < 0
            ):
                false_positive += 1
            elif (
                metric.direction_score < 0
                and metric.future_return < 0
            ):
                true_negative += 1
            elif (
                metric.direction_score < 0
                and metric.future_return > 0
            ):
                false_negative += 1

        return DirectionalClassification(
            true_positive=true_positive,
            false_positive=false_positive,
            true_negative=true_negative,
            false_negative=false_negative,
        )

    @staticmethod
    def _validate_collection(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> None:
        if not isinstance(metrics, (list, tuple)):
            raise TypeError(
                "metrics must be a list or tuple"
            )

        if not metrics:
            raise ValueError(
                "metrics must not be empty"
            )

        for metric in metrics:
            if not isinstance(metric, PredictionMetrics):
                raise TypeError(
                    "all metrics must be PredictionMetrics"
                )
