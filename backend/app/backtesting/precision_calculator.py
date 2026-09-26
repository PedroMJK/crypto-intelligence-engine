from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
)
from backend.app.predictions.prediction_metrics import PredictionMetrics


class PrecisionCalculator:
    @staticmethod
    def calculate(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> float:
        classification = DirectionalClassifier.classify(metrics)

        predicted_positive = (
            classification.true_positive
            + classification.false_positive
        )

        if predicted_positive == 0:
            raise ValueError(
                "precision requires at least one predicted positive observation"
            )

        return (
            classification.true_positive
            / predicted_positive
        )
