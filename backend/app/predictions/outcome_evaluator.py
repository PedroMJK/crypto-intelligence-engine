from backend.app.predictions.prediction_outcome import PredictionOutcome
from backend.app.predictions.prediction_record import PredictionRecord


class OutcomeEvaluator:
    @staticmethod
    def evaluate(
        prediction: PredictionRecord,
        horizon_minutes: int,
        evaluation_timestamp: int,
        evaluation_price: float,
    ) -> PredictionOutcome:
        if not isinstance(prediction, PredictionRecord):
            raise TypeError(
                "prediction must be a PredictionRecord"
            )

        return PredictionOutcome(
            symbol=prediction.symbol,
            prediction_timestamp=prediction.prediction_timestamp,
            reference_price=prediction.reference_price,
            horizon_minutes=horizon_minutes,
            evaluation_timestamp=evaluation_timestamp,
            evaluation_price=evaluation_price,
        )
