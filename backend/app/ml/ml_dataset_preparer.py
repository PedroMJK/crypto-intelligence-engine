from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_outcome import PredictionOutcome


class MLDatasetPreparer:
    @staticmethod
    def prepare_sample(
        features: FeatureSnapshot,
        outcome: PredictionOutcome,
    ) -> MLSample:
        MLDatasetPreparer._validate_features(features)
        MLDatasetPreparer._validate_outcome(outcome)
        MLDatasetPreparer._validate_compatibility(
            features,
            outcome,
        )

        return MLSample(
            features=features,
            horizon_minutes=outcome.horizon_minutes,
            target=outcome.future_return,
        )

    @staticmethod
    def prepare_dataset(
        pairs: list[
            tuple[FeatureSnapshot, PredictionOutcome]
        ]
        | tuple[
            tuple[FeatureSnapshot, PredictionOutcome],
            ...,
        ],
    ) -> MLDataset:
        MLDatasetPreparer._validate_pairs(pairs)

        samples = tuple(
            MLDatasetPreparer.prepare_sample(
                features,
                outcome,
            )
            for features, outcome in pairs
        )

        return MLDataset(samples=samples)

    @staticmethod
    def _validate_features(
        features: FeatureSnapshot,
    ) -> None:
        if not isinstance(features, FeatureSnapshot):
            raise TypeError(
                "features must be a FeatureSnapshot"
            )

    @staticmethod
    def _validate_outcome(
        outcome: PredictionOutcome,
    ) -> None:
        if not isinstance(outcome, PredictionOutcome):
            raise TypeError(
                "outcome must be a PredictionOutcome"
            )

    @staticmethod
    def _validate_compatibility(
        features: FeatureSnapshot,
        outcome: PredictionOutcome,
    ) -> None:
        if features.symbol != outcome.symbol:
            raise ValueError(
                "feature and outcome symbols must match"
            )

        if (
            features.feature_timestamp
            != outcome.prediction_timestamp
        ):
            raise ValueError(
                "feature timestamp must match outcome prediction timestamp"
            )

    @staticmethod
    def _validate_pairs(
        pairs: list[
            tuple[FeatureSnapshot, PredictionOutcome]
        ]
        | tuple[
            tuple[FeatureSnapshot, PredictionOutcome],
            ...,
        ],
    ) -> None:
        if not isinstance(pairs, (list, tuple)):
            raise TypeError(
                "pairs must be a list or tuple"
            )

        if not pairs:
            raise ValueError(
                "pairs must not be empty"
            )

        for pair in pairs:
            MLDatasetPreparer._validate_pair(pair)

    @staticmethod
    def _validate_pair(
        pair: tuple[
            FeatureSnapshot,
            PredictionOutcome,
        ],
    ) -> None:
        if (
            not isinstance(pair, tuple)
            or len(pair) != 2
        ):
            raise TypeError(
                "each pair must be a tuple with two items"
            )
