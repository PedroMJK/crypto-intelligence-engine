import pytest

from backend.app.analysis.swing_point_detector import SwingPointDetector


def test_swing_point_detector_detects_swing_high():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[10.0, 12.0, 15.0, 13.0, 11.0],
        lows=[8.0, 9.0, 10.0, 9.0, 8.0],
        window=2,
    )

    assert result == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 15.0,
            "type": "high",
        }
    ]


def test_swing_point_detector_detects_swing_low():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[14.0, 13.0, 12.0, 13.0, 14.0],
        lows=[10.0, 8.0, 6.0, 9.0, 11.0],
        window=2,
    )

    assert result == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 6.0,
            "type": "low",
        }
    ]


def test_swing_point_detector_returns_points_in_chronological_order():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[10.0, 15.0, 11.0, 9.0, 12.0],
        lows=[8.0, 10.0, 7.0, 5.0, 9.0],
        window=1,
    )

    assert result == [
        {
            "index": 1,
            "confirmation_index": 2,
            "price": 15.0,
            "type": "high",
        },
        {
            "index": 3,
            "confirmation_index": 4,
            "price": 5.0,
            "type": "low",
        },
    ]


def test_swing_point_detector_rejects_equal_highs_as_swing():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[10.0, 15.0, 15.0, 13.0, 11.0],
        lows=[8.0, 9.0, 10.0, 9.0, 8.0],
        window=2,
    )

    assert result == []


def test_swing_point_detector_rejects_equal_lows_as_swing():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[14.0, 13.0, 12.0, 13.0, 14.0],
        lows=[10.0, 6.0, 6.0, 9.0, 11.0],
        window=2,
    )

    assert result == []


def test_swing_point_detector_does_not_evaluate_series_edges():
    detector = SwingPointDetector()

    result = detector.detect(
        highs=[20.0, 12.0, 11.0, 12.0, 20.0],
        lows=[1.0, 8.0, 9.0, 8.0, 1.0],
        window=1,
    )

    assert result == []


def test_swing_point_detector_rejects_zero_window():
    detector = SwingPointDetector()

    with pytest.raises(
        ValueError,
        match="window must be greater than zero",
    ):
        detector.detect(
            highs=[10.0, 12.0, 11.0],
            lows=[8.0, 9.0, 8.0],
            window=0,
        )


def test_swing_point_detector_rejects_negative_window():
    detector = SwingPointDetector()

    with pytest.raises(
        ValueError,
        match="window must be greater than zero",
    ):
        detector.detect(
            highs=[10.0, 12.0, 11.0],
            lows=[8.0, 9.0, 8.0],
            window=-1,
        )


def test_swing_point_detector_rejects_non_integer_window():
    detector = SwingPointDetector()

    with pytest.raises(
        TypeError,
        match="window must be an integer",
    ):
        detector.detect(
            highs=[10.0, 12.0, 11.0],
            lows=[8.0, 9.0, 8.0],
            window=1.5,
        )


def test_swing_point_detector_rejects_different_series_lengths():
    detector = SwingPointDetector()

    with pytest.raises(
        ValueError,
        match="highs and lows must have the same length",
    ):
        detector.detect(
            highs=[10.0, 12.0, 11.0],
            lows=[8.0, 9.0],
            window=1,
        )


def test_swing_point_detector_rejects_insufficient_values():
    detector = SwingPointDetector()

    with pytest.raises(
        ValueError,
        match=r"price series must contain at least 2 \* window \+ 1 elements",
    ):
        detector.detect(
            highs=[10.0, 12.0, 11.0, 13.0],
            lows=[8.0, 9.0, 8.0, 10.0],
            window=2,
        )


def test_swing_point_detector_rejects_high_below_low():
    detector = SwingPointDetector()

    with pytest.raises(
        ValueError,
        match="high cannot be lower than low",
    ):
        detector.detect(
            highs=[10.0, 8.0, 11.0],
            lows=[8.0, 9.0, 8.0],
            window=1,
        )
