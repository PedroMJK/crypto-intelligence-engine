import math

import pytest

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.calibration_sample import CalibrationSample
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


def create_valid_dataset() -> CalibrationDataset:
    return CalibrationDataset(
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


def test_fit_and_predict_probability():
    calibrator = ReturnProbabilityCalibrator()

    calibrator.fit(
        create_valid_dataset()
    )

    probability = calibrator.predict_probability(
        predicted_return=0.03,
        horizon_minutes=15,
    )

    assert isinstance(
        probability,
        float,
    )
    assert 0.0 <= probability <= 1.0


def test_probability_increases_for_more_positive_prediction():
    calibrator = ReturnProbabilityCalibrator()

    calibrator.fit(
        create_valid_dataset()
    )

    negative_probability = (
        calibrator.predict_probability(
            predicted_return=-0.03,
            horizon_minutes=15,
        )
    )
    positive_probability = (
        calibrator.predict_probability(
            predicted_return=0.03,
            horizon_minutes=15,
        )
    )

    assert (
        positive_probability
        > negative_probability
    )


def test_fit_trains_independent_calibrators_per_horizon():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
                predicted_return=-0.04,
                observed_return=-0.02,
            ),
            create_sample(
                horizon_minutes=5,
                predicted_return=0.04,
                observed_return=0.02,
            ),
            create_sample(
                horizon_minutes=30,
                predicted_return=-0.03,
                observed_return=0.02,
            ),
            create_sample(
                horizon_minutes=30,
                predicted_return=0.03,
                observed_return=-0.02,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(dataset)

    probability_5 = calibrator.predict_probability(
        predicted_return=0.03,
        horizon_minutes=5,
    )
    probability_30 = calibrator.predict_probability(
        predicted_return=0.03,
        horizon_minutes=30,
    )

    assert probability_5 > 0.5
    assert probability_30 < 0.5


def test_fit_excludes_zero_observed_returns():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.04,
                observed_return=-0.02,
            ),
            create_sample(
                predicted_return=0.04,
                observed_return=0.02,
            ),
            create_sample(
                predicted_return=100.0,
                observed_return=0.0,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(dataset)

    probability = calibrator.predict_probability(
        predicted_return=0.04,
        horizon_minutes=15,
    )

    assert probability > 0.5


def test_fit_accepts_multiple_horizons():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
                predicted_return=-0.02,
                observed_return=-0.01,
            ),
            create_sample(
                horizon_minutes=5,
                predicted_return=0.02,
                observed_return=0.01,
            ),
            create_sample(
                horizon_minutes=15,
                predicted_return=-0.03,
                observed_return=-0.02,
            ),
            create_sample(
                horizon_minutes=15,
                predicted_return=0.03,
                observed_return=0.02,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(dataset)

    probability_5 = calibrator.predict_probability(
        predicted_return=0.01,
        horizon_minutes=5,
    )
    probability_15 = calibrator.predict_probability(
        predicted_return=0.01,
        horizon_minutes=15,
    )

    assert 0.0 <= probability_5 <= 1.0
    assert 0.0 <= probability_15 <= 1.0


def test_fit_rejects_horizon_without_negative_observation():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=0.01,
                observed_return=0.01,
            ),
            create_sample(
                predicted_return=0.02,
                observed_return=0.02,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()

    with pytest.raises(
        ValueError,
        match=(
            "each horizon must contain both positive "
            "and negative observed returns"
        ),
    ):
        calibrator.fit(dataset)


def test_fit_rejects_horizon_without_positive_observation():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.01,
                observed_return=-0.01,
            ),
            create_sample(
                predicted_return=-0.02,
                observed_return=-0.02,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()

    with pytest.raises(
        ValueError,
        match=(
            "each horizon must contain both positive "
            "and negative observed returns"
        ),
    ):
        calibrator.fit(dataset)


def test_fit_rejects_horizon_with_only_zero_observations():
    dataset = CalibrationDataset(
        samples=[
            create_sample(
                predicted_return=-0.01,
                observed_return=0.0,
            ),
            create_sample(
                predicted_return=0.01,
                observed_return=0.0,
            ),
        ]
    )

    calibrator = ReturnProbabilityCalibrator()

    with pytest.raises(
        ValueError,
        match=(
            "each horizon must contain both positive "
            "and negative observed returns"
        ),
    ):
        calibrator.fit(dataset)


def test_fit_rejects_invalid_dataset():
    calibrator = ReturnProbabilityCalibrator()

    with pytest.raises(
        TypeError,
        match="dataset must be a CalibrationDataset",
    ):
        calibrator.fit(
            "invalid"
        )


def test_predict_probability_rejects_before_fit():
    calibrator = ReturnProbabilityCalibrator()

    with pytest.raises(
        RuntimeError,
        match=(
            "calibrator must be fitted before prediction"
        ),
    ):
        calibrator.predict_probability(
            predicted_return=0.01,
            horizon_minutes=15,
        )


@pytest.mark.parametrize(
    "predicted_return",
    [
        None,
        "0.01",
        True,
    ],
)
def test_predict_probability_rejects_invalid_prediction_type(
    predicted_return,
):
    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(
        create_valid_dataset()
    )

    with pytest.raises(
        TypeError,
        match="predicted_return must be a number",
    ):
        calibrator.predict_probability(
            predicted_return=predicted_return,
            horizon_minutes=15,
        )


@pytest.mark.parametrize(
    "predicted_return",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_predict_probability_rejects_non_finite_prediction(
    predicted_return,
):
    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(
        create_valid_dataset()
    )

    with pytest.raises(
        ValueError,
        match="predicted_return must be finite",
    ):
        calibrator.predict_probability(
            predicted_return=predicted_return,
            horizon_minutes=15,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        15.0,
        "15",
        True,
    ],
)
def test_predict_probability_rejects_invalid_horizon_type(
    horizon_minutes,
):
    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(
        create_valid_dataset()
    )

    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        calibrator.predict_probability(
            predicted_return=0.01,
            horizon_minutes=horizon_minutes,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
        -15,
    ],
)
def test_predict_probability_rejects_non_positive_horizon(
    horizon_minutes,
):
    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(
        create_valid_dataset()
    )

    with pytest.raises(
        ValueError,
        match=(
            "horizon_minutes must be greater than zero"
        ),
    ):
        calibrator.predict_probability(
            predicted_return=0.01,
            horizon_minutes=horizon_minutes,
        )


def test_predict_probability_rejects_unknown_horizon():
    calibrator = ReturnProbabilityCalibrator()
    calibrator.fit(
        create_valid_dataset()
    )

    with pytest.raises(
        ValueError,
        match=(
            "horizon_minutes was not observed during calibration"
        ),
    ):
        calibrator.predict_probability(
            predicted_return=0.01,
            horizon_minutes=30,
        )
