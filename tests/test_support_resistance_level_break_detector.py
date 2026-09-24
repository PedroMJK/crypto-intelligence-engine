import pytest

from backend.app.analysis.support_resistance_level_break_detector import (
    SupportResistanceLevelBreakDetector,
)


def test_level_break_detector_detects_resistance_break():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            103.0,
            104.0,
            104.5,
            104.8,
            104.9,
            104.0,
            105.0,
            105.5,
            106.0,
        ],
    )

    assert result == [
        {
            "index": 10,
            "type": "resistance",
            "price": 105.0,
            "close": 105.5,
            "zone_confirmation_index": 7,
        }
    ]


def test_level_break_detector_detects_support_break():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 95.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        closes=[
            100.0,
            99.0,
            98.0,
            97.0,
            96.0,
            95.5,
            95.2,
            95.1,
            96.0,
            95.0,
            94.5,
            94.0,
        ],
    )

    assert result == [
        {
            "index": 10,
            "type": "support",
            "price": 95.0,
            "close": 94.5,
            "zone_confirmation_index": 7,
        }
    ]


def test_level_break_detector_does_not_count_equality_as_break():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 3,
            }
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            103.0,
            104.0,
            105.0,
            104.5,
        ],
    )

    assert result == []


def test_level_break_detector_returns_only_first_break_per_zone():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 3,
            }
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            103.0,
            104.0,
            105.5,
            106.0,
            107.0,
        ],
    )

    assert result == [
        {
            "index": 5,
            "type": "resistance",
            "price": 105.0,
            "close": 105.5,
            "zone_confirmation_index": 3,
        }
    ]


def test_level_break_detector_ignores_break_before_confirmation():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 2,
                "level_indices": [1, 4],
                "confirmation_index": 5,
            }
        ],
        closes=[
            100.0,
            106.0,
            104.0,
            107.0,
            104.0,
            104.5,
            105.5,
        ],
    )

    assert result == [
        {
            "index": 6,
            "type": "resistance",
            "price": 105.0,
            "close": 105.5,
            "zone_confirmation_index": 5,
        }
    ]


def test_level_break_detector_handles_multiple_zones():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 4,
            },
            {
                "type": "support",
                "price": 95.0,
                "level_count": 1,
                "level_indices": [3],
                "confirmation_index": 5,
            },
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            100.0,
            101.0,
            100.0,
            106.0,
            97.0,
            94.0,
        ],
    )

    assert result == [
        {
            "index": 6,
            "type": "resistance",
            "price": 105.0,
            "close": 106.0,
            "zone_confirmation_index": 4,
        },
        {
            "index": 8,
            "type": "support",
            "price": 95.0,
            "close": 94.0,
            "zone_confirmation_index": 5,
        },
    ]


def test_level_break_detector_returns_events_in_chronological_order():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 95.0,
                "level_count": 1,
                "level_indices": [3],
                "confirmation_index": 5,
            },
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 4,
            },
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            100.0,
            101.0,
            100.0,
            106.0,
            97.0,
            94.0,
        ],
    )

    assert [event["index"] for event in result] == [
        6,
        8,
    ]


def test_level_break_detector_rejects_invalid_zone_type():
    detector = SupportResistanceLevelBreakDetector()

    with pytest.raises(
        ValueError,
        match="zone type must be support or resistance",
    ):
        detector.detect(
            zones=[
                {
                    "type": "invalid",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            closes=[100.0, 101.0, 102.0],
        )


def test_level_break_detector_rejects_non_positive_zone_price():
    detector = SupportResistanceLevelBreakDetector()

    with pytest.raises(
        ValueError,
        match="zone price must be greater than zero",
    ):
        detector.detect(
            zones=[
                {
                    "type": "support",
                    "price": 0.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            closes=[100.0, 101.0, 102.0],
        )


def test_level_break_detector_rejects_negative_confirmation_index():
    detector = SupportResistanceLevelBreakDetector()

    with pytest.raises(
        ValueError,
        match="confirmation index cannot be negative",
    ):
        detector.detect(
            zones=[
                {
                    "type": "support",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": -1,
                }
            ],
            closes=[100.0, 101.0, 102.0],
        )


def test_level_break_detector_rejects_confirmation_outside_closes():
    detector = SupportResistanceLevelBreakDetector()

    with pytest.raises(
        ValueError,
        match=(
            "confirmation index must reference "
            "an existing close"
        ),
    ):
        detector.detect(
            zones=[
                {
                    "type": "resistance",
                    "price": 105.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 3,
                }
            ],
            closes=[100.0, 101.0, 102.0],
        )


def test_level_break_detector_returns_empty_list_for_empty_inputs():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[],
        closes=[],
    )

    assert result == []


def test_level_break_detector_returns_empty_when_zone_is_not_broken():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 3,
            }
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            103.0,
            104.0,
            104.5,
            104.8,
        ],
    )

    assert result == []


def test_level_break_detector_preserves_same_index_events():
    detector = SupportResistanceLevelBreakDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 3,
            },
            {
                "type": "resistance",
                "price": 106.0,
                "level_count": 1,
                "level_indices": [3],
                "confirmation_index": 4,
            },
        ],
        closes=[
            100.0,
            101.0,
            102.0,
            103.0,
            104.0,
            107.0,
        ],
    )

    assert result == [
        {
            "index": 5,
            "type": "resistance",
            "price": 105.0,
            "close": 107.0,
            "zone_confirmation_index": 3,
        },
        {
            "index": 5,
            "type": "resistance",
            "price": 106.0,
            "close": 107.0,
            "zone_confirmation_index": 4,
        },
    ]


def test_level_break_detector_does_not_modify_inputs():
    detector = SupportResistanceLevelBreakDetector()

    zones = [
        {
            "type": "support",
            "price": 95.0,
            "level_count": 2,
            "level_indices": [1, 3],
            "confirmation_index": 4,
        }
    ]
    closes = [
        100.0,
        99.0,
        98.0,
        97.0,
        96.0,
        94.0,
    ]

    expected_zones = [
        {
            "type": "support",
            "price": 95.0,
            "level_count": 2,
            "level_indices": [1, 3],
            "confirmation_index": 4,
        }
    ]
    expected_closes = [
        100.0,
        99.0,
        98.0,
        97.0,
        96.0,
        94.0,
    ]

    detector.detect(
        zones=zones,
        closes=closes,
    )

    assert zones == expected_zones
    assert closes == expected_closes
