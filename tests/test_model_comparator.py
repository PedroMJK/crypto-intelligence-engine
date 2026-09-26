from unittest.mock import patch

import pytest

from backend.app.backtesting.accuracy_calculator import (
    AccuracyCalculator,
)
from backend.app.backtesting.confusion_matrix_calculator import (
    ConfusionMatrixCalculator,
)
from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.model_comparator import ModelComparator
from backend.app.backtesting.model_evaluation import ModelEvaluation
from backend.app.backtesting.precision_calculator import (
    PrecisionCalculator,
)
from backend.app.backtesting.recall_calculator import RecallCalculator
from backend.app.predictions.prediction_metrics import PredictionMetrics


def create_metrics(
    *,
    symbol="FETUSDT",
    prediction_timestamp=1_800_000_000_000,
    horizon_minutes=5,
    direction_score=0.60,
    future_return=0.05,
):
    return PredictionMetrics(
        symbol=symbol,
        prediction_timestamp=prediction_timestamp,
        horizon_minutes=horizon_minutes,
        direction_score=direction_score,
        future_return=future_return,
        directional_alignment=(
            direction_score * future_return
        ),
        absolute_return=abs(future_return),
    )


def test_model_comparator_returns_model_evaluation():
    metrics = [
        create_metrics(),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert isinstance(result, ModelEvaluation)


def test_model_comparator_preserves_model_name():
    metrics = [
        create_metrics(),
    ]

    result = ModelComparator.evaluate(
        "baseline-v2",
        metrics,
    )

    assert result.model_name == "baseline-v2"


def test_model_comparator_counts_samples():
    metrics = [
        create_metrics(),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
        ),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.sample_count == 2


def test_model_comparator_calculates_all_defined_metrics():
    metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_600_000,
            direction_score=-0.60,
            future_return=-0.05,
        ),
        create_metrics(
            prediction_timestamp=1_800_000_900_000,
            direction_score=-0.60,
            future_return=0.05,
        ),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.accuracy == 0.5
    assert result.precision == 0.5
    assert result.recall == 0.5
    assert result.confusion_matrix == DirectionalClassification(
        true_positive=1,
        false_positive=1,
        true_negative=1,
        false_negative=1,
    )


def test_model_comparator_delegates_to_confusion_matrix_calculator():
    metrics = [
        create_metrics(),
    ]

    classification = DirectionalClassification(
        true_positive=1,
        false_positive=0,
        true_negative=0,
        false_negative=0,
    )

    with patch.object(
        ConfusionMatrixCalculator,
        "calculate",
        return_value=classification,
    ) as calculate:
        result = ModelComparator.evaluate(
            "baseline",
            metrics,
        )

    calculate.assert_called_once_with(metrics)
    assert result.confusion_matrix is classification


def test_model_comparator_delegates_defined_accuracy():
    metrics = [
        create_metrics(),
    ]

    with patch.object(
        AccuracyCalculator,
        "calculate",
        return_value=0.80,
    ) as calculate:
        result = ModelComparator.evaluate(
            "baseline",
            metrics,
        )

    calculate.assert_called_once_with(metrics)
    assert result.accuracy == 0.80


def test_model_comparator_delegates_defined_precision():
    metrics = [
        create_metrics(),
    ]

    with patch.object(
        PrecisionCalculator,
        "calculate",
        return_value=0.75,
    ) as calculate:
        result = ModelComparator.evaluate(
            "baseline",
            metrics,
        )

    calculate.assert_called_once_with(metrics)
    assert result.precision == 0.75


def test_model_comparator_delegates_defined_recall():
    metrics = [
        create_metrics(),
    ]

    with patch.object(
        RecallCalculator,
        "calculate",
        return_value=0.70,
    ) as calculate:
        result = ModelComparator.evaluate(
            "baseline",
            metrics,
        )

    calculate.assert_called_once_with(metrics)
    assert result.recall == 0.70


