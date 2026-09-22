import pytest

from backend.app.analysis.pressure_score import PressureScore


def test_pressure_score_returns_positive_score_for_buying_pressure():
    pressure_score = PressureScore()

    result = pressure_score.calculate(
        flow_signal=0.8,
        momentum_signal=0.4,
        volume_signal=0.6,
    )

    assert result == pytest.approx(0.6)


def test_pressure_score_returns_negative_score_for_selling_pressure():
    pressure_score = PressureScore()

    result = pressure_score.calculate(
        flow_signal=-0.8,
        momentum_signal=-0.4,
        volume_signal=-0.6,
    )

    assert result == pytest.approx(-0.6)


def test_pressure_score_returns_zero_for_balanced_signals():
    pressure_score = PressureScore()

    result = pressure_score.calculate(
        flow_signal=0.0,
        momentum_signal=0.0,
        volume_signal=0.0,
    )

    assert result == 0.0


def test_pressure_score_combines_conflicting_signals():
    pressure_score = PressureScore()

    result = pressure_score.calculate(
        flow_signal=0.9,
        momentum_signal=-0.6,
        volume_signal=0.3,
    )

    assert result == pytest.approx(0.2)


@pytest.mark.parametrize(
    "signal_name, signal_value",
    [
        ("flow_signal", 1.1),
        ("flow_signal", -1.1),
        ("momentum_signal", 1.1),
        ("momentum_signal", -1.1),
        ("volume_signal", 1.1),
        ("volume_signal", -1.1),
    ],
)
def test_pressure_score_rejects_signals_outside_normalized_range(
    signal_name,
    signal_value,
):
    pressure_score = PressureScore()

    signals = {
        "flow_signal": 0.0,
        "momentum_signal": 0.0,
        "volume_signal": 0.0,
    }
    signals[signal_name] = signal_value

    with pytest.raises(
        ValueError,
        match=f"{signal_name} must be between -1.0 and 1.0",
    ):
        pressure_score.calculate(**signals)
