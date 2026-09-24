import pytest

from backend.app.analysis.multi_timeframe_analyzer import (
    MultiTimeframeAnalyzer,
)


def test_multi_timeframe_analyzer_returns_latest_confirmed_state_per_timeframe():
    analyzer = MultiTimeframeAnalyzer()

    result = analyzer.analyze(
        states=[
            {
                "timeframe": "1m",
                "state": "bearish",
                "confirmation_timestamp": 1000,
            },
            {
                "timeframe": "1m",
                "state": "bullish",
                "confirmation_timestamp": 2000,
            },
            {
                "timeframe": "5m",
                "state": "bullish",
                "confirmation_timestamp": 1500,
            },
        ],
        reference_timestamp=2500,
    )

    assert result == [
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 2000,
        },
        {
            "timeframe": "5m",
            "state": "bullish",
            "confirmation_timestamp": 1500,
        },
    ]


def test_multi_timeframe_analyzer_ignores_future_states():
    analyzer = MultiTimeframeAnalyzer()

    result = analyzer.analyze(
        states=[
            {
                "timeframe": "1m",
                "state": "bullish",
                "confirmation_timestamp": 1000,
            },
            {
                "timeframe": "5m",
                "state": "bearish",
                "confirmation_timestamp": 3000,
            },
        ],
        reference_timestamp=2000,
    )

    assert result == [
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 1000,
        },
    ]


def test_multi_timeframe_analyzer_accepts_state_confirmed_at_reference_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    result = analyzer.analyze(
        states=[
            {
                "timeframe": "5m",
                "state": "bullish",
                "confirmation_timestamp": 2000,
            },
        ],
        reference_timestamp=2000,
    )

    assert result == [
        {
            "timeframe": "5m",
            "state": "bullish",
            "confirmation_timestamp": 2000,
        },
    ]


def test_multi_timeframe_analyzer_preserves_distinct_timeframes():
    analyzer = MultiTimeframeAnalyzer()

    result = analyzer.analyze(
        states=[
            {
                "timeframe": "1m",
                "state": "bullish",
                "confirmation_timestamp": 1000,
            },
            {
                "timeframe": "5m",
                "state": "bearish",
                "confirmation_timestamp": 1000,
            },
            {
                "timeframe": "15m",
                "state": "bullish",
                "confirmation_timestamp": 1000,
            },
        ],
        reference_timestamp=2000,
    )

    assert result == [
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 1000,
        },
        {
            "timeframe": "5m",
            "state": "bearish",
            "confirmation_timestamp": 1000,
        },
        {
            "timeframe": "15m",
            "state": "bullish",
            "confirmation_timestamp": 1000,
        },
    ]


def test_multi_timeframe_analyzer_is_independent_of_input_order():
    analyzer = MultiTimeframeAnalyzer()

    states = [
        {
            "timeframe": "5m",
            "state": "bullish",
            "confirmation_timestamp": 2000,
        },
        {
            "timeframe": "1m",
            "state": "bearish",
            "confirmation_timestamp": 1000,
        },
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 1500,
        },
    ]

    result = analyzer.analyze(
        states=states,
        reference_timestamp=2500,
    )

    assert result == [
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 1500,
        },
        {
            "timeframe": "5m",
            "state": "bullish",
            "confirmation_timestamp": 2000,
        },
    ]


def test_multi_timeframe_analyzer_returns_empty_result_for_empty_states():
    analyzer = MultiTimeframeAnalyzer()

    result = analyzer.analyze(
        states=[],
        reference_timestamp=2000,
    )

    assert result == []


def test_multi_timeframe_analyzer_rejects_empty_timeframe():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="timeframe must not be empty",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "",
                    "state": "bullish",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_empty_state():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="state must not be empty",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_negative_confirmation_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="confirmation timestamp cannot be negative",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "bullish",
                    "confirmation_timestamp": -1,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_negative_reference_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="reference timestamp cannot be negative",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "bullish",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=-1,
        )


def test_multi_timeframe_analyzer_rejects_non_integer_confirmation_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        TypeError,
        match="confirmation timestamp must be an integer",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "bullish",
                    "confirmation_timestamp": 1000.5,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_non_integer_reference_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        TypeError,
        match="reference timestamp must be an integer",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "bullish",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000.5,
        )


def test_multi_timeframe_analyzer_rejects_non_integer_timeframe():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        TypeError,
        match="timeframe must be a string",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": 1,
                    "state": "bullish",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_non_integer_state():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        TypeError,
        match="state must be a string",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": 1,
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_non_dictionary_state():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        TypeError,
        match="each state must be a dictionary",
    ):
        analyzer.analyze(
            states=[
                "invalid",
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_missing_timeframe():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="state must contain timeframe",
    ):
        analyzer.analyze(
            states=[
                {
                    "state": "bullish",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_missing_state():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="state must contain state",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "confirmation_timestamp": 1000,
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_rejects_missing_confirmation_timestamp():
    analyzer = MultiTimeframeAnalyzer()

    with pytest.raises(
        ValueError,
        match="state must contain confirmation_timestamp",
    ):
        analyzer.analyze(
            states=[
                {
                    "timeframe": "1m",
                    "state": "bullish",
                },
            ],
            reference_timestamp=2000,
        )


def test_multi_timeframe_analyzer_does_not_modify_input():
    analyzer = MultiTimeframeAnalyzer()

    states = [
        {
            "timeframe": "1m",
            "state": "bearish",
            "confirmation_timestamp": 1000,
        },
        {
            "timeframe": "1m",
            "state": "bullish",
            "confirmation_timestamp": 2000,
        },
    ]

    original_states = [
        state.copy()
        for state in states
    ]

    analyzer.analyze(
        states=states,
        reference_timestamp=2500,
    )

    assert states == original_states
