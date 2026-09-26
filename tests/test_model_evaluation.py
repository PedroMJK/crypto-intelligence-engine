from dataclasses import FrozenInstanceError
import math

import pytest

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.model_evaluation import ModelEvaluation


def create_confusion_matrix():
    return DirectionalClassification(
        true_positive=3,
        false_positive=1,
        true_negative=4,
        false_negative=2,
    )


def create_evaluation(
    *,
    model_name="baseline",
    sample_count=10,
    accuracy=0.70,
    precision=0.75,
    recall=0.60,
    confusion_matrix=None,
):
    if confusion_matrix is None:
        confusion_matrix = create_confusion_matrix()

    return ModelEvaluation(
        model_name=model_name,
        sample_count=sample_count,
        accuracy=accuracy,
        precision=precision,
        recall=recall,
        confusion_matrix=confusion_matrix,
    )


def test_model_evaluation_stores_values():
    confusion_matrix = create_confusion_matrix()

    evaluation = create_evaluation(
        model_name="baseline",
        sample_count=10,
        accuracy=0.70,
        precision=0.75,
        recall=0.60,
        confusion_matrix=confusion_matrix,
    )

    assert evaluation.model_name == "baseline"
    assert evaluation.sample_count == 10
    assert evaluation.accuracy == 0.70
    assert evaluation.precision == 0.75
    assert evaluation.recall == 0.60
    assert evaluation.confusion_matrix is confusion_matrix


def test_model_evaluation_is_immutable():
    evaluation = create_evaluation()

    with pytest.raises(FrozenInstanceError):
        evaluation.model_name = "changed"


@pytest.mark.parametrize(
    "model_name",
    [
        None,
        123,
        True,
        [],
        {},
        (),
    ],
)
def test_model_evaluation_rejects_non_string_model_name(
    model_name,
):
    with pytest.raises(TypeError):
        create_evaluation(model_name=model_name)


@pytest.mark.parametrize(
    "model_name",
    [
        "",
        " ",
        "   ",
        "\t",
        "\n",
    ],
)
def test_model_evaluation_rejects_blank_model_name(
    model_name,
):
    with pytest.raises(ValueError):
        create_evaluation(model_name=model_name)


def test_model_evaluation_preserves_model_name():
    evaluation = create_evaluation(
        model_name="  baseline-v2  ",
    )

    assert evaluation.model_name == "  baseline-v2  "


@pytest.mark.parametrize(
    "sample_count",
    [
        None,
        1.0,
        True,
        False,
        "10",
        [],
        {},
    ],
)
def test_model_evaluation_rejects_invalid_sample_count_type(
    sample_count,
):
    with pytest.raises(TypeError):
        create_evaluation(sample_count=sample_count)


@pytest.mark.parametrize(
    "sample_count",
    [
        -10,
        -1,
        0,
    ],
)
def test_model_evaluation_rejects_non_positive_sample_count(
    sample_count,
):
    with pytest.raises(ValueError):
        create_evaluation(sample_count=sample_count)


@pytest.mark.parametrize(
    "metric_name",
    [
        "accuracy",
        "precision",
        "recall",
    ],
)
def test_model_evaluation_accepts_none_for_undefined_metric(
    metric_name,
):
    values = {
        "accuracy": 0.70,
        "precision": 0.75,
        "recall": 0.60,
    }
    values[metric_name] = None

    evaluation = create_evaluation(**values)

    assert getattr(evaluation, metric_name) is None


@pytest.mark.parametrize(
    ("metric_name", "value"),
    [
        ("accuracy", 0.0),
        ("accuracy", 1.0),
        ("precision", 0.0),
        ("precision", 1.0),
        ("recall", 0.0),
        ("recall", 1.0),
    ],
)
def test_model_evaluation_accepts_metric_boundaries(
    metric_name,
    value,
):
    values = {
        "accuracy": 0.70,
        "precision": 0.75,
        "recall": 0.60,
    }
    values[metric_name] = value

    evaluation = create_evaluation(**values)

    assert getattr(evaluation, metric_name) == value


@pytest.mark.parametrize(
    ("metric_name", "value"),
    [
        ("accuracy", -0.01),
        ("accuracy", 1.01),
        ("precision", -0.01),
        ("precision", 1.01),
        ("recall", -0.01),
        ("recall", 1.01),
    ],
)
def test_model_evaluation_rejects_metric_outside_range(
    metric_name,
    value,
):
    values = {
        "accuracy": 0.70,
        "precision": 0.75,
        "recall": 0.60,
    }
    values[metric_name] = value

    with pytest.raises(ValueError):
        create_evaluation(**values)


@pytest.mark.parametrize(
    ("metric_name", "value"),
    [
        ("accuracy", math.nan),
        ("accuracy", math.inf),
        ("accuracy", -math.inf),
        ("precision", math.nan),
        ("precision", math.inf),
        ("precision", -math.inf),
        ("recall", math.nan),
        ("recall", math.inf),
        ("recall", -math.inf),
    ],
)
def test_model_evaluation_rejects_non_finite_metric(
    metric_name,
    value,
):
    values = {
        "accuracy": 0.70,
        "precision": 0.75,
        "recall": 0.60,
    }
    values[metric_name] = value

    with pytest.raises(ValueError):
        create_evaluation(**values)


@pytest.mark.parametrize(
    ("metric_name", "value"),
    [
        ("accuracy", True),
        ("accuracy", "0.70"),
        ("accuracy", []),
        ("precision", True),
        ("precision", "0.75"),
        ("precision", {}),
        ("recall", True),
        ("recall", "0.60"),
        ("recall", ()),
    ],
)
def test_model_evaluation_rejects_invalid_metric_type(
    metric_name,
    value,
):
    values = {
        "accuracy": 0.70,
        "precision": 0.75,
        "recall": 0.60,
    }
    values[metric_name] = value

    with pytest.raises(TypeError):
        create_evaluation(**values)


@pytest.mark.parametrize(
    "confusion_matrix",
    [
        None,
        123,
        True,
        "matrix",
        {},
        [],
        (),
    ],
)
def test_model_evaluation_rejects_invalid_confusion_matrix(
    confusion_matrix,
):
    with pytest.raises(TypeError):
        ModelEvaluation(
            model_name="baseline",
            sample_count=10,
            accuracy=0.70,
            precision=0.75,
            recall=0.60,
            confusion_matrix=confusion_matrix,
        )
