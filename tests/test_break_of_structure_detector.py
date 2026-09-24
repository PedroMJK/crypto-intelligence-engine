import pytest

from backend.app.analysis.break_of_structure_detector import (
    BreakOfStructureDetector,
)


def test_break_of_structure_detector_detects_bullish_break():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[9.0, 10.0, 12.0, 11.0, 11.5, 12.5],
    )

    assert result == [
        {
            "index": 5,
            "direction": "bullish",
            "level": 12.0,
            "structural_point_index": 2,
            "structural_point_confirmation_index": 4,
        }
    ]


def test_break_of_structure_detector_detects_bearish_break():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
                "classification": "LL",
            }
        ],
        closes=[10.0, 9.0, 8.0, 9.0, 8.5, 7.5],
    )

    assert result == [
        {
            "index": 5,
            "direction": "bearish",
            "level": 8.0,
            "structural_point_index": 2,
            "structural_point_confirmation_index": 4,
        }
    ]


def test_break_of_structure_detector_does_not_break_on_equal_close():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 12.0, 11.0, 12.0],
    )

    assert result == []


def test_break_of_structure_detector_ignores_break_before_confirmation():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 11.0, 12.0, 13.0, 11.0, 11.5],
    )

    assert result == []


def test_break_of_structure_detector_starts_after_confirmation():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 11.0, 12.0, 11.0, 13.0, 11.5],
    )

    assert result == []


def test_break_of_structure_detector_returns_empty_without_break():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 12.0, 11.0, 11.5, 11.8],
    )

    assert result == []


def test_break_of_structure_detector_emits_each_level_once():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 12.0, 11.0, 12.5, 13.0, 14.0],
    )

    assert len(result) == 1
    assert result[0]["index"] == 3


def test_break_of_structure_detector_detects_multiple_levels():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 10.0,
                "type": "high",
                "classification": "HH",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            },
        ],
        closes=[9.0, 10.0, 9.5, 11.0, 11.5, 12.5],
    )

    assert result == [
        {
            "index": 3,
            "direction": "bullish",
            "level": 10.0,
            "structural_point_index": 1,
            "structural_point_confirmation_index": 2,
        },
        {
            "index": 5,
            "direction": "bullish",
            "level": 12.0,
            "structural_point_index": 3,
            "structural_point_confirmation_index": 4,
        },
    ]


def test_break_of_structure_detector_returns_events_chronologically():
    detector = BreakOfStructureDetector()

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
        closes=[10.0, 12.0, 11.0, 12.5, 9.0, 7.5],
    )

    assert [
        event["index"]
        for event in result
    ] == [3, 5]


def test_break_of_structure_detector_ignores_point_without_confirmation():
    detector = BreakOfStructureDetector()

    result = detector.detect(
        structural_points=[
            {
                "index": 1,
                "price": 12.0,
                "type": "high",
                "classification": "HH",
            }
        ],
        closes=[10.0, 12.0, 13.0],
    )

    assert result == []


def test_break_of_structure_detector_returns_empty_for_empty_points():
    detector = BreakOfStructureDetector()

    assert detector.detect([], [10.0, 11.0, 12.0]) == []


def test_break_of_structure_detector_rejects_invalid_point_type():
    detector = BreakOfStructureDetector()

    with pytest.raises(
        ValueError,
        match="point type must be high or low",
    ):
        detector.detect(
            structural_points=[
                {
                    "index": 1,
                    "confirmation_index": 2,
                    "price": 12.0,
                    "type": "invalid",
                    "classification": None,
                }
            ],
            closes=[10.0, 11.0, 12.0],
        )


def test_break_of_structure_detector_rejects_non_chronological_points():
    detector = BreakOfStructureDetector()

    with pytest.raises(
        ValueError,
        match="points must be in chronological order",
    ):
        detector.detect(
            structural_points=[
                {
                    "index": 3,
                    "confirmation_index": 4,
                    "price": 12.0,
                    "type": "high",
                    "classification": "HH",
                },
                {
                    "index": 1,
                    "confirmation_index": 2,
                    "price": 8.0,
                    "type": "low",
                    "classification": "LL",
                },
            ],
            closes=[10.0, 11.0, 12.0, 11.0, 10.0],
        )


def test_break_of_structure_detector_rejects_confirmation_before_point():
    detector = BreakOfStructureDetector()

    with pytest.raises(
        ValueError,
        match="confirmation index cannot be lower than point index",
    ):
        detector.detect(
            structural_points=[
                {
                    "index": 3,
                    "confirmation_index": 2,
                    "price": 12.0,
                    "type": "high",
                    "classification": "HH",
                }
            ],
            closes=[10.0, 11.0, 12.0, 11.0],
        )


def test_break_of_structure_detector_rejects_confirmation_outside_closes():
    detector = BreakOfStructureDetector()

    with pytest.raises(
        ValueError,
        match="confirmation index must reference an existing close",
    ):
        detector.detect(
            structural_points=[
                {
                    "index": 1,
                    "confirmation_index": 4,
                    "price": 12.0,
                    "type": "high",
                    "classification": "HH",
                }
            ],
            closes=[10.0, 11.0, 12.0],
        )
