import pytest

from backend.app.analysis.structure_change_detector import (
    StructureChangeDetector,
)


def test_structure_change_detector_detects_bullish_to_bearish_change():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "HL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            }
        ],
    )

    assert result == [
        {
            "index": 6,
            "previous_trend": "bullish",
            "new_direction": "bearish",
            "break_direction": "bearish",
            "level": 8.0,
            "structural_point_index": 3,
        }
    ]


def test_structure_change_detector_detects_bearish_to_bullish_change():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bullish",
                "level": 12.0,
                "structural_point_index": 1,
                "structural_point_confirmation_index": 2,
            }
        ],
    )

    assert result == [
        {
            "index": 6,
            "previous_trend": "bearish",
            "new_direction": "bullish",
            "break_direction": "bullish",
            "level": 12.0,
            "structural_point_index": 1,
        }
    ]


def test_structure_change_detector_ignores_bullish_continuation():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "HL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bullish",
                "level": 12.0,
                "structural_point_index": 1,
                "structural_point_confirmation_index": 2,
            }
        ],
    )

    assert result == []


def test_structure_change_detector_ignores_bearish_continuation():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            }
        ],
    )

    assert result == []


def test_structure_change_detector_ignores_indeterminate_structure():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            }
        ],
    )

    assert result == []


def test_structure_change_detector_uses_only_confirmed_points():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "HL",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 11.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 6,
                "confirmation_index": 8,
                "price": 7.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            }
        ],
    )

    assert result[0]["previous_trend"] == "bullish"
    assert result[0]["new_direction"] == "bearish"


def test_structure_change_detector_includes_point_confirmed_on_break_candle():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 3,
                "confirmation_index": 6,
                "price": 8.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bullish",
                "level": 12.0,
                "structural_point_index": 1,
                "structural_point_confirmation_index": 2,
            }
        ],
    )

    assert result[0]["previous_trend"] == "bearish"
    assert result[0]["new_direction"] == "bullish"


def test_structure_change_detector_ignores_points_without_confirmation():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "HL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            }
        ],
    )

    assert result == []


def test_structure_change_detector_detects_multiple_changes():
    detector = StructureChangeDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "HL",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 11.0,
                "type": "high",
                "classification": "LH",
            },
            {
                "index": 7,
                "confirmation_index": 8,
                "price": 7.0,
                "type": "low",
                "classification": "LL",
            },
        ],
        break_events=[
            {
                "index": 6,
                "direction": "bearish",
                "level": 8.0,
                "structural_point_index": 3,
                "structural_point_confirmation_index": 4,
            },
            {
                "index": 9,
                "direction": "bullish",
                "level": 11.0,
                "structural_point_index": 5,
                "structural_point_confirmation_index": 7,
            },
        ],
    )

    assert result == [
        {
            "index": 6,
            "previous_trend": "bullish",
            "new_direction": "bearish",
            "break_direction": "bearish",
            "level": 8.0,
            "structural_point_index": 3,
        },
        {
            "index": 9,
            "previous_trend": "bearish",
            "new_direction": "bullish",
            "break_direction": "bullish",
            "level": 11.0,
            "structural_point_index": 5,
        },
    ]


def test_structure_change_detector_returns_empty_without_break_events():
    detector = StructureChangeDetector()

    assert detector.detect([], []) == []


def test_structure_change_detector_rejects_invalid_break_direction():
    detector = StructureChangeDetector()

    with pytest.raises(
        ValueError,
        match="break direction must be bullish or bearish",
    ):
        detector.detect(
            structural_points=[],
            break_events=[
                {
                    "index": 4,
                    "direction": "invalid",
                    "level": 10.0,
                    "structural_point_index": 1,
                    "structural_point_confirmation_index": 2,
                }
            ],
        )


def test_structure_change_detector_rejects_non_chronological_break_events():
    detector = StructureChangeDetector()

    with pytest.raises(
        ValueError,
        match="break events must be in chronological order",
    ):
        detector.detect(
            structural_points=[],
            break_events=[
                {
                    "index": 6,
                    "direction": "bearish",
                    "level": 8.0,
                    "structural_point_index": 3,
                    "structural_point_confirmation_index": 4,
                },
                {
                    "index": 5,
                    "direction": "bullish",
                    "level": 12.0,
                    "structural_point_index": 1,
                    "structural_point_confirmation_index": 2,
                },
            ],
        )
