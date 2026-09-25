from backend.app.predictions.prediction_record import PredictionRecord


class PredictionRegistry:
    def __init__(self) -> None:
        self._records: list[PredictionRecord] = []

    @property
    def records(self) -> tuple[PredictionRecord, ...]:
        return tuple(self._records)

    def register(self, record: PredictionRecord) -> None:
        if not isinstance(record, PredictionRecord):
            raise TypeError(
                "record must be a PredictionRecord"
            )

        self._records.append(record)
