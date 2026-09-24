import pytest

from backend.app.analysis.market_regime_analyzer import (
    MarketRegimeAnalyzer,
)


def test_market_regime_analyzer_detects_bullish_expanding_regime():
    analyzer = MarketRegimeAnalyzer()

    result = analyzer.analyze(
        trend_state="bullish",
        volatility_state="expanding",
    )

    assert result == {
        "trend": "bullish",
        "volatility": "expanding",
    }


def test_market_regime_analyzer_detects_bearish_contracting_regime():
    analyzer = MarketRegimeAnalyzer()

    result = analyzer.analyze(
        trend_state="bearish",
        volatility_state="contracting",
    )

    assert result == {
        "trend": "bearish",
        "volatility": "contracting",
    }


def test_market_regime_analyzer_supports_indeterminate_stable_regime():
    analyzer = MarketRegimeAnalyzer()

    result = analyzer.analyze(
        trend_state="indeterminate",
        volatility_state="stable",
    )

    assert result == {
        "trend": "indeterminate",
        "volatility": "stable",
    }


def test_market_regime_analyzer_preserves_input_states():
    analyzer = MarketRegimeAnalyzer()

    trend_state = "bullish"
    volatility_state = "expanding"

    result = analyzer.analyze(
        trend_state=trend_state,
        volatility_state=volatility_state,
    )

    assert trend_state == "bullish"
    assert volatility_state == "expanding"

    assert result == {
        "trend": "bullish",
        "volatility": "expanding",
    }


@pytest.mark.parametrize(
    "trend_state",
    [
        "neutral",
        "sideways",
        "strong_bullish",
        "strong_bearish",
    ],
)
def test_market_regime_analyzer_rejects_invalid_trend_state(
    trend_state,
):
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        ValueError,
        match="invalid trend state",
    ):
        analyzer.analyze(
            trend_state=trend_state,
            volatility_state="stable",
        )


@pytest.mark.parametrize(
    "volatility_state",
    [
        "high",
        "low",
        "volatile",
        "normal",
    ],
)
def test_market_regime_analyzer_rejects_invalid_volatility_state(
    volatility_state,
):
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        ValueError,
        match="invalid volatility state",
    ):
        analyzer.analyze(
            trend_state="bullish",
            volatility_state=volatility_state,
        )


def test_market_regime_analyzer_rejects_empty_trend_state():
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        ValueError,
        match="trend state must not be empty",
    ):
        analyzer.analyze(
            trend_state="",
            volatility_state="stable",
        )


def test_market_regime_analyzer_rejects_empty_volatility_state():
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        ValueError,
        match="volatility state must not be empty",
    ):
        analyzer.analyze(
            trend_state="bullish",
            volatility_state="",
        )


def test_market_regime_analyzer_rejects_non_string_trend_state():
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        TypeError,
        match="trend state must be a string",
    ):
        analyzer.analyze(
            trend_state=1,
            volatility_state="stable",
        )


def test_market_regime_analyzer_rejects_non_string_volatility_state():
    analyzer = MarketRegimeAnalyzer()

    with pytest.raises(
        TypeError,
        match="volatility state must be a string",
    ):
        analyzer.analyze(
            trend_state="bullish",
            volatility_state=1,
        )
