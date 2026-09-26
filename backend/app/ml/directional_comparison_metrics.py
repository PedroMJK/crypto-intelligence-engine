from dataclasses import dataclass


@dataclass(frozen=True)
class DirectionalComparisonMetrics:
    directional_accuracy: float
    correct_predictions: int
    evaluated_predictions: int
    neutral_predictions: int
