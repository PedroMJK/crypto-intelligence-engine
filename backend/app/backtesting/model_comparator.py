from backend.app.backtesting.accuracy_calculator import (
    AccuracyCalculator,
)
from backend.app.backtesting.confusion_matrix_calculator import (
    ConfusionMatrixCalculator,
)
from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)
from backend.app.backtesting.model_evaluation import ModelEvaluation
from backend.app.backtesting.precision_calculator import (
    PrecisionCalculator,
)
from backend.app.backtesting.recall_calculator import RecallCalculator
from backend.app.predictions.prediction_metrics import PredictionMetrics


class ModelComparator:
    @staticmethod
    def compare(
        models: list[tuple[str, list[PredictionMetrics] | tuple[PredictionMetrics, ...]]]
        | tuple[
            tuple[str, list[PredictionMetrics] | tuple[PredictionMetrics, ...]],
            ...,
        ],
    ) -> tuple[ModelEvaluation, ...]:
        ModelComparator._validate_models(models)

        return tuple(
            ModelComparator.evaluate(
                model_name,
                metrics,
            )
            for model_name, metrics in models
        )

    @staticmethod
    def _validate_models(
        models,
    ) -> None:
        if not isinstance(models, (list, tuple)):
            raise TypeError(
                "models must be a list or tuple"
            )

        if not models:
            raise ValueError(
                "models must not be empty"
            )

        for model in models:
            if (
                not isinstance(model, tuple)
                or len(model) != 2
            ):
                raise TypeError(
                    "each model must be a tuple containing model_name and metrics"
                )

    @staticmethod
    def evaluate(
        model_name: str,
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> ModelEvaluation:
        ModelComparator._validate_model_name(model_name)

        confusion_matrix = ConfusionMatrixCalculator.calculate(metrics)

        accuracy = ModelComparator._calculate_accuracy(
            metrics,
            confusion_matrix,
        )
        precision = ModelComparator._calculate_precision(
            metrics,
            confusion_matrix,
        )
        recall = ModelComparator._calculate_recall(
            metrics,
            confusion_matrix,
        )

        return ModelEvaluation(
            model_name=model_name,
            sample_count=len(metrics),
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            confusion_matrix=confusion_matrix,
        )

    @staticmethod
    def _validate_model_name(
        model_name: str,
    ) -> None:
        if not isinstance(model_name, str):
            raise TypeError(
                "model_name must be a str"
            )

        if not model_name.strip():
            raise ValueError(
                "model_name must not be blank"
            )

    @staticmethod
    def _calculate_accuracy(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
        confusion_matrix: DirectionalClassification,
    ) -> float | None:
        evaluated_count = (
            confusion_matrix.true_positive
            + confusion_matrix.false_positive
            + confusion_matrix.true_negative
            + confusion_matrix.false_negative
        )

        if evaluated_count == 0:
            return None

        return AccuracyCalculator.calculate(metrics)

    @staticmethod
    def _calculate_precision(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
        confusion_matrix: DirectionalClassification,
    ) -> float | None:
        predicted_positive = (
            confusion_matrix.true_positive
            + confusion_matrix.false_positive
        )

        if predicted_positive == 0:
            return None

        return PrecisionCalculator.calculate(metrics)

    @staticmethod
    def _calculate_recall(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
        confusion_matrix: DirectionalClassification,
    ) -> float | None:
        actual_positive = (
            confusion_matrix.true_positive
            + confusion_matrix.false_negative
        )

        if actual_positive == 0:
            return None

        return RecallCalculator.calculate(metrics)
