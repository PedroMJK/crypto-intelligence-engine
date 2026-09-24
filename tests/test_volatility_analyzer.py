import pytest

from backend.app.analysis.volatility_analyzer import (
    VolatilityAnalyzer,
)


def test_volatility_analyzer_detects_expanding_volatility():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[2.0, 2.0, 2.0, 3.0],
        lookback=3,
    )

    assert result == {
        "current_atr": 3.0,
        "reference_atr": pytest.approx(2.0),
        "ratio": pytest.approx(1.5),
        "change": pytest.approx(0.5),
        "state": "expanding",
    }


def test_volatility_analyzer_detects_contracting_volatility():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[3.0, 3.0, 3.0, 2.0],
        lookback=3,
    )

    assert result == {
        "current_atr": 2.0,
        "reference_atr": pytest.approx(3.0),
        "ratio": pytest.approx(2.0 / 3.0),
        "change": pytest.approx(-1.0 / 3.0),
        "state": "contracting",
    }


def test_volatility_analyzer_detects_stable_volatility():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[2.0, 2.0, 2.0, 2.0],
        lookback=3,
    )

    assert result == {
        "current_atr": 2.0,
        "reference_atr": pytest.approx(2.0),
        "ratio": pytest.approx(1.0),
        "change": pytest.approx(0.0),
        "state": "stable",
    }


def test_volatility_analyzer_uses_only_requested_lookback():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[
            100.0,
            10.0,
            20.0,
            30.0,
            40.0,
        ],
        lookback=2,
    )

    assert result == {
        "current_atr": 40.0,
        "reference_atr": pytest.approx(25.0),
        "ratio": pytest.approx(1.6),
        "change": pytest.approx(0.6),
        "state": "expanding",
    }


def test_volatility_analyzer_supports_lookback_of_one():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[2.0, 3.0],
        lookback=1,
    )

    assert result == {
        "current_atr": 3.0,
        "reference_atr": pytest.approx(2.0),
        "ratio": pytest.approx(1.5),
        "change": pytest.approx(0.5),
        "state": "expanding",
    }


def test_volatility_analyzer_does_not_modify_atr_values():
    analyzer = VolatilityAnalyzer()

    atr_values = [
        2.0,
        2.5,
        3.0,
        4.0,
    ]
    expected_atr_values = [
        2.0,
        2.5,
        3.0,
        4.0,
    ]

    analyzer.analyze(
        atr_values=atr_values,
        lookback=3,
    )

    assert atr_values == expected_atr_values


def test_volatility_analyzer_rejects_zero_lookback():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match="lookback must be greater than zero",
    ):
        analyzer.analyze(
            atr_values=[2.0, 3.0],
            lookback=0,
        )


def test_volatility_analyzer_rejects_negative_lookback():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match="lookback must be greater than zero",
    ):
        analyzer.analyze(
            atr_values=[2.0, 3.0],
            lookback=-1,
        )


def test_volatility_analyzer_rejects_non_integer_lookback():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        TypeError,
        match="lookback must be an integer",
    ):
        analyzer.analyze(
            atr_values=[2.0, 3.0],
            lookback=1.5,
        )


def test_volatility_analyzer_rejects_insufficient_atr_values():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match=(
            "atr_values must contain the current ATR "
            "and at least lookback previous values"
        ),
    ):
        analyzer.analyze(
            atr_values=[2.0, 3.0],
            lookback=2,
        )


def test_volatility_analyzer_rejects_empty_atr_values():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match=(
            "atr_values must contain the current ATR "
            "and at least lookback previous values"
        ),
    ):
        analyzer.analyze(
            atr_values=[],
            lookback=1,
        )


def test_volatility_analyzer_rejects_negative_atr():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match="ATR values cannot be negative",
    ):
        analyzer.analyze(
            atr_values=[2.0, -1.0, 3.0],
            lookback=2,
        )


def test_volatility_analyzer_accepts_zero_current_atr():
    analyzer = VolatilityAnalyzer()

    result = analyzer.analyze(
        atr_values=[2.0, 2.0, 0.0],
        lookback=2,
    )

    assert result == {
        "current_atr": 0.0,
        "reference_atr": pytest.approx(2.0),
        "ratio": pytest.approx(0.0),
        "change": pytest.approx(-1.0),
        "state": "contracting",
    }


def test_volatility_analyzer_rejects_zero_reference_atr():
    analyzer = VolatilityAnalyzer()

    with pytest.raises(
        ValueError,
        match="reference ATR must be greater than zero",
    ):
        analyzer.analyze(
            atr_values=[0.0, 0.0, 1.0],
            lookback=2,
        )
