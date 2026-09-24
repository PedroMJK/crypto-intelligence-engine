import pytest

from backend.app.analysis.anomaly_detector import AnomalyDetector


def test_anomaly_detector_returns_statistical_context():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[80.0, 90.0, 100.0, 110.0, 120.0],
        current_value=130.0,
    )

    assert result["current_value"] == 130.0
    assert result["mean"] == pytest.approx(100.0)
    assert result["standard_deviation"] == pytest.approx(
        14.142135623730951
    )
    assert result["deviation"] == pytest.approx(30.0)
    assert result["z_score"] == pytest.approx(
        2.1213203435596424
    )


def test_anomaly_detector_returns_positive_z_score_above_mean():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[80.0, 90.0, 100.0, 110.0, 120.0],
        current_value=120.0,
    )

    assert result["z_score"] > 0


def test_anomaly_detector_returns_negative_z_score_below_mean():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[80.0, 90.0, 100.0, 110.0, 120.0],
        current_value=70.0,
    )

    assert result["z_score"] < 0


def test_anomaly_detector_returns_zero_z_score_at_mean():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[80.0, 90.0, 100.0, 110.0, 120.0],
        current_value=100.0,
    )

    assert result["z_score"] == pytest.approx(0.0)
    assert result["deviation"] == pytest.approx(0.0)


def test_anomaly_detector_uses_population_standard_deviation():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[1.0, 2.0, 3.0],
        current_value=4.0,
    )

    assert result["mean"] == pytest.approx(2.0)
    assert result["standard_deviation"] == pytest.approx(
        0.816496580927726
    )
    assert result["z_score"] == pytest.approx(
        2.449489742783178
    )


def test_anomaly_detector_accepts_negative_values():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[-3.0, -2.0, -1.0],
        current_value=-4.0,
    )

    assert result["mean"] == pytest.approx(-2.0)
    assert result["deviation"] == pytest.approx(-2.0)
    assert result["z_score"] < 0


def test_anomaly_detector_accepts_zero_values():
    detector = AnomalyDetector()

    result = detector.analyze(
        historical_values=[-1.0, 0.0, 1.0],
        current_value=0.0,
    )

    assert result["mean"] == pytest.approx(0.0)
    assert result["z_score"] == pytest.approx(0.0)


def test_anomaly_detector_rejects_empty_history():
    detector = AnomalyDetector()

    with pytest.raises(
        ValueError,
        match="historical values must not be empty",
    ):
        detector.analyze(
            historical_values=[],
            current_value=100.0,
        )


def test_anomaly_detector_rejects_constant_history():
    detector = AnomalyDetector()

    with pytest.raises(
        ValueError,
        match="historical standard deviation must be greater than zero",
    ):
        detector.analyze(
            historical_values=[100.0, 100.0, 100.0],
            current_value=110.0,
        )


def test_anomaly_detector_rejects_non_list_history():
    detector = AnomalyDetector()

    with pytest.raises(
        TypeError,
        match="historical values must be a list",
    ):
        detector.analyze(
            historical_values=(80.0, 90.0, 100.0),
            current_value=110.0,
        )


def test_anomaly_detector_rejects_non_numeric_historical_value():
    detector = AnomalyDetector()

    with pytest.raises(
        TypeError,
        match="historical values must contain only numbers",
    ):
        detector.analyze(
            historical_values=[80.0, "90", 100.0],
            current_value=110.0,
        )


def test_anomaly_detector_rejects_non_numeric_current_value():
    detector = AnomalyDetector()

    with pytest.raises(
        TypeError,
        match="current value must be a number",
    ):
        detector.analyze(
            historical_values=[80.0, 90.0, 100.0],
            current_value="110",
        )


def test_anomaly_detector_does_not_modify_history():
    detector = AnomalyDetector()
    historical_values = [
        80.0,
        90.0,
        100.0,
        110.0,
        120.0,
    ]
    original_values = historical_values.copy()

    detector.analyze(
        historical_values=historical_values,
        current_value=130.0,
    )

    assert historical_values == original_values


def test_anomaly_detector_is_deterministic():
    detector = AnomalyDetector()
    historical_values = [
        80.0,
        90.0,
        100.0,
        110.0,
        120.0,
    ]

    first_result = detector.analyze(
        historical_values=historical_values,
        current_value=130.0,
    )
    second_result = detector.analyze(
        historical_values=historical_values,
        current_value=130.0,
    )

    assert first_result == second_result
