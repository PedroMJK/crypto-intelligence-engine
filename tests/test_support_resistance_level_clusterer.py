import pytest

from backend.app.analysis.support_resistance_level_clusterer import (
    SupportResistanceLevelClusterer,
)


def test_support_resistance_level_clusterer_keeps_single_level():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "resistance",
            }
        ]
    )

    assert result == [
        {
            "type": "resistance",
            "price": 100.0,
            "level_count": 1,
            "level_indices": [2],
            "confirmation_index": 4,
        }
    ]


def test_support_resistance_level_clusterer_groups_nearby_levels():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "resistance",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 100.5,
                "type": "resistance",
            },
        ]
    )

    assert result == [
        {
            "type": "resistance",
            "price": 100.25,
            "level_count": 2,
            "level_indices": [2, 5],
            "confirmation_index": 7,
        }
    ]


def test_support_resistance_level_clusterer_separates_distant_levels():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "resistance",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 102.0,
                "type": "resistance",
            },
        ]
    )

    assert result == [
        {
            "type": "resistance",
            "price": 100.0,
            "level_count": 1,
            "level_indices": [2],
            "confirmation_index": 4,
        },
        {
            "type": "resistance",
            "price": 102.0,
            "level_count": 1,
            "level_indices": [5],
            "confirmation_index": 7,
        },
    ]


def test_support_resistance_level_clusterer_separates_level_types():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "resistance",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 100.5,
                "type": "support",
            },
        ]
    )

    assert result == [
        {
            "type": "resistance",
            "price": 100.0,
            "level_count": 1,
            "level_indices": [2],
            "confirmation_index": 4,
        },
        {
            "type": "support",
            "price": 100.5,
            "level_count": 1,
            "level_indices": [5],
            "confirmation_index": 7,
        },
    ]


def test_support_resistance_level_clusterer_uses_updated_cluster_price():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "resistance",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 100.8,
                "type": "resistance",
            },
            {
                "index": 8,
                "confirmation_index": 10,
                "price": 101.2,
                "type": "resistance",
            },
        ]
    )

    assert result == [
        {
            "type": "resistance",
            "price": 100.66666666666667,
            "level_count": 3,
            "level_indices": [2, 5, 8],
            "confirmation_index": 10,
        }
    ]


def test_support_resistance_level_clusterer_includes_tolerance_boundary():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "support",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 101.0,
                "type": "support",
            },
        ]
    )

    assert result == [
        {
            "type": "support",
            "price": 100.5,
            "level_count": 2,
            "level_indices": [2, 5],
            "confirmation_index": 7,
        }
    ]


def test_support_resistance_level_clusterer_rejects_negative_tolerance():
    with pytest.raises(
        ValueError,
        match="tolerance ratio cannot be negative",
    ):
        SupportResistanceLevelClusterer(
            tolerance_ratio=-0.01
        )


def test_support_resistance_level_clusterer_rejects_invalid_level_type():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    with pytest.raises(
        ValueError,
        match="level type must be support or resistance",
    ):
        clusterer.cluster(
            [
                {
                    "index": 2,
                    "confirmation_index": 4,
                    "price": 100.0,
                    "type": "invalid",
                }
            ]
        )


def test_support_resistance_level_clusterer_rejects_non_positive_price():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    with pytest.raises(
        ValueError,
        match="level price must be greater than zero",
    ):
        clusterer.cluster(
            [
                {
                    "index": 2,
                    "confirmation_index": 4,
                    "price": 0.0,
                    "type": "support",
                }
            ]
        )


def test_support_resistance_level_clusterer_rejects_non_chronological_levels():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    with pytest.raises(
        ValueError,
        match="levels must be in chronological order",
    ):
        clusterer.cluster(
            [
                {
                    "index": 5,
                    "confirmation_index": 7,
                    "price": 100.0,
                    "type": "resistance",
                },
                {
                    "index": 2,
                    "confirmation_index": 4,
                    "price": 100.5,
                    "type": "resistance",
                },
            ]
        )


def test_support_resistance_level_clusterer_rejects_confirmation_index_lower_than_index():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    with pytest.raises(
        ValueError,
        match="confirmation index cannot be lower than level index",
    ):
        clusterer.cluster(
            [
                {
                    "index": 5,
                    "confirmation_index": 4,
                    "price": 100.0,
                    "type": "support",
                }
            ]
        )


def test_support_resistance_level_clusterer_rejects_non_chronological_confirmations():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    with pytest.raises(
        ValueError,
        match="level confirmations must be in chronological order",
    ):
        clusterer.cluster(
            [
                {
                    "index": 2,
                    "confirmation_index": 10,
                    "price": 100.0,
                    "type": "resistance",
                },
                {
                    "index": 5,
                    "confirmation_index": 7,
                    "price": 100.5,
                    "type": "resistance",
                },
            ]
        )


def test_support_resistance_level_clusterer_does_not_modify_input():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.01
    )

    levels = [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 100.0,
            "type": "resistance",
        },
        {
            "index": 5,
            "confirmation_index": 7,
            "price": 100.5,
            "type": "resistance",
        },
    ]

    expected_levels = [
        {
            "index": 2,
            "confirmation_index": 4,
            "price": 100.0,
            "type": "resistance",
        },
        {
            "index": 5,
            "confirmation_index": 7,
            "price": 100.5,
            "type": "resistance",
        },
    ]

    clusterer.cluster(levels)

    assert levels == expected_levels


def test_support_resistance_level_clusterer_zero_tolerance_groups_only_equal_prices():
    clusterer = SupportResistanceLevelClusterer(
        tolerance_ratio=0.0
    )

    result = clusterer.cluster(
        [
            {
                "index": 2,
                "confirmation_index": 4,
                "price": 100.0,
                "type": "support",
            },
            {
                "index": 5,
                "confirmation_index": 7,
                "price": 100.0,
                "type": "support",
            },
            {
                "index": 8,
                "confirmation_index": 10,
                "price": 100.01,
                "type": "support",
            },
        ]
    )

    assert result == [
        {
            "type": "support",
            "price": 100.0,
            "level_count": 2,
            "level_indices": [2, 5],
            "confirmation_index": 7,
        },
        {
            "type": "support",
            "price": 100.01,
            "level_count": 1,
            "level_indices": [8],
            "confirmation_index": 10,
        },
    ]
