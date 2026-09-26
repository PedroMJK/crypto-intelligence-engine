import math

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.probability_calibration_metrics import (
    ProbabilityCalibrationMetrics,
)
from backend.app.ml.return_probability_calibrator import (
    ReturnProbabilityCalibrator,
)


class ProbabilityCalibrationEvaluator:
    @staticmethod
    def evaluate(
        calibrator: ReturnProbabilityCalibrator,
        dataset: CalibrationDataset,
    ) -> dict[int, ProbabilityCalibrationMetrics]:
        ProbabilityCalibrationEvaluator._validate_calibrator(
            calibrator
        )
        ProbabilityCalibrationEvaluator._validate_dataset(
            dataset
        )

        observations_by_horizon: dict[
            int,
            list[int],
        ] = {}
        probabilities_by_horizon: dict[
            int,
            list[float],
        ] = {}

        for sample in dataset.samples:
            if sample.observed_return == 0.0:
                continue

            probability = calibrator.predict_probability(
                predicted_return=sample.predicted_return,
                horizon_minutes=sample.horizon_minutes,
            )

            observation = (
                1
                if sample.observed_return > 0.0
                else 0
            )

            observations_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(observation)

            probabilities_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(probability)

        ProbabilityCalibrationEvaluator._validate_directional_observations(
            observations_by_horizon
        )

        metrics_by_horizon: dict[
            int,
            ProbabilityCalibrationMetrics,
        ] = {}

        for (
            horizon_minutes,
            observations,
        ) in observations_by_horizon.items():
            probabilities = probabilities_by_horizon[
                horizon_minutes
            ]

            metrics_by_horizon[
                horizon_minutes
            ] = ProbabilityCalibrationMetrics(
                brier_score=(
                    ProbabilityCalibrationEvaluator._calculate_brier_score(
                        observations,
                        probabilities,
                    )
                ),
                log_loss=(
                    ProbabilityCalibrationEvaluator._calculate_log_loss(
                        observations,
                        probabilities,
                    )
                ),
            )

        return metrics_by_horizon

    @staticmethod
    def _validate_calibrator(
        calibrator: ReturnProbabilityCalibrator,
    ) -> None:
        if not isinstance(
            calibrator,
            ReturnProbabilityCalibrator,
        ):
            raise TypeError(
                "calibrator must be a "
                "ReturnProbabilityCalibrator"
            )

    @staticmethod
    def _validate_dataset(
        dataset: CalibrationDataset,
    ) -> None:
        if not isinstance(
            dataset,
            CalibrationDataset,
        ):
            raise TypeError(
                "dataset must be a CalibrationDataset"
            )

    @staticmethod
    def _validate_directional_observations(
        observations_by_horizon: dict[
            int,
            list[int],
        ],
    ) -> None:
        if not observations_by_horizon:
            raise ValueError(
                "dataset must contain at least one "
                "directional observation"
            )

    @staticmethod
    def _calculate_brier_score(
        observations: list[int],
        probabilities: list[float],
    ) -> float:
        squared_errors = [
            (probability - observation) ** 2
            for observation, probability in zip(
                observations,
                probabilities,
            )
        ]

        return (
            sum(squared_errors)
            / len(squared_errors)
        )

    @staticmethod
    def _calculate_log_loss(
        observations: list[int],
        probabilities: list[float],
    ) -> float:
        epsilon = 1e-15

        losses = []

        for (
            observation,
            probability,
        ) in zip(
            observations,
            probabilities,
        ):
            clipped_probability = min(
                max(
                    probability,
                    epsilon,
                ),
                1.0 - epsilon,
            )

            loss = -(
                observation
                * math.log(
                    clipped_probability
                )
                + (1 - observation)
                * math.log(
                    1.0
                    - clipped_probability
                )
            )

            losses.append(loss)

        return sum(losses) / len(losses)
