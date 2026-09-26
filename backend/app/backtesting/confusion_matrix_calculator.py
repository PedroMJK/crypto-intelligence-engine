from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
)
from backend.app.predictions.prediction_metrics import PredictionMetrics


class ConfusionMatrixCalculator:
    @staticmethod
    def calculate(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> DirectionalClassification:
        return DirectionalClassifier.classify(metrics)
