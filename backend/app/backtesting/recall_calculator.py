from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
)
from backend.app.predictions.prediction_metrics import PredictionMetrics


class RecallCalculator:
    @staticmethod
    def calculate(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> float:
        classification = DirectionalClassifier.classify(metrics)

        actual_positive = (
            classification.true_positive
            + classification.false_negative
        )

        if actual_positive == 0:
            raise ValueError(
                "recall requires at least one actual positive observation"
            )

        return (
            classification.true_positive
            / actual_positive
        )
