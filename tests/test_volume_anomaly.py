import pytest

from backend.app.analysis.volume_anomaly import VolumeAnomaly


def test_volume_anomaly_returns_ratio_above_baseline():
    volume_anomaly = VolumeAnomaly()

    result = volume_anomaly.calculate(
        current_volume=200.0,
        baseline_volume=100.0,
    )

    assert result == 2.0


def test_volume_anomaly_returns_one_when_volume_matches_baseline():
    volume_anomaly = VolumeAnomaly()

    result = volume_anomaly.calculate(
        current_volume=100.0,
        baseline_volume=100.0,
    )

    assert result == 1.0


def test_volume_anomaly_returns_ratio_below_baseline():
    volume_anomaly = VolumeAnomaly()

    result = volume_anomaly.calculate(
        current_volume=50.0,
        baseline_volume=100.0,
    )

    assert result == 0.5


def test_volume_anomaly_accepts_zero_current_volume():
    volume_anomaly = VolumeAnomaly()

    result = volume_anomaly.calculate(
        current_volume=0.0,
        baseline_volume=100.0,
    )

    assert result == 0.0


def test_volume_anomaly_rejects_negative_current_volume():
    volume_anomaly = VolumeAnomaly()

    with pytest.raises(
        ValueError,
        match="current_volume cannot be negative",
    ):
        volume_anomaly.calculate(
            current_volume=-1.0,
            baseline_volume=100.0,
        )


def test_volume_anomaly_rejects_zero_baseline_volume():
    volume_anomaly = VolumeAnomaly()

    with pytest.raises(
        ValueError,
        match="baseline_volume must be greater than zero",
    ):
        volume_anomaly.calculate(
            current_volume=100.0,
            baseline_volume=0.0,
        )


def test_volume_anomaly_rejects_negative_baseline_volume():
    volume_anomaly = VolumeAnomaly()

    with pytest.raises(
        ValueError,
        match="baseline_volume must be greater than zero",
    ):
        volume_anomaly.calculate(
            current_volume=100.0,
            baseline_volume=-1.0,
        )
