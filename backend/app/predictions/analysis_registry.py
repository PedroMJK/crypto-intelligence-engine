from backend.app.predictions.analysis_record import AnalysisRecord


class AnalysisRegistry:
    def __init__(self) -> None:
        self._records: list[AnalysisRecord] = []

    @property
    def records(self) -> tuple[AnalysisRecord, ...]:
        return tuple(self._records)

    def register(self, record: AnalysisRecord) -> None:
        if not isinstance(record, AnalysisRecord):
            raise TypeError(
                "record must be an AnalysisRecord"
            )

        self._records.append(record)
