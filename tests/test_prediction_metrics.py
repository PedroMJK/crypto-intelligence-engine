import math

import pytest

from backend.app.predictions.prediction_metrics import PredictionMetrics


def create_metrics(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "horizon_minutes": 5,
        "direction_score": 0.80,
        "future_return": 0.05,
        "directional_alignment": 0.04,
        "absolute_return": 0.05,
    }
    values.update(overrides)

    return PredictionMetrics(**values)


def test_prediction_metrics_preserves_values():
    metrics = create_metrics()

    assert metrics.symbol == "FETUSDT"
    assert metrics.prediction_timestamp == 1_800_000_000_000
    assert metrics.horizon_minutes == 5
    assert metrics.direction_score == 0.80
    assert metrics.future_return == 0.05
    assert metrics.directional_alignment == 0.04
    assert metrics.absolute_return == 0.05


def test_prediction_metrics_is_immutable():
    metrics = create_metrics()

    with pytest.raises(AttributeError):
        metrics.future_return = 0.10


@pytest.mark.parametrize(
    "symbol",
    [
        None,
        123,
        True,
        [],
        {},
    ],
)
def test_prediction_metrics_rejects_non_string_symbol(symbol):
    with pytest.raises(TypeError):
        create_metrics(symbol=symbol)


def test_prediction_metrics_rejects_empty_symbol():
    with pytest.raises(ValueError):
        create_metrics(symbol="")


@pytest.mark.parametrize(
    "prediction_timestamp",
    [
        None,
        1.5,
        "1800000000000",
        True,
    ],
)
def test_prediction_metrics_rejects_non_integer_prediction_timestamp(
    prediction_timestamp,
):
    with pytest.raises(TypeError):
        create_metrics(
            prediction_timestamp=prediction_timestamp,
        )


def test_prediction_metrics_rejects_negative_prediction_timestamp():
    with pytest.raises(ValueError):
        create_metrics(prediction_timestamp=-1)


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        1.5,
        "5",
        True,
    ],
)
def test_prediction_metrics_rejects_non_integer_horizon_minutes(
    horizon_minutes,
):
    with pytest.raises(TypeError):
        create_metrics(horizon_minutes=horizon_minutes)


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
    ],
)
def test_prediction_metrics_rejects_non_positive_horizon_minutes(
    horizon_minutes,
):
    with pytest.raises(ValueError):
        create_metrics(horizon_minutes=horizon_minutes)


@pytest.mark.parametrize(
    "direction_score",
    [
        None,
        "0.5",
        True,
    ],
)
def test_prediction_metrics_rejects_non_numeric_direction_score(
    direction_score,
):
    with pytest.raises(TypeError):
        create_metrics(direction_score=direction_score)


@pytest.mark.parametrize(
    "direction_score",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_prediction_metrics_rejects_non_finite_direction_score(
    direction_score,
):
    with pytest.raises(ValueError):
        create_metrics(direction_score=direction_score)


@pytest.mark.parametrize(
    "direction_score",
    [
        -1.01,
        1.01,
    ],
)
def test_prediction_metrics_rejects_direction_score_outside_range(
    direction_score,
):
    with pytest.raises(ValueError):
        create_metrics(direction_score=direction_score)


@pytest.mark.parametrize(
    "field_name",
    [
        "future_return",
        "directional_alignment",
        "absolute_return",
    ],
)
@pytest.mark.parametrize(
    "value",
    [
        None,
        "0.05",
        True,
    ],
)
def test_prediction_metrics_rejects_non_numeric_metric(
    field_name,
    value,
):
    with pytest.raises(TypeError):
        create_metrics(**{field_name: value})


@pytest.mark.parametrize(
    "field_name",
    [
        "future_return",
        "directional_alignment",
        "absolute_return",
    ],
)
@pytest.mark.parametrize(
    "value",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_prediction_metrics_rejects_non_finite_metric(
    field_name,
    value,
):
    with pytest.raises(ValueError):
        create_metrics(**{field_name: value})


def test_prediction_metrics_rejects_negative_absolute_return():
    with pytest.raises(ValueError):
        create_metrics(absolute_return=-0.01)
