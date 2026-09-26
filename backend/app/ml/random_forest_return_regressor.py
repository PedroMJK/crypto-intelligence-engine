from sklearn.ensemble import RandomForestRegressor

from backend.app.ml.ml_dataset import MLDataset
from backend.app.predictions.feature_snapshot import FeatureSnapshot


class RandomForestReturnRegressor:
    def __init__(
        self,
        n_estimators: int = 100,
        random_state: int | None = 42,
    ) -> None:
        self._validate_n_estimators(
            n_estimators
        )
        self._validate_random_state(
            random_state
        )

        self._n_estimators = n_estimators
        self._random_state = random_state
        self._models_by_horizon: dict[
            int,
            RandomForestRegressor,
        ] = {}
        self._feature_names: tuple[str, ...] = ()
        self._is_fitted = False

    def fit(
        self,
        dataset: MLDataset,
    ) -> None:
        self._validate_dataset(dataset)

        feature_names = self._build_feature_names(
            dataset
        )
        self._validate_training_feature_schemas(
            dataset,
            feature_names,
        )

        samples_by_horizon = self._group_by_horizon(
            dataset
        )

        models_by_horizon: dict[
            int,
            RandomForestRegressor,
        ] = {}

        for (
            horizon_minutes,
            samples,
        ) in samples_by_horizon.items():
            training_features = [
                self._build_feature_vector(
                    sample.features,
                    feature_names,
                )
                for sample in samples
            ]
            training_targets = [
                sample.target
                for sample in samples
            ]

            model = RandomForestRegressor(
                n_estimators=self._n_estimators,
                random_state=self._random_state,
            )
            model.fit(
                training_features,
                training_targets,
            )

            models_by_horizon[
                horizon_minutes
            ] = model

        self._feature_names = feature_names
        self._models_by_horizon = (
            models_by_horizon
        )
        self._is_fitted = True

    def predict(
        self,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        self._validate_fitted()
        self._validate_features(features)
        self._validate_horizon_minutes(
            horizon_minutes
        )
        self._validate_known_horizon(
            horizon_minutes
        )
        self._validate_prediction_feature_schema(
            features
        )

        feature_vector = (
            self._build_feature_vector(
                features,
                self._feature_names,
            )
        )

        prediction = self._models_by_horizon[
            horizon_minutes
        ].predict(
            [feature_vector]
        )[0]

        return float(prediction)

    @staticmethod
    def _validate_n_estimators(
        n_estimators: int,
    ) -> None:
        if (
            isinstance(n_estimators, bool)
            or not isinstance(n_estimators, int)
        ):
            raise TypeError(
                "n_estimators must be an int"
            )

        if n_estimators <= 0:
            raise ValueError(
                "n_estimators must be greater than zero"
            )

    @staticmethod
    def _validate_random_state(
        random_state: int | None,
    ) -> None:
        if random_state is None:
            return

        if (
            isinstance(random_state, bool)
            or not isinstance(random_state, int)
        ):
            raise TypeError(
                "random_state must be an int or None"
            )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )

    @staticmethod
    def _validate_features(
        features: FeatureSnapshot,
    ) -> None:
        if not isinstance(
            features,
            FeatureSnapshot,
        ):
            raise TypeError(
                "features must be a FeatureSnapshot"
            )

    def _validate_fitted(self) -> None:
        if not self._is_fitted:
            raise RuntimeError(
                "model must be fitted before prediction"
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
        if (
            horizon_minutes
            not in self._models_by_horizon
        ):
            raise ValueError(
                "horizon_minutes was not observed during training"
            )

    @staticmethod
    def _build_feature_names(
        dataset: MLDataset,
    ) -> tuple[str, ...]:
        first_sample = dataset.samples[0]

        return tuple(
            sorted(
                first_sample.features.features.keys()
            )
        )

    @staticmethod
    def _validate_training_feature_schemas(
        dataset: MLDataset,
        feature_names: tuple[str, ...],
    ) -> None:
        expected_feature_names = set(
            feature_names
        )

        for sample in dataset.samples:
            current_feature_names = set(
                sample.features.features.keys()
            )

            if (
                current_feature_names
                != expected_feature_names
            ):
                raise ValueError(
                    "all training samples must use the same feature schema"
                )

    def _validate_prediction_feature_schema(
        self,
        features: FeatureSnapshot,
    ) -> None:
        if (
            set(features.features.keys())
            != set(self._feature_names)
        ):
            raise ValueError(
                "prediction feature schema must match training feature schema"
            )

    @staticmethod
    def _group_by_horizon(
        dataset: MLDataset,
    ) -> dict[int, list]:
        samples_by_horizon: dict[
            int,
            list,
        ] = {}

        for sample in dataset.samples:
            samples_by_horizon.setdefault(
                sample.horizon_minutes,
                [],
            ).append(sample)

        return samples_by_horizon

    @staticmethod
    def _build_feature_vector(
        features: FeatureSnapshot,
        feature_names: tuple[str, ...],
    ) -> list[float]:
        return [
            features.features[feature_name]
            for feature_name in feature_names
        ]
