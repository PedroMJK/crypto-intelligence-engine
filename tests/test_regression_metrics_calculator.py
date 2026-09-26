import math

import pytest

from backend.app.ml.regression_metrics import RegressionMetrics
from backend.app.ml.regression_metrics_calculator import (
    RegressionMetricsCalculator,
)


def test_regression_metrics_calculator_calculates_metrics():
    actual = (
        0.01,
        0.03,
        0.05,
    )
    predicted = (
        0.02,
        0.02,
        0.02,
    )

    metrics = RegressionMetricsCalculator.calculate(
        actual=actual,
        predicted=predicted,
    )

    assert isinstance(
        metrics,
        RegressionMetrics,
    )
    assert metrics.mae == pytest.approx(
        0.016666666666666666
    )
    assert metrics.mse == pytest.approx(
        0.00036666666666666667
    )
    assert metrics.rmse == pytest.approx(
        math.sqrt(
            0.00036666666666666667
        )
    )

def test_regression_metrics_calculator_accepts_lists():
    metrics = RegressionMetricsCalculator.calculate(
        actual=[
            0.01,
            0.03,
        ],
        predicted=[
            0.02,
            0.02,
        ],
    )

    assert metrics.mae == pytest.approx(
        0.01
    )
    assert metrics.mse == pytest.approx(
        0.0001
    )
    assert metrics.rmse == pytest.approx(
        0.01
    )


@pytest.mark.parametrize(
    ("actual", "predicted"),
    [
        (None, [0.01]),
        ("invalid", [0.01]),
        (123, [0.01]),
        (True, [0.01]),
        ([0.01], None),
        ([0.01], "invalid"),
        ([0.01], 123),
        ([0.01], True),
    ],
)
def test_regression_metrics_calculator_rejects_invalid_collections(
    actual,
    predicted,
):
    with pytest.raises(
        TypeError,
        match="actual and predicted must be lists or tuples",
    ):
        RegressionMetricsCalculator.calculate(
            actual=actual,
            predicted=predicted,
        )


@pytest.mark.parametrize(
    ("actual", "predicted"),
    [
        ([], []),
        ((), ()),
    ],
)
def test_regression_metrics_calculator_rejects_empty_collections(
    actual,
    predicted,
):
    with pytest.raises(
        ValueError,
        match="actual and predicted must not be empty",
    ):
        RegressionMetricsCalculator.calculate(
            actual=actual,
            predicted=predicted,
        )


@pytest.mark.parametrize(
    ("actual", "predicted"),
    [
        ([0.01], [0.01, 0.02]),
        ([0.01, 0.02], [0.01]),
    ],
)
def test_regression_metrics_calculator_rejects_different_lengths(
    actual,
    predicted,
):
    with pytest.raises(
        ValueError,
        match="actual and predicted must have the same length",
    ):
        RegressionMetricsCalculator.calculate(
            actual=actual,
            predicted=predicted,
        )


@pytest.mark.parametrize(
    ("actual", "predicted"),
    [
        ([True], [0.01]),
        ([0.01], [False]),
        (["0.01"], [0.01]),
        ([0.01], ["0.01"]),
        ([None], [0.01]),
        ([0.01], [None]),
    ],
)
def test_regression_metrics_calculator_rejects_non_numeric_values(
    actual,
    predicted,
):
    with pytest.raises(
        TypeError,
        match="actual and predicted values must be numbers",
    ):
        RegressionMetricsCalculator.calculate(
            actual=actual,
            predicted=predicted,
        )


@pytest.mark.parametrize(
    ("actual", "predicted"),
    [
        ([math.nan], [0.01]),
        ([math.inf], [0.01]),
        ([-math.inf], [0.01]),
        ([0.01], [math.nan]),
        ([0.01], [math.inf]),
        ([0.01], [-math.inf]),
    ],
)
def test_regression_metrics_calculator_rejects_non_finite_values(
    actual,
    predicted,
):
    with pytest.raises(
        ValueError,
        match="actual and predicted values must be finite",
    ):
        RegressionMetricsCalculator.calculate(
            actual=actual,
            predicted=predicted,
        )
