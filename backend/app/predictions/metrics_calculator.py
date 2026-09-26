from backend.app.predictions.prediction_metrics import PredictionMetrics
from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


class MetricsCalculator:
    @staticmethod
    def calculate(
        prediction: PredictionRecord,
        outcome: PredictionOutcome,
    ) -> PredictionMetrics:
        MetricsCalculator._validate_prediction(prediction)
        MetricsCalculator._validate_outcome(outcome)
        MetricsCalculator._validate_compatibility(
            prediction,
            outcome,
        )

        future_return = outcome.future_return

        return PredictionMetrics(
            symbol=prediction.symbol,
            prediction_timestamp=prediction.prediction_timestamp,
            horizon_minutes=outcome.horizon_minutes,
            direction_score=prediction.direction_score,
            future_return=future_return,
            directional_alignment=(
                prediction.direction_score
                * future_return
            ),
            absolute_return=abs(future_return),
        )

    @staticmethod
    def _validate_prediction(
        prediction: PredictionRecord,
    ) -> None:
        if not isinstance(prediction, PredictionRecord):
            raise TypeError(
                "prediction must be a PredictionRecord"
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
        prediction: PredictionRecord,
        outcome: PredictionOutcome,
    ) -> None:
        if prediction.symbol != outcome.symbol:
            raise ValueError(
                "prediction and outcome symbols must match"
            )

        if (
            prediction.prediction_timestamp
            != outcome.prediction_timestamp
        ):
            raise ValueError(
                "prediction and outcome timestamps must match"
            )

        if prediction.reference_price != outcome.reference_price:
            raise ValueError(
                "prediction and outcome reference prices must match"
            )
