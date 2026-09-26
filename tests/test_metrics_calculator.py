import pytest

from backend.app.predictions.metrics_calculator import MetricsCalculator
from backend.app.predictions.prediction_metrics import PredictionMetrics
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


def create_prediction(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "direction_score": 0.80,
    }
    values.update(overrides)

    return PredictionRecord(**values)


def create_outcome(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.50,
        "horizon_minutes": 5,
        "evaluation_timestamp": 1_800_000_300_000,
        "evaluation_price": 0.525,
    }
    values.update(overrides)

    return PredictionOutcome(**values)


def test_metrics_calculator_returns_prediction_metrics():
    metrics = MetricsCalculator.calculate(
        prediction=create_prediction(),
        outcome=create_outcome(),
    )

    assert isinstance(metrics, PredictionMetrics)


def test_metrics_calculator_preserves_prediction_data():
    prediction = create_prediction(
        direction_score=0.75,
    )

    metrics = MetricsCalculator.calculate(
        prediction=prediction,
        outcome=create_outcome(),
    )

    assert metrics.symbol == prediction.symbol
    assert (
        metrics.prediction_timestamp
        == prediction.prediction_timestamp
    )
    assert metrics.direction_score == prediction.direction_score


def test_metrics_calculator_preserves_outcome_horizon():
    metrics = MetricsCalculator.calculate(
        prediction=create_prediction(),
        outcome=create_outcome(
            horizon_minutes=15,
            evaluation_timestamp=1_800_000_900_000,
        ),
    )

    assert metrics.horizon_minutes == 15


def test_metrics_calculator_preserves_future_return():
    outcome = create_outcome(
        reference_price=0.50,
        evaluation_price=0.525,
    )

    metrics = MetricsCalculator.calculate(
        prediction=create_prediction(),
        outcome=outcome,
    )

    assert metrics.future_return == pytest.approx(0.05)


def test_metrics_calculator_calculates_absolute_return():
    outcome = create_outcome(
        evaluation_price=0.475,
    )

    metrics = MetricsCalculator.calculate(
        prediction=create_prediction(),
        outcome=outcome,
    )

    assert metrics.future_return == pytest.approx(-0.05)
    assert metrics.absolute_return == pytest.approx(0.05)


@pytest.mark.parametrize(
    (
        "direction_score",
        "evaluation_price",
        "expected_alignment",
    ),
    [
        (0.80, 0.525, 0.04),
        (0.80, 0.475, -0.04),
        (-0.80, 0.475, 0.04),
        (-0.80, 0.525, -0.04),
        (0.00, 0.525, 0.00),
        (0.80, 0.50, 0.00),
    ],
)
def test_metrics_calculator_calculates_directional_alignment(
    direction_score,
    evaluation_price,
    expected_alignment,
):
    prediction = create_prediction(
        direction_score=direction_score,
    )
    outcome = create_outcome(
        evaluation_price=evaluation_price,
    )

    metrics = MetricsCalculator.calculate(
        prediction=prediction,
        outcome=outcome,
    )

    assert metrics.directional_alignment == pytest.approx(
        expected_alignment
    )


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        {},
        "FETUSDT",
        123,
        True,
    ],
)
def test_metrics_calculator_rejects_non_prediction_record(
    prediction,
):
    with pytest.raises(TypeError):
        MetricsCalculator.calculate(
            prediction=prediction,
            outcome=create_outcome(),
        )


@pytest.mark.parametrize(
    "outcome",
    [
        None,
        {},
        "FETUSDT",
        123,
        True,
    ],
)
def test_metrics_calculator_rejects_non_prediction_outcome(
    outcome,
):
    with pytest.raises(TypeError):
        MetricsCalculator.calculate(
            prediction=create_prediction(),
            outcome=outcome,
        )


def test_metrics_calculator_rejects_symbol_mismatch():
    with pytest.raises(ValueError):
        MetricsCalculator.calculate(
            prediction=create_prediction(
                symbol="FETUSDT",
            ),
            outcome=create_outcome(
                symbol="BTCUSDT",
            ),
        )


def test_metrics_calculator_rejects_prediction_timestamp_mismatch():
    with pytest.raises(ValueError):
        MetricsCalculator.calculate(
            prediction=create_prediction(
                prediction_timestamp=1_800_000_000_000,
            ),
            outcome=create_outcome(
                prediction_timestamp=1_800_000_001_000,
            ),
        )


def test_metrics_calculator_rejects_reference_price_mismatch():
    with pytest.raises(ValueError):
        MetricsCalculator.calculate(
            prediction=create_prediction(
                reference_price=0.50,
            ),
            outcome=create_outcome(
                reference_price=0.51,
            ),
        )
