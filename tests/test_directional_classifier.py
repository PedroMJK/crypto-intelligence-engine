import pytest

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.directional_classifier import (
    DirectionalClassifier,
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


def test_directional_classifier_returns_classification():
    metrics = [
        create_metrics(),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert isinstance(
        result,
        DirectionalClassification,
    )


def test_directional_classifier_counts_true_positive():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 1
    assert result.false_positive == 0
    assert result.true_negative == 0
    assert result.false_negative == 0


def test_directional_classifier_counts_false_positive():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=-0.05,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 1
    assert result.true_negative == 0
    assert result.false_negative == 0


def test_directional_classifier_counts_true_negative():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 0
    assert result.true_negative == 1
    assert result.false_negative == 0


def test_directional_classifier_counts_false_negative():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=0.05,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 0
    assert result.false_positive == 0
    assert result.true_negative == 0
    assert result.false_negative == 1


def test_directional_classifier_counts_mixed_observations():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.40,
            future_return=-0.03,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=-0.50,
            future_return=-0.02,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=-0.70,
            future_return=0.04,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result == DirectionalClassification(
        true_positive=1,
        false_positive=1,
        true_negative=1,
        false_negative=1,
    )


def test_directional_classifier_excludes_zero_direction_score():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.05,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_directional_classifier_excludes_zero_future_return():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.0,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_directional_classifier_excludes_fully_neutral_observation():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.0,
        ),
    ]

    result = DirectionalClassifier.classify(metrics)

    assert result == DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )


def test_directional_classifier_does_not_apply_magnitude_threshold():
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

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 1
    assert result.true_negative == 1


def test_directional_classifier_accepts_tuple():
    metrics = (
        create_metrics(),
    )

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 1


def test_directional_classifier_accepts_multiple_symbols():
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

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 1
    assert result.true_negative == 1


def test_directional_classifier_accepts_multiple_horizons():
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

    result = DirectionalClassifier.classify(metrics)

    assert result.true_positive == 1
    assert result.false_positive == 1


def test_directional_classifier_does_not_mutate_metrics():
    metrics = [
        create_metrics(),
    ]
    original = tuple(metrics)

    DirectionalClassifier.classify(metrics)

    assert tuple(metrics) == original


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
def test_directional_classifier_rejects_invalid_collection(metrics):
    with pytest.raises(TypeError):
        DirectionalClassifier.classify(metrics)


def test_directional_classifier_rejects_empty_list():
    with pytest.raises(ValueError):
        DirectionalClassifier.classify([])


def test_directional_classifier_rejects_empty_tuple():
    with pytest.raises(ValueError):
        DirectionalClassifier.classify(())


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
def test_directional_classifier_rejects_invalid_metric_item(
    invalid_item,
):
    valid = create_metrics()

    with pytest.raises(TypeError):
        DirectionalClassifier.classify(
            [valid, invalid_item],
        )
