import pytest

from backend.app.analysis.support_resistance_level_strength_calculator import (
    SupportResistanceLevelStrengthCalculator,
)


def test_level_strength_calculator_returns_initial_zone_strength():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        touch_events=[],
    )

    assert result == [
        {
            "index": 7,
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "touch_count": 0,
            "strength": 2,
            "zone_confirmation_index": 7,
        }
    ]


def test_level_strength_calculator_increases_strength_after_touch():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        touch_events=[
            {
                "index": 10,
                "type": "support",
                "price": 100.0,
                "zone_confirmation_index": 7,
            }
        ],
    )

    assert result == [
        {
            "index": 7,
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "touch_count": 0,
            "strength": 2,
            "zone_confirmation_index": 7,
        },
        {
            "index": 10,
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "touch_count": 1,
            "strength": 3,
            "zone_confirmation_index": 7,
        },
    ]


def test_level_strength_calculator_accumulates_multiple_touches():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 3,
                "level_indices": [1, 4, 6],
                "confirmation_index": 8,
            }
        ],
        touch_events=[
            {
                "index": 10,
                "type": "resistance",
                "price": 105.0,
                "zone_confirmation_index": 8,
            },
            {
                "index": 14,
                "type": "resistance",
                "price": 105.0,
                "zone_confirmation_index": 8,
            },
        ],
    )

    assert result == [
        {
            "index": 8,
            "type": "resistance",
            "price": 105.0,
            "level_count": 3,
            "touch_count": 0,
            "strength": 3,
            "zone_confirmation_index": 8,
        },
        {
            "index": 10,
            "type": "resistance",
            "price": 105.0,
            "level_count": 3,
            "touch_count": 1,
            "strength": 4,
            "zone_confirmation_index": 8,
        },
        {
            "index": 14,
            "type": "resistance",
            "price": 105.0,
            "level_count": 3,
            "touch_count": 2,
            "strength": 5,
            "zone_confirmation_index": 8,
        },
    ]


def test_level_strength_calculator_handles_multiple_zones():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "support",
                "price": 95.0,
                "level_count": 2,
                "level_indices": [1, 3],
                "confirmation_index": 5,
            },
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [4],
                "confirmation_index": 6,
            },
        ],
        touch_events=[
            {
                "index": 8,
                "type": "resistance",
                "price": 105.0,
                "zone_confirmation_index": 6,
            },
            {
                "index": 7,
                "type": "support",
                "price": 95.0,
                "zone_confirmation_index": 5,
            },
        ],
    )

    assert result == [
        {
            "index": 5,
            "type": "support",
            "price": 95.0,
            "level_count": 2,
            "touch_count": 0,
            "strength": 2,
            "zone_confirmation_index": 5,
        },
        {
            "index": 6,
            "type": "resistance",
            "price": 105.0,
            "level_count": 1,
            "touch_count": 0,
            "strength": 1,
            "zone_confirmation_index": 6,
        },
        {
            "index": 7,
            "type": "support",
            "price": 95.0,
            "level_count": 2,
            "touch_count": 1,
            "strength": 3,
            "zone_confirmation_index": 5,
        },
        {
            "index": 8,
            "type": "resistance",
            "price": 105.0,
            "level_count": 1,
            "touch_count": 1,
            "strength": 2,
            "zone_confirmation_index": 6,
        },
    ]


def test_level_strength_calculator_returns_events_in_chronological_order():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [3],
                "confirmation_index": 6,
            },
            {
                "type": "support",
                "price": 95.0,
                "level_count": 2,
                "level_indices": [1, 2],
                "confirmation_index": 4,
            },
        ],
        touch_events=[
            {
                "index": 8,
                "type": "resistance",
                "price": 105.0,
                "zone_confirmation_index": 6,
            },
            {
                "index": 7,
                "type": "support",
                "price": 95.0,
                "zone_confirmation_index": 4,
            },
        ],
    )

    assert [event["index"] for event in result] == [
        4,
        6,
        7,
        8,
    ]


def test_level_strength_calculator_rejects_invalid_zone_type():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="zone type must be support or resistance",
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "invalid",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            touch_events=[],
        )


def test_level_strength_calculator_rejects_non_positive_zone_price():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="zone price must be greater than zero",
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "support",
                    "price": 0.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            touch_events=[],
        )


def test_level_strength_calculator_rejects_invalid_level_count():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="level count must be a positive integer",
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "support",
                    "price": 100.0,
                    "level_count": 0,
                    "level_indices": [1],
                    "confirmation_index": 2,
                }
            ],
            touch_events=[],
        )


