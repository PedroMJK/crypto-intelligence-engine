import pytest

from backend.app.analysis.structural_trend_detector import (
    StructuralTrendDetector,
)


def test_structural_trend_detector_detects_bullish_structure():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "HL",
            },
        ]
    )

    assert result == "bullish"


def test_structural_trend_detector_detects_bearish_structure():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "LL",
            },
        ]
    )

    assert result == "bearish"


def test_structural_trend_detector_returns_indeterminate_for_hh_and_ll():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "LL",
            },
        ]
    )

    assert result == "indeterminate"


def test_structural_trend_detector_returns_indeterminate_for_lh_and_hl():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "HL",
            },
        ]
    )

    assert result == "indeterminate"


def test_structural_trend_detector_returns_indeterminate_without_both_sides():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            }
        ]
    )

    assert result == "indeterminate"


def test_structural_trend_detector_returns_indeterminate_for_empty_list():
    detector = StructuralTrendDetector()

    assert detector.detect([]) == "indeterminate"


def test_structural_trend_detector_uses_latest_classifications():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "HL",
            },
            {
                "index": 3,
                "price": 9.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 4,
                "price": 6.0,
                "type": "low",
                "classification": "LL",
            },
        ]
    )

    assert result == "bearish"


def test_structural_trend_detector_ignores_unclassified_points():
    detector = StructuralTrendDetector()

    result = detector.detect(
        [
            {
                "index": 1,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 2,
                "price": 7.0,
                "type": "low",
                "classification": "HL",
            },
            {
                "index": 3,
                "price": 10.0,
                "type": "high",
                "classification": None,
            },
        ]
    )

    assert result == "bullish"


def test_structural_trend_detector_rejects_invalid_point_type():
    detector = StructuralTrendDetector()

    with pytest.raises(
        ValueError,
        match="point type must be high or low",
    ):
        detector.detect(
            [
                {
                    "index": 1,
                    "price": 10.0,
                    "type": "invalid",
                    "classification": None,
                }
            ]
        )


def test_structural_trend_detector_rejects_invalid_high_classification():
    detector = StructuralTrendDetector()

    with pytest.raises(
        ValueError,
        match="invalid classification for high point",
    ):
        detector.detect(
            [
                {
                    "index": 1,
                    "price": 10.0,
                    "type": "high",
                    "classification": "HL",
                }
            ]
        )


def test_structural_trend_detector_rejects_invalid_low_classification():
    detector = StructuralTrendDetector()

    with pytest.raises(
        ValueError,
        match="invalid classification for low point",
    ):
        detector.detect(
            [
                {
                    "index": 1,
                    "price": 7.0,
                    "type": "low",
                    "classification": "HH",
                }
            ]
        )


def test_structural_trend_detector_rejects_non_chronological_points():
    detector = StructuralTrendDetector()

    with pytest.raises(
        ValueError,
        match="points must be in chronological order",
    ):
        detector.detect(
            [
                {
                    "index": 3,
                    "price": 10.0,
                    "type": "high",
                    "classification": "HH",
                },
                {
                    "index": 1,
                    "price": 7.0,
                    "type": "low",
                    "classification": "HL",
                },
            ]
        )
