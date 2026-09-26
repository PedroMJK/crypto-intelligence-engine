import math
from unittest.mock import Mock

import pytest

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.calibration_sample import CalibrationSample
from backend.app.ml.probability_calibration_evaluator import (
    ProbabilityCalibrationEvaluator,
)
from backend.app.ml.probability_calibration_metrics import (
    ProbabilityCalibrationMetrics,
)
from backend.app.ml.return_probability_calibrator import (
    ReturnProbabilityCalibrator,
)


def create_sample(
    *,
    horizon_minutes: int = 15,
    predicted_return: float = 0.01,
    observed_return: float = 0.01,
) -> CalibrationSample:
    return CalibrationSample(
        horizon_minutes=horizon_minutes,
        predicted_return=predicted_return,
        observed_return=observed_return,
    )


def create_fitted_calibrator() -> ReturnProbabilityCalibrator:
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.04,
                observed_return=-0.03,
            ),
            create_sample(
                predicted_return=-0.02,
                observed_return=-0.01,
            ),
            create_sample(
                predicted_return=0.02,
                observed_return=0.01,
            ),
            create_sample(
                predicted_return=0.04,
                observed_return=0.03,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(dataset)

    return calibrator


def test_evaluate_returns_metrics_per_horizon():
    calibrator = create_fitted_calibrator()

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                predicted_return=0.03,
                observed_return=0.02,
            ),
        ]
    )

    result = ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    assert set(result.keys()) == {15}
    assert isinstance(
        result[15],
        ProbabilityCalibrationMetrics,
    )


def test_evaluate_calculates_expected_metrics():
    calibrator = Mock(
        spec=ReturnProbabilityCalibrator
    )
    calibrator.predict_probability.side_effect = [
        0.20,
        0.80,
    ]

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                predicted_return=0.03,
                observed_return=0.02,
            ),
        ]
    )

    result = ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    metrics = result[15]

    expected_brier_score = 0.04
    expected_log_loss = -math.log(0.80)

    assert metrics.brier_score == pytest.approx(
        expected_brier_score
    )
    assert metrics.log_loss == pytest.approx(
        expected_log_loss
    )


def test_evaluate_groups_metrics_by_horizon():
    calibrator = Mock(
        spec=ReturnProbabilityCalibrator
    )
    calibrator.predict_probability.side_effect = [
        0.20,
        0.80,
        0.30,
        0.70,
    ]

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                horizon_minutes=5,
                predicted_return=0.03,
                observed_return=0.02,
            ),
            create_sample(
                horizon_minutes=30,
                predicted_return=-0.02,
                observed_return=-0.01,
            ),
            create_sample(
                horizon_minutes=30,
                predicted_return=0.02,
                observed_return=0.01,
            ),
        ]
    )

    result = ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    assert set(result.keys()) == {
        5,
        30,
    }

    assert result[5].brier_score == pytest.approx(
        0.04
    )
    assert result[30].brier_score == pytest.approx(
        0.09
    )


def test_evaluate_excludes_zero_observed_returns():
    calibrator = Mock(
        spec=ReturnProbabilityCalibrator
    )
    calibrator.predict_probability.side_effect = [
        0.20,
        0.80,
    ]

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                predicted_return=100.0,
                observed_return=0.0,
            ),
            create_sample(
                predicted_return=0.03,
                observed_return=0.02,
            ),
        ]
    )

    result = ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    assert (
        calibrator.predict_probability.call_count
        == 2
    )
    assert result[15].brier_score == pytest.approx(
        0.04
    )


def test_evaluate_does_not_fit_calibrator():
    calibrator = Mock(
        spec=ReturnProbabilityCalibrator
    )
    calibrator.predict_probability.side_effect = [
        0.20,
        0.80,
    ]

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                predicted_return=0.03,
                observed_return=0.02,
            ),
        ]
    )

    ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    calibrator.fit.assert_not_called()


def test_evaluate_uses_prediction_and_horizon():
    calibrator = Mock(
        spec=ReturnProbabilityCalibrator
    )
    calibrator.predict_probability.return_value = 0.75

    sample = create_sample(
        horizon_minutes=15,
        predicted_return=0.025,
        observed_return=0.01,
    )

    dataset = CalibrationDataset(
        samples=[
            sample,
        ]
    )

    ProbabilityCalibrationEvaluator.evaluate(
        calibrator=calibrator,
        dataset=dataset,
    )

    calibrator.predict_probability.assert_called_once_with(
        predicted_return=0.025,
        horizon_minutes=15,
    )


def test_evaluate_rejects_dataset_with_only_zero_returns():
    calibrator = create_fitted_calibrator()

    dataset = CalibrationDataset(
        samples=[
            create_sample(
                observed_return=0.0,
            ),
            create_sample(
                predicted_return=-0.01,
                observed_return=0.0,
            ),
        ]
    )

    with pytest.raises(
        ValueError,
        match=(
            "dataset must contain at least one "
            "directional observation"
        ),
    ):
        ProbabilityCalibrationEvaluator.evaluate(
            calibrator=calibrator,
            dataset=dataset,
        )


@pytest.mark.parametrize(
    "calibrator",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_evaluate_rejects_invalid_calibrator(
    calibrator,
):
    dataset = CalibrationDataset(
        samples=[
            create_sample(),
        ]
    )

    with pytest.raises(
        TypeError,
        match=(
            "calibrator must be a "
            "ReturnProbabilityCalibrator"
        ),
    ):
        ProbabilityCalibrationEvaluator.evaluate(
            calibrator=calibrator,
            dataset=dataset,
        )


@pytest.mark.parametrize(
    "dataset",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_evaluate_rejects_invalid_dataset(
    dataset,
):
    calibrator = create_fitted_calibrator()

    with pytest.raises(
        TypeError,
        match="dataset must be a CalibrationDataset",
    ):
        ProbabilityCalibrationEvaluator.evaluate(
            calibrator=calibrator,
            dataset=dataset,
        )
