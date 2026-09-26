import math

from sklearn.linear_model import LogisticRegression

from backend.app.ml.calibration_dataset import CalibrationDataset


class ReturnProbabilityCalibrator:
    def __init__(self) -> None:
        self._models_by_horizon: dict[
            int,
            LogisticRegression,
        ] = {}
        self._is_fitted = False

    def fit(
        self,
        dataset: CalibrationDataset,
    ) -> None:
        self._validate_dataset(dataset)

        samples_by_horizon = (
            self._group_directional_samples_by_horizon(
                dataset
            )
        )

        self._validate_horizon_classes(
            samples_by_horizon
        )

        models_by_horizon: dict[
            int,
            LogisticRegression,
        ] = {}

        for (
            horizon_minutes,
            samples,
        ) in samples_by_horizon.items():
            predicted_returns = [
                [sample.predicted_return]
                for sample in samples
            ]
            directional_targets = [
                self._build_directional_target(
                    sample.observed_return
                )
                for sample in samples
            ]

            model = LogisticRegression()
            model.fit(
                predicted_returns,
                directional_targets,
            )

            models_by_horizon[
                horizon_minutes
            ] = model

        self._models_by_horizon = (
            models_by_horizon
        )
        self._is_fitted = True

    def predict_probability(
        self,
        predicted_return: float,
        horizon_minutes: int,
    ) -> float:
        self._validate_fitted()
        self._validate_predicted_return(
            predicted_return
        )
        self._validate_horizon_minutes(
            horizon_minutes
        )
        self._validate_known_horizon(
            horizon_minutes
        )

        model = self._models_by_horizon[
            horizon_minutes
        ]

        probability = model.predict_proba(
            [[predicted_return]]
        )[0][1]

        return float(probability)

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

    def _validate_fitted(self) -> None:
        if not self._is_fitted:
            raise RuntimeError(
                "calibrator must be fitted before prediction"
            )

    @staticmethod
    def _validate_predicted_return(
        predicted_return: float,
    ) -> None:
        if (
            isinstance(predicted_return, bool)
            or not isinstance(
                predicted_return,
                (int, float),
            )
        ):
            raise TypeError(
                "predicted_return must be a number"
            )

        if not math.isfinite(
            predicted_return
        ):
            raise ValueError(
                "predicted_return must be finite"
            )

    @staticmethod
    def _validate_horizon_minutes(
        horizon_minutes: int,
    ) -> None:
        if (
            isinstance(horizon_minutes, bool)
            or not isinstance(
                horizon_minutes,
                int,
            )
        ):
            raise TypeError(
                "horizon_minutes must be an int"
            )

        if horizon_minutes <= 0:
            raise ValueError(
                "horizon_minutes must be greater than zero"
            )

    def _validate_known_horizon(
        self,
        horizon_minutes: int,
    ) -> None:
        if (
            horizon_minutes
            not in self._models_by_horizon
        ):
            raise ValueError(
                "horizon_minutes was not observed during calibration"
            )

    @staticmethod
    def _group_directional_samples_by_horizon(
        dataset: CalibrationDataset,
    ) -> dict[int, list]:
        samples_by_horizon: dict[
            int,
            list,
        ] = {}

        for sample in dataset.samples:
            if sample.observed_return == 0.0:
                continue

            samples_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample)

        return samples_by_horizon

    @staticmethod
    def _validate_horizon_classes(
        samples_by_horizon: dict[int, list],
    ) -> None:
        if not samples_by_horizon:
            raise ValueError(
                "each horizon must contain both positive "
                "and negative observed returns"
            )

        for samples in samples_by_horizon.values():
            has_positive = any(
                sample.observed_return > 0.0
                for sample in samples
            )
            has_negative = any(
                sample.observed_return < 0.0
                for sample in samples
            )

            if not (
                has_positive
                and has_negative
            ):
                raise ValueError(
                    "each horizon must contain both positive "
                    "and negative observed returns"
                )

    @staticmethod
    def _build_directional_target(
        observed_return: float,
    ) -> int:
        if observed_return > 0.0:
            return 1

        return 0
