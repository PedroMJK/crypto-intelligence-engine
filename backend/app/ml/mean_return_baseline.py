from backend.app.ml.ml_dataset import MLDataset


class MeanReturnBaseline:
    def __init__(self) -> None:
        self._means_by_horizon: dict[int, float] = {}
        self._is_fitted = False

    def fit(
        self,
        dataset: MLDataset,
    ) -> None:
        self._validate_dataset(dataset)

        targets_by_horizon: dict[
            int,
            list[float],
        ] = {}

        for sample in dataset.samples:
            targets_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample.target)

        self._means_by_horizon = {
            horizon_minutes: (
                sum(targets)
                / len(targets)
            )
            for horizon_minutes, targets
            in targets_by_horizon.items()
        }

        self._is_fitted = True

    def predict(
        self,
        horizon_minutes: int,
    ) -> float:
        self._validate_fitted()
        self._validate_horizon_minutes(
            horizon_minutes
        )
        self._validate_known_horizon(
            horizon_minutes
        )

        return self._means_by_horizon[
            horizon_minutes
        ]

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )

    def _validate_fitted(self) -> None:
        if not self._is_fitted:
            raise RuntimeError(
                "baseline must be fitted before prediction"
            )

    @staticmethod
    def _validate_horizon_minutes(
        horizon_minutes: int,
    ) -> None:
        if (
            isinstance(horizon_minutes, bool)
            or not isinstance(horizon_minutes, int)
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
        if horizon_minutes not in self._means_by_horizon:
            raise ValueError(
                "horizon_minutes was not observed during training"
            )