def test_level_strength_calculator_rejects_negative_confirmation_index():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="confirmation index cannot be negative",
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "support",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": -1,
                }
            ],
            touch_events=[],
        )


def test_level_strength_calculator_rejects_invalid_touch_type():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="touch type must be support or resistance",
    ):
        calculator.calculate(
            zones=[],
            touch_events=[
                {
                    "index": 5,
                    "type": "invalid",
                    "price": 100.0,
                    "zone_confirmation_index": 2,
                }
            ],
        )


def test_level_strength_calculator_rejects_non_positive_touch_price():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="touch price must be greater than zero",
    ):
        calculator.calculate(
            zones=[],
            touch_events=[
                {
                    "index": 5,
                    "type": "support",
                    "price": 0.0,
                    "zone_confirmation_index": 2,
                }
            ],
        )


def test_level_strength_calculator_rejects_touch_at_confirmation():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match=(
            "touch index must be greater than "
            "zone confirmation index"
        ),
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "support",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 3,
                }
            ],
            touch_events=[
                {
                    "index": 3,
                    "type": "support",
                    "price": 100.0,
                    "zone_confirmation_index": 3,
                }
            ],
        )


def test_level_strength_calculator_rejects_orphan_touch():
    calculator = SupportResistanceLevelStrengthCalculator()

    with pytest.raises(
        ValueError,
        match="touch event must reference an existing zone",
    ):
        calculator.calculate(
            zones=[
                {
                    "type": "support",
                    "price": 100.0,
                    "level_count": 1,
                    "level_indices": [1],
                    "confirmation_index": 3,
                }
            ],
            touch_events=[
                {
                    "index": 5,
                    "type": "resistance",
                    "price": 105.0,
                    "zone_confirmation_index": 3,
                }
            ],
        )


def test_level_strength_calculator_does_not_modify_inputs():
    calculator = SupportResistanceLevelStrengthCalculator()

    zones = [
        {
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "level_indices": [1, 3],
            "confirmation_index": 5,
        }
    ]
    touch_events = [
        {
            "index": 7,
            "type": "support",
            "price": 100.0,
            "zone_confirmation_index": 5,
        }
    ]

    expected_zones = [
        {
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "level_indices": [1, 3],
            "confirmation_index": 5,
        }
    ]
    expected_touch_events = [
        {
            "index": 7,
            "type": "support",
            "price": 100.0,
            "zone_confirmation_index": 5,
        }
    ]

    calculator.calculate(
        zones=zones,
        touch_events=touch_events,
    )

    assert zones == expected_zones
    assert touch_events == expected_touch_events


def test_level_strength_calculator_handles_unsorted_touch_events():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "support",
                "price": 100.0,
                "level_count": 2,
                "level_indices": [2, 5],
                "confirmation_index": 7,
            }
        ],
        touch_events=[
            {
                "index": 15,
                "type": "support",
                "price": 100.0,
                "zone_confirmation_index": 7,
            },
            {
                "index": 10,
                "type": "support",
                "price": 100.0,
                "zone_confirmation_index": 7,
            },
        ],
    )

    assert [
        (event["index"], event["touch_count"], event["strength"])
        for event in result
    ] == [
        (7, 0, 2),
        (10, 1, 3),
        (15, 2, 4),
    ]


def test_level_strength_calculator_returns_empty_list_for_empty_inputs():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[],
        touch_events=[],
    )

    assert result == []


def test_level_strength_calculator_preserves_same_index_events():
    calculator = SupportResistanceLevelStrengthCalculator()

    result = calculator.calculate(
        zones=[
            {
                "type": "support",
                "price": 95.0,
                "level_count": 2,
                "level_indices": [1, 3],
                "confirmation_index": 5,
            },
            {
                "type": "resistance",
                "price": 105.0,
                "level_count": 1,
                "level_indices": [2],
                "confirmation_index": 6,
            },
        ],
        touch_events=[
            {
                "index": 8,
                "type": "support",
                "price": 95.0,
                "zone_confirmation_index": 5,
            },
            {
                "index": 8,
                "type": "resistance",
                "price": 105.0,
                "zone_confirmation_index": 6,
            },
        ],
    )

    events_at_index_8 = [
        event
        for event in result
        if event["index"] == 8
    ]

    assert events_at_index_8 == [
        {
            "index": 8,
            "type": "support",
            "price": 95.0,
            "level_count": 2,
            "touch_count": 1,
            "strength": 3,
            "zone_confirmation_index": 5,
        },
        {
            "index": 8,
            "type": "resistance",
            "price": 105.0,
            "level_count": 1,
            "touch_count": 1,
            "strength": 2,
            "zone_confirmation_index": 6,
        },
    ]
