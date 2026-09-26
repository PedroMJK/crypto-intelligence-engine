import pytest

from backend.app.predictions.prediction_metrics import PredictionMetrics
from backend.app.predictions.statistical_report import StatisticalReport
from backend.app.predictions.statistical_report_generator import (
    StatisticalReportGenerator,
)


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


def test_statistical_report_generator_returns_statistical_report():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(),
        ]
    )

    assert isinstance(report, StatisticalReport)


def test_statistical_report_generator_preserves_horizon():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(horizon_minutes=15),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                horizon_minutes=15,
            ),
        ]
    )

    assert report.horizon_minutes == 15


def test_statistical_report_generator_counts_samples():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_002_000,
            ),
        ]
    )

    assert report.sample_count == 3


def test_statistical_report_generator_calculates_mean_direction_score():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                direction_score=0.80,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                direction_score=0.20,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_002_000,
                direction_score=-0.40,
            ),
        ]
    )

    assert report.mean_direction_score == pytest.approx(0.20)


def test_statistical_report_generator_calculates_mean_future_return():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                future_return=0.05,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                future_return=-0.02,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_002_000,
                future_return=0.00,
            ),
        ]
    )

    assert report.mean_future_return == pytest.approx(0.01)


def test_statistical_report_generator_calculates_mean_absolute_return():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                absolute_return=0.05,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                absolute_return=0.02,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_002_000,
                absolute_return=0.00,
            ),
        ]
    )

    assert report.mean_absolute_return == pytest.approx(
        0.07 / 3
    )


def test_statistical_report_generator_calculates_mean_directional_alignment():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                directional_alignment=0.04,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                directional_alignment=-0.01,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_002_000,
                directional_alignment=0.00,
            ),
        ]
    )

    assert report.mean_directional_alignment == pytest.approx(
        0.01
    )


def test_statistical_report_generator_handles_single_sample():
    metrics = create_metrics(
        horizon_minutes=30,
        direction_score=-0.50,
        future_return=-0.04,
        absolute_return=0.04,
        directional_alignment=0.02,
    )

    report = StatisticalReportGenerator.generate(
        [metrics]
    )

    assert report.horizon_minutes == 30
    assert report.sample_count == 1
    assert report.mean_direction_score == pytest.approx(-0.50)
    assert report.mean_future_return == pytest.approx(-0.04)
    assert report.mean_absolute_return == pytest.approx(0.04)
    assert report.mean_directional_alignment == pytest.approx(0.02)


def test_statistical_report_generator_does_not_derive_absolute_return_from_mean():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                future_return=0.10,
                absolute_return=0.10,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                future_return=-0.10,
                absolute_return=0.10,
            ),
        ]
    )

    assert report.mean_future_return == pytest.approx(0.00)
    assert report.mean_absolute_return == pytest.approx(0.10)


def test_statistical_report_generator_does_not_derive_alignment_from_means():
    report = StatisticalReportGenerator.generate(
        [
            create_metrics(
                direction_score=1.0,
                future_return=0.10,
                directional_alignment=0.10,
            ),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
                direction_score=-1.0,
                future_return=-0.10,
                directional_alignment=0.10,
            ),
        ]
    )

    assert report.mean_direction_score == pytest.approx(0.00)
    assert report.mean_future_return == pytest.approx(0.00)
    assert report.mean_directional_alignment == pytest.approx(0.10)


def test_statistical_report_generator_rejects_empty_collection():
    with pytest.raises(ValueError):
        StatisticalReportGenerator.generate([])


@pytest.mark.parametrize(
    "metrics",
    [
        None,
        123,
        True,
        "metrics",
        {},
    ],
)
def test_statistical_report_generator_rejects_invalid_collection(
    metrics,
):
    with pytest.raises(TypeError):
        StatisticalReportGenerator.generate(metrics)


@pytest.mark.parametrize(
    "invalid_metric",
    [
        None,
        123,
        True,
        "metric",
        {},
    ],
)
def test_statistical_report_generator_rejects_non_prediction_metrics(
    invalid_metric,
):
    with pytest.raises(TypeError):
        StatisticalReportGenerator.generate(
            [
                create_metrics(),
                invalid_metric,
            ]
        )


def test_statistical_report_generator_rejects_mixed_horizons():
    with pytest.raises(ValueError):
        StatisticalReportGenerator.generate(
            [
                create_metrics(
                    horizon_minutes=5,
                ),
                create_metrics(
                    prediction_timestamp=1_800_000_001_000,
                    horizon_minutes=15,
                ),
            ]
        )


def test_statistical_report_generator_accepts_tuple():
    report = StatisticalReportGenerator.generate(
        (
            create_metrics(),
            create_metrics(
                prediction_timestamp=1_800_000_001_000,
            ),
        )
    )

    assert report.sample_count == 2
