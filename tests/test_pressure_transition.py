import pytest

from backend.app.analysis.pressure_transition import PressureTransition


def test_pressure_transition_returns_positive_change():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=0.2,
        current_score=0.7,
    )

    assert result == pytest.approx(0.5)


def test_pressure_transition_returns_negative_change():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=0.7,
        current_score=0.2,
    )

    assert result == pytest.approx(-0.5)


def test_pressure_transition_returns_zero_when_pressure_does_not_change():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=0.4,
        current_score=0.4,
    )

    assert result == 0.0


def test_pressure_transition_detects_change_from_selling_to_buying():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=-0.4,
        current_score=0.4,
    )

    assert result == pytest.approx(0.8)


def test_pressure_transition_detects_change_from_buying_to_selling():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=0.4,
        current_score=-0.4,
    )

    assert result == pytest.approx(-0.8)


def test_pressure_transition_supports_maximum_positive_change():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=-1.0,
        current_score=1.0,
    )

    assert result == pytest.approx(2.0)


def test_pressure_transition_supports_maximum_negative_change():
    pressure_transition = PressureTransition()

    result = pressure_transition.calculate(
        previous_score=1.0,
        current_score=-1.0,
    )

    assert result == pytest.approx(-2.0)


@pytest.mark.parametrize(
    "score_name, score_value",
    [
        ("previous_score", 1.1),
        ("previous_score", -1.1),
        ("current_score", 1.1),
        ("current_score", -1.1),
    ],
)
def test_pressure_transition_rejects_scores_outside_normalized_range(
    score_name,
    score_value,
):
    pressure_transition = PressureTransition()

    scores = {
        "previous_score": 0.0,
        "current_score": 0.0,
    }
    scores[score_name] = score_value

    with pytest.raises(
        ValueError,
        match=f"{score_name} must be between -1.0 and 1.0",
    ):
        pressure_transition.calculate(**scores)