def test_model_comparator_returns_none_for_undefined_accuracy():
    metrics = [
        create_metrics(
            direction_score=0.0,
            future_return=0.05,
        ),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.accuracy is None


def test_model_comparator_returns_none_for_undefined_precision():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.precision is None


def test_model_comparator_returns_none_for_undefined_recall():
    metrics = [
        create_metrics(
            direction_score=-0.60,
            future_return=-0.05,
        ),
    ]

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.recall is None


def test_model_comparator_accepts_tuple():
    metrics = (
        create_metrics(),
    )

    result = ModelComparator.evaluate(
        "baseline",
        metrics,
    )

    assert result.sample_count == 1


@pytest.mark.parametrize(
    "metrics",
    [
        None,
        123,
        True,
        "metrics",
        {},
        set(),
    ],
)
def test_model_comparator_rejects_invalid_collection(metrics):
    with pytest.raises(TypeError):
        ModelComparator.evaluate(
            "baseline",
            metrics,
        )


def test_model_comparator_rejects_empty_list():
    with pytest.raises(ValueError):
        ModelComparator.evaluate(
            "baseline",
            [],
        )


def test_model_comparator_rejects_empty_tuple():
    with pytest.raises(ValueError):
        ModelComparator.evaluate(
            "baseline",
            (),
        )


@pytest.mark.parametrize(
    "invalid_item",
    [
        None,
        123,
        True,
        "metrics",
        {},
        [],
        (),
    ],
)
def test_model_comparator_rejects_invalid_metric_item(
    invalid_item,
):
    with pytest.raises(TypeError):
        ModelComparator.evaluate(
            "baseline",
            [
                create_metrics(),
                invalid_item,
            ],
        )


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
def test_model_comparator_rejects_invalid_model_name(
    model_name,
):
    with pytest.raises(TypeError):
        ModelComparator.evaluate(
            model_name,
            [create_metrics()],
        )


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
def test_model_comparator_rejects_blank_model_name(
    model_name,
):
    with pytest.raises(ValueError):
        ModelComparator.evaluate(
            model_name,
            [create_metrics()],
        )


def test_model_comparator_compares_multiple_models():
    baseline_metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=0.05,
        ),
    ]
    candidate_metrics = [
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=-0.60,
            future_return=-0.05,
        ),
    ]

    result = ModelComparator.compare(
        [
            ("baseline", baseline_metrics),
            ("candidate", candidate_metrics),
        ]
    )

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(
        isinstance(evaluation, ModelEvaluation)
        for evaluation in result
    )


def test_model_comparator_preserves_model_order():
    metrics = [
        create_metrics(),
    ]

    result = ModelComparator.compare(
        [
            ("model-b", metrics),
            ("model-a", metrics),
            ("model-c", metrics),
        ]
    )

    assert tuple(
        evaluation.model_name
        for evaluation in result
    ) == (
        "model-b",
        "model-a",
        "model-c",
    )


def test_model_comparator_evaluates_each_model():
    baseline_metrics = [
        create_metrics(),
    ]
    candidate_metrics = [
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
        ),
    ]

    with patch.object(
        ModelComparator,
        "evaluate",
        side_effect=[
            ModelEvaluation(
                model_name="baseline",
                sample_count=1,
                accuracy=1.0,
                precision=1.0,
                recall=1.0,
                confusion_matrix=DirectionalClassification(
                    true_positive=1,
                    false_positive=0,
                    true_negative=0,
                    false_negative=0,
                ),
            ),
            ModelEvaluation(
                model_name="candidate",
                sample_count=1,
                accuracy=1.0,
                precision=1.0,
                recall=1.0,
                confusion_matrix=DirectionalClassification(
                    true_positive=1,
                    false_positive=0,
                    true_negative=0,
                    false_negative=0,
                ),
            ),
        ],
    ) as evaluate:
        result = ModelComparator.compare(
            [
                ("baseline", baseline_metrics),
                ("candidate", candidate_metrics),
            ]
        )

    assert len(result) == 2
    assert evaluate.call_count == 2
    evaluate.assert_any_call(
        "baseline",
        baseline_metrics,
    )
    evaluate.assert_any_call(
        "candidate",
        candidate_metrics,
    )


def test_model_comparator_does_not_rank_models():
    weaker_metrics = [
        create_metrics(
            direction_score=0.60,
            future_return=-0.05,
        ),
    ]
    stronger_metrics = [
        create_metrics(
            prediction_timestamp=1_800_000_300_000,
            direction_score=0.60,
            future_return=0.05,
        ),
    ]

    result = ModelComparator.compare(
        [
            ("weaker", weaker_metrics),
            ("stronger", stronger_metrics),
        ]
    )

    assert tuple(
        evaluation.model_name
        for evaluation in result
    ) == (
        "weaker",
        "stronger",
    )


def test_model_comparator_accepts_tuple_of_models():
    metrics = [
        create_metrics(),
    ]

    result = ModelComparator.compare(
        (
            ("baseline", metrics),
            ("candidate", metrics),
        )
    )

    assert len(result) == 2


@pytest.mark.parametrize(
    "models",
    [
        None,
        123,
        True,
        "models",
        {},
        set(),
    ],
)
def test_model_comparator_rejects_invalid_models_collection(
    models,
):
    with pytest.raises(TypeError):
        ModelComparator.compare(models)


def test_model_comparator_rejects_empty_models_list():
    with pytest.raises(ValueError):
        ModelComparator.compare([])


def test_model_comparator_rejects_empty_models_tuple():
    with pytest.raises(ValueError):
        ModelComparator.compare(())


@pytest.mark.parametrize(
    "model",
    [
        None,
        123,
        True,
        "model",
        {},
        [],
        (),
        ("baseline",),
        ("baseline", [], "extra"),
    ],
)
def test_model_comparator_rejects_invalid_model_entry(
    model,
):
    with pytest.raises(TypeError):
        ModelComparator.compare([model])
