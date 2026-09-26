from unittest.mock import patch

import pytest

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
)
from backend.app.backtesting.confusion_matrix_calculator import (
    ConfusionMatrixCalculator,
)
from backend.app.predictions.prediction_metrics import PredictionMetrics


def create_metrics(
    *,
    symbol="FETUSDT",
    prediction_timestamp=1_800_000_000_000,
    horizon_minutes=5,
    direction_score=0.60,
    future_return=0.05,
):
    return PredictionMetrics(
        symbol=symbol,
        prediction_timestamp=prediction_timestamp,
        horizon_minutes=horizon_minutes,
        direction_score=direction_score,
        future_return=future_return,
        directional_alignment=(
            direction_score * future_return
        ),
        absolute_return=abs(future_return),
    )


def test_confusion_matrix_calculator_returns_directional_classification():
    metrics = [
        create_metrics(),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert isinstance(
        result,
        DirectionalClassification,
    )


def test_confusion_matrix_calculator_delegates_to_directional_classifier():
    metrics = [
        create_metrics(),
    ]

    classification = DirectionalClassification(
        true_positive=3,
        false_positive=2,
        true_negative=4,
        false_negative=1,
    )

    with patch.object(
        DirectionalClassifier,
        "classify",
        return_value=classification,
    ) as classify:
        result = ConfusionMatrixCalculator.calculate(metrics)

    classify.assert_called_once_with(metrics)
    assert result is classification


def test_confusion_matrix_calculator_counts_true_positives():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.40,
            future_return=0.03,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result.true_positive == 2
    assert result.false_positive == 0
    assert result.true_negative == 0
    assert result.false_negative == 0


def test_confusion_matrix_calculator_counts_false_positives():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.40,
            future_return=-0.03,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 2
    assert result.true_negative == 0
    assert result.false_negative == 0


def test_confusion_matrix_calculator_counts_true_negatives():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.40,
            future_return=-0.03,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 0
    assert result.true_negative == 2
    assert result.false_negative == 0


def test_confusion_matrix_calculator_counts_false_negatives():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.40,
            future_return=0.03,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 0
    assert result.true_negative == 0
    assert result.false_negative == 2


def test_confusion_matrix_calculator_counts_mixed_classification():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=-0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=-0.60,
            future_return=0.05,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=1,
        false_positive=1,
        true_negative=1,
        false_negative=1,
    )


def test_confusion_matrix_calculator_ignores_neutral_direction():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.05,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_confusion_matrix_calculator_ignores_neutral_return():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.0,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_confusion_matrix_calculator_accepts_only_neutral_observations():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.60,
            future_return=0.0,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=0.0,
            future_return=0.0,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_confusion_matrix_calculator_does_not_apply_magnitude_threshold():
    metrics = [
        create_metrics(
            direction_score=0.001,
            future_return=0.000001,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.001,
            future_return=-0.000001,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=1,
        false_positive=0,
        true_negative=1,
        false_negative=0,
    )


def test_confusion_matrix_calculator_accepts_tuple():
    metrics = (
        create_metrics(),
    )

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result.true_positive == 1


def test_confusion_matrix_calculator_accepts_multiple_symbols():
    metrics = [
        create_metrics(
            symbol="FETUSDT",
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            symbol="BTCUSDT",
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.70,
            future_return=-0.02,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=1,
        false_positive=0,
        true_negative=1,
        false_negative=0,
    )


def test_confusion_matrix_calculator_accepts_multiple_horizons():
    metrics = [
        create_metrics(
            horizon_minutes=5,
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            horizon_minutes=30,
            direction_score=-0.70,
            future_return=0.02,
        ),
    ]

    result = ConfusionMatrixCalculator.calculate(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=1,
        true_negative=0,
        false_negative=1,
    )


@pytest.mark.parametrize(
    "metrics",
    [
        None,
        123,
        True,
        "metrics",
        {},
        set(),
    ],
)
def test_confusion_matrix_calculator_rejects_invalid_collection(metrics):
    with pytest.raises(TypeError):
        ConfusionMatrixCalculator.calculate(metrics)


def test_confusion_matrix_calculator_rejects_empty_list():
    with pytest.raises(ValueError):
        ConfusionMatrixCalculator.calculate([])


def test_confusion_matrix_calculator_rejects_empty_tuple():
    with pytest.raises(ValueError):
        ConfusionMatrixCalculator.calculate(())


@pytest.mark.parametrize(
    "invalid_item",
    [
        None,
        123,
        True,
        "metrics",
        {},
        [],
        (),
    ],
)
def test_confusion_matrix_calculator_rejects_invalid_metric_item(
    invalid_item,
):
    valid = create_metrics()

    with pytest.raises(TypeError):
        ConfusionMatrixCalculator.calculate(
            [valid, invalid_item],
        )
