import pytest

from backend.app.ml.directional_comparison_metrics import (
    DirectionalComparisonMetrics,
)
from backend.app.ml.model_comparison_dataset import (
    ModelComparisonDataset,
)
from backend.app.ml.model_comparison_evaluator import (
    ModelComparisonEvaluator,
)
from backend.app.ml.model_comparison_sample import (
    ModelComparisonSample,
)


def create_sample(
    *,
    horizon_minutes: int = 15,
    traditional_direction_score: float = 0.50,
    ml_predicted_return: float = 0.01,
    observed_return: float = 0.02,
) -> ModelComparisonSample:
    return ModelComparisonSample(
        horizon_minutes=horizon_minutes,
        traditional_direction_score=traditional_direction_score,
        ml_predicted_return=ml_predicted_return,
        observed_return=observed_return,
    )


def test_evaluate_returns_metrics_per_horizon():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    assert set(result.keys()) == {15}

    traditional_metrics, ml_metrics = result[15]

    assert isinstance(
        traditional_metrics,
        DirectionalComparisonMetrics,
    )
    assert isinstance(
        ml_metrics,
        DirectionalComparisonMetrics,
    )


def test_evaluate_calculates_directional_accuracy():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                traditional_direction_score=0.50,
                ml_predicted_return=0.01,
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=0.50,
                ml_predicted_return=-0.01,
                observed_return=-0.02,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=0.01,
                observed_return=-0.03,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=-0.01,
                observed_return=0.03,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.correct_predictions == 2
    assert traditional.evaluated_predictions == 4
    assert traditional.directional_accuracy == pytest.approx(
        0.50
    )

    assert ml.correct_predictions == 2
    assert ml.evaluated_predictions == 4
    assert ml.directional_accuracy == pytest.approx(
        0.50
    )


def test_evaluate_groups_results_by_horizon():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
            ),
            create_sample(
                horizon_minutes=30,
                traditional_direction_score=-0.50,
                ml_predicted_return=-0.01,
                observed_return=-0.02,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    assert set(result.keys()) == {
        5,
        30,
    }


def test_evaluate_excludes_zero_observed_return():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=-0.90,
                ml_predicted_return=-0.90,
                observed_return=0.0,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.evaluated_predictions == 1
    assert ml.evaluated_predictions == 1
    assert traditional.neutral_predictions == 0
    assert ml.neutral_predictions == 0


def test_evaluate_tracks_traditional_neutral_prediction():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                traditional_direction_score=0.0,
                ml_predicted_return=0.01,
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=-0.01,
                observed_return=-0.02,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.neutral_predictions == 1
    assert traditional.evaluated_predictions == 1
    assert traditional.correct_predictions == 1
    assert traditional.directional_accuracy == pytest.approx(
        1.0
    )

    assert ml.neutral_predictions == 0
    assert ml.evaluated_predictions == 2


def test_evaluate_tracks_ml_neutral_prediction():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                traditional_direction_score=0.50,
                ml_predicted_return=0.0,
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=-0.01,
                observed_return=-0.02,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.neutral_predictions == 0
    assert traditional.evaluated_predictions == 2

    assert ml.neutral_predictions == 1
    assert ml.evaluated_predictions == 1
    assert ml.correct_predictions == 1
    assert ml.directional_accuracy == pytest.approx(
        1.0
    )


def test_evaluate_handles_horizon_with_only_neutral_traditional_predictions():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                traditional_direction_score=0.0,
                ml_predicted_return=0.01,
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=0.0,
                ml_predicted_return=-0.01,
                observed_return=-0.02,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.directional_accuracy == 0.0
    assert traditional.correct_predictions == 0
    assert traditional.evaluated_predictions == 0
    assert traditional.neutral_predictions == 2

    assert ml.directional_accuracy == pytest.approx(
        1.0
    )


def test_evaluate_handles_horizon_with_only_neutral_ml_predictions():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                traditional_direction_score=0.50,
                ml_predicted_return=0.0,
                observed_return=0.02,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=0.0,
                observed_return=-0.02,
            ),
        ]
    )

    result = ModelComparisonEvaluator.evaluate(
        dataset
    )

    traditional, ml = result[15]

    assert traditional.directional_accuracy == pytest.approx(
        1.0
    )

    assert ml.directional_accuracy == 0.0
    assert ml.correct_predictions == 0
    assert ml.evaluated_predictions == 0
    assert ml.neutral_predictions == 2


def test_evaluate_rejects_dataset_with_only_zero_observed_returns():
    dataset = ModelComparisonDataset(
        samples=[
            create_sample(
                observed_return=0.0,
            ),
            create_sample(
                traditional_direction_score=-0.50,
                ml_predicted_return=-0.01,
                observed_return=0.0,
            ),
        ]
    )

    with pytest.raises(
        ValueError,
        match=(
            "dataset must contain at least one "
            "directional observation"
        ),
    ):
        ModelComparisonEvaluator.evaluate(
            dataset
        )


@pytest.mark.parametrize(
    "dataset",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_evaluate_rejects_invalid_dataset(
    dataset,
):
    with pytest.raises(
        TypeError,
        match=(
            "dataset must be a ModelComparisonDataset"
        ),
    ):
        ModelComparisonEvaluator.evaluate(
            dataset
        )
