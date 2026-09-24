import pytest

from backend.app.analysis.support_resistance_level_detector import (
    SupportResistanceLevelDetector,
)


def test_support_resistance_level_detector_detects_resistance():
    detector = SupportResistanceLevelDetector()

    result = detector.detect(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
            }
        ]
    )

    assert result == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 12.0,
            "type": "resistance",
        }
    ]


def test_support_resistance_level_detector_detects_support():
    detector = SupportResistanceLevelDetector()

    result = detector.detect(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 8.0,
                "type": "low",
            }
        ]
    )

    assert result == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 8.0,
            "type": "support",
        }
    ]


def test_support_resistance_level_detector_detects_multiple_levels():
    detector = SupportResistanceLevelDetector()

    result = detector.detect(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 8.0,
                "type": "low",
            },
        ]
    )

    assert result == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 12.0,
            "type": "resistance",
        },
        {
            "index": 5,
            "confirmation_index": 7,
            "price": 8.0,
            "type": "support",
        },
    ]


def test_support_resistance_level_detector_ignores_unconfirmed_point():
    detector = SupportResistanceLevelDetector()

    result = detector.detect(
        [
            {
                "index": 2,
                "price": 12.0,
                "type": "high",
            }
        ]
    )

    assert result == []


def test_support_resistance_level_detector_returns_empty_list():
    detector = SupportResistanceLevelDetector()

    assert detector.detect([]) == []


def test_support_resistance_level_detector_rejects_invalid_point_type():
    detector = SupportResistanceLevelDetector()

    with pytest.raises(
        ValueError,
        match="point type must be high or low",
    ):
        detector.detect(
            [
                {
                    "index": 2,
                    "confirmation_index": 4,
                    "price": 12.0,
                    "type": "invalid",
                }
            ]
        )


def test_support_resistance_level_detector_rejects_non_chronological_points():
    detector = SupportResistanceLevelDetector()

    with pytest.raises(
        ValueError,
        match="points must be in chronological order",
    ):
        detector.detect(
            [
                {
                    "index": 5,
                    "confirmation_index": 7,
                    "price": 12.0,
                    "type": "high",
                },
                {
                    "index": 2,
                    "confirmation_index": 4,
                    "price": 8.0,
                    "type": "low",
                },
            ]
        )


def test_support_resistance_level_detector_rejects_confirmation_before_point():
    detector = SupportResistanceLevelDetector()

    with pytest.raises(
        ValueError,
        match=(
            "confirmation index cannot be lower than point index"
        ),
    ):
        detector.detect(
            [
                {
                    "index": 4,
                    "confirmation_index": 3,
                    "price": 12.0,
                    "type": "high",
                }
            ]
        )


def test_support_resistance_level_detector_does_not_modify_input():
    detector = SupportResistanceLevelDetector()
    swing_points = [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 12.0,
            "type": "high",
        }
    ]

    detector.detect(swing_points)

    assert swing_points == [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 12.0,
            "type": "high",
        }
    ]
