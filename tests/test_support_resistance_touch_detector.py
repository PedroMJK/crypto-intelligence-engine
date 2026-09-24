import pytest

from backend.app.analysis.support_resistance_touch_detector import (
    SupportResistanceTouchDetector,
)


def test_support_resistance_touch_detector_detects_resistance_touch():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        highs=[
            95.0,
            96.0,
            97.0,
            98.0,
            99.0,
            99.5,
            99.8,
            100.0,
            100.5,
        ],
        lows=[
            94.0,
            95.0,
            96.0,
            97.0,
            98.0,
            98.5,
            98.8,
            99.0,
            99.5,
        ],
    )

    assert result == [
        {
            "index": 8,
            "type": "resistance",
            "price": 100.0,
            "zone_confirmation_index": 7,
        }
    ]


def test_support_resistance_touch_detector_detects_support_touch():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        highs=[
            105.0,
            104.0,
            103.0,
            102.0,
            101.5,
            101.0,
            100.8,
            101.0,
            100.5,
        ],
        lows=[
            104.0,
            103.0,
            102.0,
            101.0,
            100.5,
            100.2,
            100.1,
            100.0,
            99.5,
        ],
    )

    assert result == [
        {
            "index": 8,
            "type": "support",
            "price": 100.0,
            "zone_confirmation_index": 7,
        }
    ]


def test_support_resistance_touch_detector_detects_multiple_touches():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [1, 3],
                "confirmation_index": 4,
            }
        ],
        highs=[
            95.0,
            96.0,
            97.0,
            98.0,
            100.0,
            100.5,
            99.5,
            101.0,
        ],
        lows=[
            94.0,
            95.0,
            96.0,
            97.0,
            99.0,
            99.5,
            98.5,
            99.8,
        ],
    )

    assert result == [
        {
            "index": 5,
            "type": "resistance",
            "price": 100.0,
            "zone_confirmation_index": 4,
        },
        {
            "index": 7,
            "type": "resistance",
            "price": 100.0,
            "zone_confirmation_index": 4,
        },
    ]


def test_support_resistance_touch_detector_ignores_candle_above_zone():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 100.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            }
        ],
        highs=[98.0, 99.0, 100.0, 110.0],
        lows=[97.0, 98.0, 99.0, 105.0],
    )

    assert result == []


def test_support_resistance_touch_detector_ignores_candle_below_zone():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            }
        ],
        highs=[102.0, 101.0, 100.0, 95.0],
        lows=[101.0, 100.0, 99.0, 90.0],
    )

    assert result == []


def test_support_resistance_touch_detector_includes_high_boundary():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "resistance",
                "price": 100.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            }
        ],
        highs=[98.0, 99.0, 99.5, 100.0],
        lows=[97.0, 98.0, 98.5, 99.0],
    )

    assert result == [
        {
            "index": 3,
            "type": "resistance",
            "price": 100.0,
            "zone_confirmation_index": 2,
        }
    ]


def test_support_resistance_touch_detector_includes_low_boundary():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            }
        ],
        highs=[103.0, 102.0, 101.0, 101.0],
        lows=[102.0, 101.0, 100.5, 100.0],
    )

    assert result == [
        {
            "index": 3,
            "type": "support",
            "price": 100.0,
            "zone_confirmation_index": 2,
        }
    ]


def test_support_resistance_touch_detector_ignores_confirmation_candle():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 3,
            }
        ],
        highs=[104.0, 103.0, 102.0, 101.0],
        lows=[103.0, 102.0, 101.0, 100.0],
    )

    assert result == []


def test_support_resistance_touch_detector_detects_multiple_zones():
    detector = SupportResistanceTouchDetector()

    result = detector.detect(
        zones=[
            {
                "type": "support",
                "price": 95.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            },
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 3,
            },
        ],
        highs=[
            100.0,
            101.0,
            102.0,
            96.0,
            106.0,
        ],
        lows=[
            99.0,
            100.0,
            101.0,
            94.0,
            104.0,
        ],
    )

    assert result == [
        {
            "index": 3,
            "type": "support",
            "price": 95.0,
            "zone_confirmation_index": 2,
        },
        {
            "index": 4,
            "type": "resistance",
            "price": 105.0,
            "zone_confirmation_index": 3,
        },
    ]


def test_support_resistance_touch_detector_returns_events_in_chronological_order():
    detector = SupportResistanceTouchDetector()

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
                "type": "support",
                "price": 95.0,
                "level_count": 1,
                "level_indices": [1],
                "confirmation_index": 2,
            },
        ],
        highs=[
            100.0,
            101.0,
            102.0,
            96.0,
            106.0,
        ],
        lows=[
            99.0,
            100.0,
            101.0,
            94.0,
            104.0,
        ],
    )

    assert result == [
        {
            "index": 3,
            "type": "support",
            "price": 95.0,
            "zone_confirmation_index": 2,
        },
        {
            "index": 4,
            "type": "resistance",
            "price": 105.0,
            "zone_confirmation_index": 3,
        },
    ]


def test_support_resistance_touch_detector_rejects_different_series_lengths():
    detector = SupportResistanceTouchDetector()

    with pytest.raises(
        ValueError,
        match="highs and lows must have the same length",
    ):
        detector.detect(
            zones=[],
            highs=[100.0, 101.0],
            lows=[99.0],
        )


def test_support_resistance_touch_detector_rejects_high_below_low():
    detector = SupportResistanceTouchDetector()

    with pytest.raises(
        ValueError,
        match="high cannot be lower than low",
    ):
        detector.detect(
            zones=[],
            highs=[100.0, 98.0],
            lows=[99.0, 99.0],
        )


def test_support_resistance_touch_detector_rejects_invalid_zone_type():
    detector = SupportResistanceTouchDetector()

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
                    "confirmation_index": 1,
                }
            ],
            highs=[100.0, 101.0],
            lows=[99.0, 100.0],
        )


def test_support_resistance_touch_detector_rejects_non_positive_zone_price():
    detector = SupportResistanceTouchDetector()

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
                    "confirmation_index": 1,
                }
            ],
            highs=[100.0, 101.0],
            lows=[99.0, 100.0],
        )


def test_support_resistance_touch_detector_rejects_negative_confirmation_index():
    detector = SupportResistanceTouchDetector()

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
            highs=[100.0, 101.0],
            lows=[99.0, 100.0],
        )


def test_support_resistance_touch_detector_rejects_confirmation_index_out_of_range():
    detector = SupportResistanceTouchDetector()

    with pytest.raises(
        ValueError,
        match="confirmation index must reference an existing candle",
    ):
        detector.detect(
            zones=[
                {
                    "type": "resistance",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            highs=[100.0, 101.0],
            lows=[99.0, 100.0],
        )


def test_support_resistance_touch_detector_does_not_modify_inputs():
    detector = SupportResistanceTouchDetector()

    zones = [
        {
            "type": "support",
            "price": 100.0,
            "level_count": 1,
            "level_indices": [1],
            "confirmation_index": 1,
        }
    ]
    highs = [102.0, 101.0, 100.5]
    lows = [101.0, 100.0, 99.5]

    expected_zones = [
        {
            "type": "support",
            "price": 100.0,
            "level_count": 1,
            "level_indices": [1],
            "confirmation_index": 1,
        }
    ]
    expected_highs = [102.0, 101.0, 100.5]
    expected_lows = [101.0, 100.0, 99.5]

    detector.detect(
        zones=zones,
        highs=highs,
        lows=lows,
    )

    assert zones == expected_zones
    assert highs == expected_highs
    assert lows == expected_lows
