import math

import pytest

from backend.app.predictions.statistical_report import StatisticalReport


def create_report(**overrides):
    values = {
        "horizon_minutes": 5,
        "sample_count": 10,
        "mean_direction_score": 0.20,
        "mean_future_return": 0.01,
        "mean_absolute_return": 0.03,
        "mean_directional_alignment": 0.004,
    }
    values.update(overrides)

    return StatisticalReport(**values)


def test_statistical_report_preserves_values():
    report = create_report()

    assert report.horizon_minutes == 5
    assert report.sample_count == 10
    assert report.mean_direction_score == 0.20
    assert report.mean_future_return == 0.01
    assert report.mean_absolute_return == 0.03
    assert report.mean_directional_alignment == 0.004


def test_statistical_report_is_immutable():
    report = create_report()

    with pytest.raises(AttributeError):
        report.sample_count = 20


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        1.5,
        "5",
        True,
    ],
)
def test_statistical_report_rejects_non_integer_horizon_minutes(
    horizon_minutes,
):
    with pytest.raises(TypeError):
        create_report(horizon_minutes=horizon_minutes)


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
    ],
)
def test_statistical_report_rejects_non_positive_horizon_minutes(
    horizon_minutes,
):
    with pytest.raises(ValueError):
        create_report(horizon_minutes=horizon_minutes)


@pytest.mark.parametrize(
    "sample_count",
    [
        None,
        1.5,
        "10",
        True,
    ],
)
def test_statistical_report_rejects_non_integer_sample_count(
    sample_count,
):
    with pytest.raises(TypeError):
        create_report(sample_count=sample_count)


@pytest.mark.parametrize(
    "sample_count",
    [
        0,
        -1,
    ],
)
def test_statistical_report_rejects_non_positive_sample_count(
    sample_count,
):
    with pytest.raises(ValueError):
        create_report(sample_count=sample_count)


@pytest.mark.parametrize(
    "field_name",
    [
        "mean_direction_score",
        "mean_future_return",
        "mean_absolute_return",
        "mean_directional_alignment",
    ],
)
@pytest.mark.parametrize(
    "value",
    [
        None,
        "0.01",
        True,
    ],
)
def test_statistical_report_rejects_non_numeric_mean(
    field_name,
    value,
):
    with pytest.raises(TypeError):
        create_report(**{field_name: value})


@pytest.mark.parametrize(
    "field_name",
    [
        "mean_direction_score",
        "mean_future_return",
        "mean_absolute_return",
        "mean_directional_alignment",
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
def test_statistical_report_rejects_non_finite_mean(
    field_name,
    value,
):
    with pytest.raises(ValueError):
        create_report(**{field_name: value})


@pytest.mark.parametrize(
    "mean_direction_score",
    [
        -1.01,
        1.01,
    ],
)
def test_statistical_report_rejects_mean_direction_score_outside_range(
    mean_direction_score,
):
    with pytest.raises(ValueError):
        create_report(
            mean_direction_score=mean_direction_score,
        )


def test_statistical_report_accepts_direction_score_boundaries():
    lower_report = create_report(
        mean_direction_score=-1.0,
    )
    upper_report = create_report(
        mean_direction_score=1.0,
    )

    assert lower_report.mean_direction_score == -1.0
    assert upper_report.mean_direction_score == 1.0


def test_statistical_report_rejects_negative_mean_absolute_return():
    with pytest.raises(ValueError):
        create_report(
            mean_absolute_return=-0.01,
        )


def test_statistical_report_accepts_zero_means():
    report = create_report(
        mean_direction_score=0.0,
        mean_future_return=0.0,
        mean_absolute_return=0.0,
        mean_directional_alignment=0.0,
    )

    assert report.mean_direction_score == 0.0
    assert report.mean_future_return == 0.0
    assert report.mean_absolute_return == 0.0
    assert report.mean_directional_alignment == 0.0
