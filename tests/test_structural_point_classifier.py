import pytest

from backend.app.analysis.structural_point_classifier import (
    StructuralPointClassifier,
)


def test_structural_point_classifier_classifies_higher_high():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 10.0, "type": "high"},
            {"index": 3, "price": 12.0, "type": "high"},
        ]
    )

    assert result == [
        {
            "index": 1,
            "price": 10.0,
            "type": "high",
            "classification": None,
        },
        {
            "index": 3,
            "price": 12.0,
            "type": "high",
            "classification": "HH",
        },
    ]


def test_structural_point_classifier_classifies_lower_high():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 12.0, "type": "high"},
            {"index": 3, "price": 10.0, "type": "high"},
        ]
    )

    assert result[1]["classification"] == "LH"


def test_structural_point_classifier_classifies_higher_low():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 6.0, "type": "low"},
            {"index": 3, "price": 8.0, "type": "low"},
        ]
    )

    assert result[1]["classification"] == "HL"


def test_structural_point_classifier_classifies_lower_low():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 8.0, "type": "low"},
            {"index": 3, "price": 6.0, "type": "low"},
        ]
    )

    assert result[1]["classification"] == "LL"


def test_structural_point_classifier_compares_points_of_same_type():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 10.0, "type": "high"},
            {"index": 2, "price": 6.0, "type": "low"},
            {"index": 3, "price": 12.0, "type": "high"},
            {"index": 4, "price": 7.0, "type": "low"},
        ]
    )

    assert result == [
        {
            "index": 1,
            "price": 10.0,
            "type": "high",
            "classification": None,
        },
        {
            "index": 2,
            "price": 6.0,
            "type": "low",
            "classification": None,
        },
        {
            "index": 3,
            "price": 12.0,
            "type": "high",
            "classification": "HH",
        },
        {
            "index": 4,
            "price": 7.0,
            "type": "low",
            "classification": "HL",
        },
    ]


def test_structural_point_classifier_handles_consecutive_same_type_points():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 10.0, "type": "high"},
            {"index": 2, "price": 12.0, "type": "high"},
            {"index": 3, "price": 11.0, "type": "high"},
        ]
    )

    assert [
        point["classification"]
        for point in result
    ] == [None, "HH", "LH"]


def test_structural_point_classifier_leaves_equal_high_unclassified():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 10.0, "type": "high"},
            {"index": 3, "price": 10.0, "type": "high"},
        ]
    )

    assert result[1]["classification"] is None


def test_structural_point_classifier_leaves_equal_low_unclassified():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 6.0, "type": "low"},
            {"index": 3, "price": 6.0, "type": "low"},
        ]
    )

    assert result[1]["classification"] is None


def test_structural_point_classifier_uses_equal_point_as_new_reference():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {"index": 1, "price": 10.0, "type": "high"},
            {"index": 2, "price": 12.0, "type": "high"},
            {"index": 3, "price": 12.0, "type": "high"},
            {"index": 4, "price": 11.0, "type": "high"},
        ]
    )

    assert [
        point["classification"]
        for point in result
    ] == [None, "HH", None, "LH"]


def test_structural_point_classifier_preserves_confirmation_index():
    classifier = StructuralPointClassifier()

    result = classifier.classify(
        [
            {
                "index": 1,
                "confirmation_index": 2,
                "price": 10.0,
                "type": "high",
            },
            {
                "index": 3,
                "confirmation_index": 4,
                "price": 12.0,
                "type": "high",
            },
        ]
    )

    assert result == [
        {
            "index": 1,
            "confirmation_index": 2,
            "price": 10.0,
            "type": "high",
            "classification": None,
        },
        {
            "index": 3,
            "confirmation_index": 4,
            "price": 12.0,
            "type": "high",
            "classification": "HH",
        },
    ]


def test_structural_point_classifier_returns_empty_list():
    classifier = StructuralPointClassifier()

    assert classifier.classify([]) == []


def test_structural_point_classifier_rejects_invalid_point_type():
    classifier = StructuralPointClassifier()

    with pytest.raises(
        ValueError,
        match="point type must be high or low",
    ):
        classifier.classify(
            [
                {
                    "index": 1,
                    "price": 10.0,
                    "type": "invalid",
                }
            ]
        )


def test_structural_point_classifier_rejects_non_chronological_points():
    classifier = StructuralPointClassifier()

    with pytest.raises(
        ValueError,
        match="points must be in chronological order",
    ):
        classifier.classify(
            [
                {"index": 3, "price": 10.0, "type": "high"},
                {"index": 1, "price": 12.0, "type": "high"},
            ]
        )
