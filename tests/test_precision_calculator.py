from unittest.mock import patch

import pytest

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
)
from backend.app.backtesting.precision_calculator import PrecisionCalculator
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


def test_precision_calculator_returns_float():
    metrics = [
        create_metrics(),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert isinstance(result, float)


def test_precision_calculator_delegates_to_directional_classifier():
    metrics = [
        create_metrics(),
    ]

    classification = DirectionalClassification(
        true_positive=3,
        false_positive=1,
        true_negative=8,
        false_negative=2,
    )

    with patch.object(
        DirectionalClassifier,
        "classify",
        return_value=classification,
    ) as classify:
        result = PrecisionCalculator.calculate(metrics)

    classify.assert_called_once_with(metrics)
    assert result == pytest.approx(0.75)


def test_precision_calculator_returns_one_for_only_true_positives():
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

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_returns_zero_for_only_false_positives():
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

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(0.0)


def test_precision_calculator_calculates_partial_precision():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.50,
            future_return=0.04,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=0.70,
            future_return=-0.02,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=0.30,
            future_return=-0.01,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(0.5)


def test_precision_calculator_ignores_true_negatives():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.60,
            future_return=-0.05,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_ignores_false_negatives():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.60,
            future_return=0.05,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_ignores_neutral_observations():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.0,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=0.80,
            future_return=0.0,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=0.0,
            future_return=0.0,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_does_not_apply_magnitude_threshold():
    metrics = [
        create_metrics(
            direction_score=0.001,
            future_return=0.000001,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_accepts_tuple():
    metrics = (
        create_metrics(),
    )

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_precision_calculator_accepts_multiple_symbols():
    metrics = [
        create_metrics(
            symbol="FETUSDT",
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            symbol="BTCUSDT",
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.70,
            future_return=-0.02,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(0.5)


def test_precision_calculator_accepts_multiple_horizons():
    metrics = [
        create_metrics(
            horizon_minutes=5,
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            horizon_minutes=30,
            direction_score=0.70,
            future_return=-0.02,
        ),
    ]

    result = PrecisionCalculator.calculate(metrics)

    assert result == pytest.approx(0.5)


def test_precision_calculator_rejects_no_predicted_positive_observations():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.60,
            future_return=0.05,
        ),
    ]

    with pytest.raises(ValueError):
        PrecisionCalculator.calculate(metrics)


def test_precision_calculator_rejects_only_neutral_observations():
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
    ]

    with pytest.raises(ValueError):
        PrecisionCalculator.calculate(metrics)


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
def test_precision_calculator_rejects_invalid_collection(metrics):
    with pytest.raises(TypeError):
        PrecisionCalculator.calculate(metrics)


def test_precision_calculator_rejects_empty_list():
    with pytest.raises(ValueError):
        PrecisionCalculator.calculate([])


def test_precision_calculator_rejects_empty_tuple():
    with pytest.raises(ValueError):
        PrecisionCalculator.calculate(())


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
def test_precision_calculator_rejects_invalid_metric_item(
    invalid_item,
):
    valid = create_metrics()

    with pytest.raises(TypeError):
        PrecisionCalculator.calculate(
            [valid, invalid_item],
        )
