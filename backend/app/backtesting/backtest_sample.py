from dataclasses import dataclass

from backend.app.predictions.feature_snapshot import FeatureSnapshot
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


@dataclass(frozen=True)
class BacktestSample:
    features: FeatureSnapshot
    prediction: PredictionRecord
    outcome: PredictionOutcome

    def __post_init__(self) -> None:
        self._validate_components()
        self._validate_symbols()
        self._validate_timestamps()
        self._validate_reference_prices()

    def _validate_components(self) -> None:
        if not isinstance(self.features, FeatureSnapshot):
            raise TypeError(
                "features must be a FeatureSnapshot"
            )

        if not isinstance(self.prediction, PredictionRecord):
            raise TypeError(
                "prediction must be a PredictionRecord"
            )

        if not isinstance(self.outcome, PredictionOutcome):
            raise TypeError(
                "outcome must be a PredictionOutcome"
            )

    def _validate_symbols(self) -> None:
        if self.features.symbol != self.prediction.symbol:
            raise ValueError(
                "feature and prediction symbols must match"
            )

        if self.prediction.symbol != self.outcome.symbol:
            raise ValueError(
                "prediction and outcome symbols must match"
            )

    def _validate_timestamps(self) -> None:
        if (
            self.features.feature_timestamp
            != self.prediction.prediction_timestamp
        ):
            raise ValueError(
                "feature and prediction timestamps must match"
            )

        if (
            self.prediction.prediction_timestamp
            != self.outcome.prediction_timestamp
        ):
            raise ValueError(
                "prediction and outcome timestamps must match"
            )

    def _validate_reference_prices(self) -> None:
        if (
            self.prediction.reference_price
            != self.outcome.reference_price
        ):
            raise ValueError(
                "prediction and outcome reference prices must match"
            )
