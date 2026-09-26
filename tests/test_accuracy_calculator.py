import pytest

from backend.app.backtesting.accuracy_calculator import AccuracyCalculator
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


def test_accuracy_calculator_returns_float():
    metrics = [
        create_metrics(),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert isinstance(result, float)


def test_accuracy_calculator_returns_one_for_all_aligned():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.40,
            future_return=-0.03,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_accuracy_calculator_returns_zero_for_all_opposed():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.40,
            future_return=0.03,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(0.0)


def test_accuracy_calculator_calculates_partial_accuracy():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.40,
            future_return=-0.03,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=0.50,
            future_return=-0.02,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=-0.70,
            future_return=0.04,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(0.5)


def test_accuracy_calculator_excludes_zero_direction_score():
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
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_accuracy_calculator_excludes_zero_future_return():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.80,
            future_return=0.0,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_accuracy_calculator_excludes_fully_neutral_observation():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.0,
            future_return=0.0,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(0.0)


def test_accuracy_calculator_does_not_apply_magnitude_threshold():
    metrics = [
        create_metrics(
            direction_score=0.001,
            future_return=0.000001,
        ),
    ]

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_accuracy_calculator_accepts_tuple():
    metrics = (
        create_metrics(),
    )

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


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
def test_accuracy_calculator_rejects_invalid_collection(metrics):
    with pytest.raises(TypeError):
        AccuracyCalculator.calculate(metrics)


def test_accuracy_calculator_rejects_empty_list():
    with pytest.raises(ValueError):
        AccuracyCalculator.calculate([])


def test_accuracy_calculator_rejects_empty_tuple():
    with pytest.raises(ValueError):
        AccuracyCalculator.calculate(())


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
def test_accuracy_calculator_rejects_invalid_metric_item(
    invalid_item,
):
    valid = create_metrics()

    with pytest.raises(TypeError):
        AccuracyCalculator.calculate(
            [valid, invalid_item],
        )


def test_accuracy_calculator_rejects_only_neutral_observations():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.60,
            future_return=0.0,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=0.0,
            future_return=0.0,
        ),
    ]

    with pytest.raises(ValueError):
        AccuracyCalculator.calculate(metrics)


def test_accuracy_calculator_accepts_multiple_symbols():
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

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(1.0)


def test_accuracy_calculator_accepts_multiple_horizons():
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

    result = AccuracyCalculator.calculate(metrics)

    assert result == pytest.approx(0.5)
