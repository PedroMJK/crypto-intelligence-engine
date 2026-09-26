import math

import pytest

from backend.app.ml.model_comparison_sample import (
    ModelComparisonSample,
)


def test_model_comparison_sample_stores_valid_values():
    sample = ModelComparisonSample(
        horizon_minutes=15,
        traditional_direction_score=0.60,
        ml_predicted_return=0.012,
        observed_return=0.008,
    )

    assert sample.horizon_minutes == 15
    assert sample.traditional_direction_score == 0.60
    assert sample.ml_predicted_return == 0.012
    assert sample.observed_return == 0.008


def test_model_comparison_sample_is_immutable():
    sample = ModelComparisonSample(
        horizon_minutes=15,
        traditional_direction_score=0.60,
        ml_predicted_return=0.012,
        observed_return=0.008,
    )

    with pytest.raises(AttributeError):
        sample.ml_predicted_return = 0.020


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        15.0,
        "15",
        True,
    ],
)
def test_model_comparison_sample_rejects_invalid_horizon_type(
    horizon_minutes,
):
    with pytest.raises(
        TypeError,
        match="horizon_minutes must be an int",
    ):
        ModelComparisonSample(
            horizon_minutes=horizon_minutes,
            traditional_direction_score=0.60,
            ml_predicted_return=0.012,
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
def test_model_comparison_sample_rejects_non_positive_horizon(
    horizon_minutes,
):
    with pytest.raises(
        ValueError,
        match="horizon_minutes must be greater than zero",
    ):
        ModelComparisonSample(
            horizon_minutes=horizon_minutes,
            traditional_direction_score=0.60,
            ml_predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "traditional_direction_score",
    [
        None,
        "0.5",
        True,
    ],
)
def test_model_comparison_sample_rejects_invalid_traditional_score_type(
    traditional_direction_score,
):
    with pytest.raises(
        TypeError,
        match="traditional_direction_score must be a number",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=traditional_direction_score,
            ml_predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "traditional_direction_score",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_model_comparison_sample_rejects_non_finite_traditional_score(
    traditional_direction_score,
):
    with pytest.raises(
        ValueError,
        match="traditional_direction_score must be finite",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=traditional_direction_score,
            ml_predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "traditional_direction_score",
    [
        -1.01,
        -2.0,
        1.01,
        2.0,
    ],
)
def test_model_comparison_sample_rejects_traditional_score_outside_range(
    traditional_direction_score,
):
    with pytest.raises(
        ValueError,
        match=(
            "traditional_direction_score must be between "
            "-1 and 1"
        ),
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=traditional_direction_score,
            ml_predicted_return=0.012,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "traditional_direction_score",
    [
        -1.0,
        -0.50,
        0.0,
        0.50,
        1.0,
    ],
)
def test_model_comparison_sample_accepts_traditional_score_range(
    traditional_direction_score,
):
    sample = ModelComparisonSample(
        horizon_minutes=15,
        traditional_direction_score=traditional_direction_score,
        ml_predicted_return=0.012,
        observed_return=0.008,
    )

    assert (
        sample.traditional_direction_score
        == traditional_direction_score
    )


@pytest.mark.parametrize(
    "ml_predicted_return",
    [
        None,
        "0.01",
        True,
    ],
)
def test_model_comparison_sample_rejects_invalid_ml_prediction_type(
    ml_predicted_return,
):
    with pytest.raises(
        TypeError,
        match="ml_predicted_return must be a number",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=0.60,
            ml_predicted_return=ml_predicted_return,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "ml_predicted_return",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_model_comparison_sample_rejects_non_finite_ml_prediction(
    ml_predicted_return,
):
    with pytest.raises(
        ValueError,
        match="ml_predicted_return must be finite",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=0.60,
            ml_predicted_return=ml_predicted_return,
            observed_return=0.008,
        )


@pytest.mark.parametrize(
    "ml_predicted_return",
    [
        -2.0,
        -0.50,
        0.0,
        0.50,
        2.0,
    ],
)
def test_model_comparison_sample_accepts_any_finite_ml_prediction(
    ml_predicted_return,
):
    sample = ModelComparisonSample(
        horizon_minutes=15,
        traditional_direction_score=0.60,
        ml_predicted_return=ml_predicted_return,
        observed_return=0.008,
    )

    assert sample.ml_predicted_return == ml_predicted_return


@pytest.mark.parametrize(
    "observed_return",
    [
        None,
        "0.01",
        True,
    ],
)
def test_model_comparison_sample_rejects_invalid_observed_return_type(
    observed_return,
):
    with pytest.raises(
        TypeError,
        match="observed_return must be a number",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=0.60,
            ml_predicted_return=0.012,
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
def test_model_comparison_sample_rejects_non_finite_observed_return(
    observed_return,
):
    with pytest.raises(
        ValueError,
        match="observed_return must be finite",
    ):
        ModelComparisonSample(
            horizon_minutes=15,
            traditional_direction_score=0.60,
            ml_predicted_return=0.012,
            observed_return=observed_return,
        )


@pytest.mark.parametrize(
    "observed_return",
    [
        -2.0,
        -0.50,
        0.0,
        0.50,
        2.0,
    ],
)
def test_model_comparison_sample_accepts_any_finite_observed_return(
    observed_return,
):
    sample = ModelComparisonSample(
        horizon_minutes=15,
        traditional_direction_score=0.60,
        ml_predicted_return=0.012,
        observed_return=observed_return,
    )

    assert sample.observed_return == observed_return
