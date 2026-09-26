from dataclasses import FrozenInstanceError

import pytest

from backend.app.ml.directional_comparison_metrics import (
    DirectionalComparisonMetrics,
)


def test_directional_comparison_metrics_stores_values():
    metrics = DirectionalComparisonMetrics(
        directional_accuracy=0.75,
        correct_predictions=3,
        evaluated_predictions=4,
        neutral_predictions=2,
    )

    assert metrics.directional_accuracy == 0.75
    assert metrics.correct_predictions == 3
    assert metrics.evaluated_predictions == 4
    assert metrics.neutral_predictions == 2


def test_directional_comparison_metrics_is_immutable():
    metrics = DirectionalComparisonMetrics(
        directional_accuracy=0.75,
        correct_predictions=3,
        evaluated_predictions=4,
        neutral_predictions=2,
    )

    with pytest.raises(FrozenInstanceError):
        metrics.directional_accuracy = 0.50
