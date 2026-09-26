from backend.app.ml.directional_comparison_metrics import (
    DirectionalComparisonMetrics,
)
from backend.app.ml.model_comparison_dataset import (
    ModelComparisonDataset,
)


class ModelComparisonEvaluator:
    @staticmethod
    def evaluate(
        dataset: ModelComparisonDataset,
    ) -> dict[
        int,
        tuple[
            DirectionalComparisonMetrics,
            DirectionalComparisonMetrics,
        ],
    ]:
        ModelComparisonEvaluator._validate_dataset(
            dataset
        )

        directional_samples_by_horizon: dict[
            int,
            list,
        ] = {}

        for sample in dataset.samples:
            if sample.observed_return == 0.0:
                continue

            directional_samples_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample)

        ModelComparisonEvaluator._validate_directional_observations(
            directional_samples_by_horizon
        )

        results: dict[
            int,
            tuple[
                DirectionalComparisonMetrics,
                DirectionalComparisonMetrics,
            ],
        ] = {}

        for (
            horizon_minutes,
            samples,
        ) in directional_samples_by_horizon.items():
            traditional_metrics = (
                ModelComparisonEvaluator._calculate_metrics(
                    predictions=[
                        sample.traditional_direction_score
                        for sample in samples
                    ],
                    observations=[
                        sample.observed_return
                        for sample in samples
                    ],
                )
            )

            ml_metrics = (
                ModelComparisonEvaluator._calculate_metrics(
                    predictions=[
                        sample.ml_predicted_return
                        for sample in samples
                    ],
                    observations=[
                        sample.observed_return
                        for sample in samples
                    ],
                )
            )

            results[horizon_minutes] = (
                traditional_metrics,
                ml_metrics,
            )

        return results

    @staticmethod
    def _validate_dataset(
        dataset: ModelComparisonDataset,
    ) -> None:
        if not isinstance(
            dataset,
            ModelComparisonDataset,
        ):
            raise TypeError(
                "dataset must be a ModelComparisonDataset"
            )

    @staticmethod
    def _validate_directional_observations(
        directional_samples_by_horizon: dict[
            int,
            list,
        ],
    ) -> None:
        if not directional_samples_by_horizon:
            raise ValueError(
                "dataset must contain at least one "
                "directional observation"
            )

    @staticmethod
    def _calculate_metrics(
        predictions: list[float],
        observations: list[float],
    ) -> DirectionalComparisonMetrics:
        correct_predictions = 0
        evaluated_predictions = 0
        neutral_predictions = 0

        for (
            prediction,
            observation,
        ) in zip(
            predictions,
            observations,
        ):
            if prediction == 0.0:
                neutral_predictions += 1
                continue

            evaluated_predictions += 1

            if (
                ModelComparisonEvaluator._direction(
                    prediction
                )
                == ModelComparisonEvaluator._direction(
                    observation
                )
            ):
                correct_predictions += 1

        directional_accuracy = (
            correct_predictions
            / evaluated_predictions
            if evaluated_predictions > 0
            else 0.0
        )

        return DirectionalComparisonMetrics(
            directional_accuracy=directional_accuracy,
            correct_predictions=correct_predictions,
            evaluated_predictions=evaluated_predictions,
            neutral_predictions=neutral_predictions,
        )

    @staticmethod
    def _direction(
        value: float,
    ) -> int:
        if value > 0.0:
            return 1

        return -1
