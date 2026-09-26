import math
from typing import Protocol, runtime_checkable

from backend.app.ml.ml_sample import MLSample
from backend.app.ml.model_comparison_dataset import (
    ModelComparisonDataset,
)
from backend.app.ml.model_comparison_sample import (
    ModelComparisonSample,
)
from backend.app.predictions.analysis_record import AnalysisRecord
from backend.app.predictions.feature_snapshot import FeatureSnapshot


@runtime_checkable
class ComparisonReturnRegressor(Protocol):
    def predict(
        self,
        features: FeatureSnapshot,
        horizon_minutes: int,
    ) -> float:
        ...


class ModelComparisonDatasetBuilder:
    @staticmethod
    def build(
        model: ComparisonReturnRegressor,
        pairs: list[tuple[AnalysisRecord, MLSample]]
        | tuple[tuple[AnalysisRecord, MLSample], ...],
    ) -> ModelComparisonDataset:
        ModelComparisonDatasetBuilder._validate_model(
            model
        )
        ModelComparisonDatasetBuilder._validate_pairs(
            pairs
        )

        samples = tuple(
            ModelComparisonDatasetBuilder._build_sample(
                model=model,
                analysis=analysis,
                sample=sample,
            )
            for analysis, sample in pairs
        )

        return ModelComparisonDataset(
            samples=samples
        )

    @staticmethod
    def _build_sample(
        model: ComparisonReturnRegressor,
        analysis: AnalysisRecord,
        sample: MLSample,
    ) -> ModelComparisonSample:
        ModelComparisonDatasetBuilder._validate_compatibility(
            analysis,
            sample,
        )

        predicted_return = model.predict(
            features=sample.features,
            horizon_minutes=sample.horizon_minutes,
        )

        ModelComparisonDatasetBuilder._validate_prediction(
            predicted_return
        )

        return ModelComparisonSample(
            horizon_minutes=sample.horizon_minutes,
            traditional_direction_score=analysis.direction_score,
            ml_predicted_return=predicted_return,
            observed_return=sample.target,
        )

    @staticmethod
    def _validate_model(
        model: ComparisonReturnRegressor,
    ) -> None:
        predict = getattr(
            model,
            "predict",
            None,
        )

        if not callable(predict):
            raise TypeError(
                "model must provide a callable predict method"
            )

    @staticmethod
    def _validate_pairs(
        pairs: list[tuple[AnalysisRecord, MLSample]]
        | tuple[tuple[AnalysisRecord, MLSample], ...],
    ) -> None:
        if not isinstance(
            pairs,
            (list, tuple),
        ):
            raise TypeError(
                "pairs must be a list or tuple"
            )

        if not pairs:
            raise ValueError(
                "pairs must not be empty"
            )

        for pair in pairs:
            ModelComparisonDatasetBuilder._validate_pair(
                pair
            )

    @staticmethod
    def _validate_pair(
        pair: tuple[AnalysisRecord, MLSample],
    ) -> None:
        if (
            not isinstance(pair, tuple)
            or len(pair) != 2
        ):
            raise TypeError(
                "each pair must be a tuple with two items"
            )

        analysis, sample = pair

        ModelComparisonDatasetBuilder._validate_analysis(
            analysis
        )
        ModelComparisonDatasetBuilder._validate_sample(
            sample
        )

    @staticmethod
    def _validate_analysis(
        analysis: AnalysisRecord,
    ) -> None:
        if not isinstance(
            analysis,
            AnalysisRecord,
        ):
            raise TypeError(
                "analysis must be an AnalysisRecord"
            )

    @staticmethod
    def _validate_sample(
        sample: MLSample,
    ) -> None:
        if not isinstance(
            sample,
            MLSample,
        ):
            raise TypeError(
                "sample must be an MLSample"
            )

    @staticmethod
    def _validate_compatibility(
        analysis: AnalysisRecord,
        sample: MLSample,
    ) -> None:
        if (
            analysis.symbol
            != sample.features.symbol
        ):
            raise ValueError(
                "analysis and sample symbols must match"
            )

        if (
            analysis.reference_timestamp
            != sample.features.feature_timestamp
        ):
            raise ValueError(
                "analysis reference timestamp must match "
                "sample feature timestamp"
            )

    @staticmethod
    def _validate_prediction(
        prediction: float,
    ) -> None:
        if (
            isinstance(prediction, bool)
            or not isinstance(
                prediction,
                (int, float),
            )
        ):
            raise TypeError(
                "model prediction must be a number"
            )

        if not math.isfinite(prediction):
            raise ValueError(
                "model prediction must be finite"
            )
