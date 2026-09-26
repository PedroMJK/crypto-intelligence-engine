import pytest

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)


def test_directional_classification_stores_counts():
    classification = DirectionalClassification(
        true_positive=4,
        false_positive=2,
        true_negative=3,
        false_negative=1,
    )

    assert classification.true_positive == 4
    assert classification.false_positive == 2
    assert classification.true_negative == 3
    assert classification.false_negative == 1


def test_directional_classification_accepts_zero_counts():
    classification = DirectionalClassification(
        true_positive=0,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )

    assert classification.true_positive == 0
    assert classification.false_positive == 0
    assert classification.true_negative == 0
    assert classification.false_negative == 0


@pytest.mark.parametrize(
    "field_name",
    [
        "true_positive",
        "false_positive",
        "true_negative",
        "false_negative",
    ],
)
def test_directional_classification_rejects_negative_count(
    field_name,
):
    values = {
        "true_positive": 1,
        "false_positive": 1,
        "true_negative": 1,
        "false_negative": 1,
    }
    values[field_name] = -1

    with pytest.raises(ValueError):
        DirectionalClassification(**values)


@pytest.mark.parametrize(
    "invalid_value",
    [
        None,
        True,
        False,
        1.0,
        "1",
        [],
        {},
    ],
)
@pytest.mark.parametrize(
    "field_name",
    [
        "true_positive",
        "false_positive",
        "true_negative",
        "false_negative",
    ],
)
def test_directional_classification_rejects_invalid_count_type(
    field_name,
    invalid_value,
):
    values = {
        "true_positive": 1,
        "false_positive": 1,
        "true_negative": 1,
        "false_negative": 1,
    }
    values[field_name] = invalid_value

    with pytest.raises(TypeError):
        DirectionalClassification(**values)


def test_directional_classification_is_immutable():
    classification = DirectionalClassification(
        true_positive=1,
        false_positive=2,
        true_negative=3,
        false_negative=4,
    )

    with pytest.raises(AttributeError):
        classification.true_positive = 10
