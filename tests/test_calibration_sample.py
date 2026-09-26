import math

import pytest

from backend.app.ml.calibration_sample import CalibrationSample


def test_calibration_sample_stores_valid_values():
    sample = CalibrationSample(
        horizon_minutes=15,
        predicted_return=0.012,
        observed_return=0.008,
    )

    assert sample.horizon_minutes == 15
    assert sample.predicted_return == 0.012
    assert sample.observed_return == 0.008


def test_calibration_sample_is_immutable():
    sample = CalibrationSample(
        horizon_minutes=15,
        predicted_return=0.012,
        observed_return=0.008,
    )

    with pytest.raises(AttributeError):
        sample.predicted_return = 0.020


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        15.0,
        "15",
        True,
    ],
)
def test_calibration_sample_rejects_invalid_horizon_type(
    horizon_minutes,
):
    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        CalibrationSample(
            horizon_minutes=horizon_minutes,
            predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        0,
        -1,
        -30,
    ],
)
def test_calibration_sample_rejects_non_positive_horizon(
    horizon_minutes,
):
    with pytest.raises(
        ValueError,
        match="horizon_minutes must be greater than zero",
    ):
        CalibrationSample(
            horizon_minutes=horizon_minutes,
            predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "predicted_return",
    [
        None,
        "0.01",
        True,
    ],
)
def test_calibration_sample_rejects_invalid_predicted_return_type(
    predicted_return,
):
    with pytest.raises(
        TypeError,
        match="predicted_return must be a number",
    ):
        CalibrationSample(
            horizon_minutes=15,
            predicted_return=predicted_return,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "predicted_return",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_calibration_sample_rejects_non_finite_predicted_return(
    predicted_return,
):
    with pytest.raises(
        ValueError,
        match="predicted_return must be finite",
    ):
        CalibrationSample(
            horizon_minutes=15,
            predicted_return=predicted_return,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "observed_return",
    [
        None,
        "0.01",
        True,
    ],
)
def test_calibration_sample_rejects_invalid_observed_return_type(
    observed_return,
):
    with pytest.raises(
        TypeError,
        match="observed_return must be a number",
    ):
        CalibrationSample(
            horizon_minutes=15,
            predicted_return=0.012,
            observed_return=observed_return,
        )


@pytest.mark.parametrize(
    "observed_return",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_calibration_sample_rejects_non_finite_observed_return(
    observed_return,
):
    with pytest.raises(
        ValueError,
        match="observed_return must be finite",
    ):
        CalibrationSample(
            horizon_minutes=15,
            predicted_return=0.012,
            observed_return=observed_return,
        )


@pytest.mark.parametrize(
    "predicted_return",
    [
        -2,
        -0.50,
        0,
        0.50,
        2,
    ],
)
def test_calibration_sample_accepts_any_finite_predicted_return(
    predicted_return,
):
    sample = CalibrationSample(
        horizon_minutes=15,
        predicted_return=predicted_return,
        observed_return=0.008,
    )

    assert sample.predicted_return == predicted_return


@pytest.mark.parametrize(
    "observed_return",
    [
        -2,
        -0.50,
        0,
        0.50,
        2,
    ],
)
def test_calibration_sample_accepts_any_finite_observed_return(
    observed_return,
):
    sample = CalibrationSample(
        horizon_minutes=15,
        predicted_return=0.012,
        observed_return=observed_return,
    )

    assert sample.observed_return == observed_return
