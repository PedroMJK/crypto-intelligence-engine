from backend.app.predictions.prediction_metrics import PredictionMetrics


class AccuracyCalculator:
    @staticmethod
    def calculate(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> float:
        AccuracyCalculator._validate_collection(metrics)

        aligned_count = 0
        opposed_count = 0

        for metric in metrics:
            if metric.directional_alignment > 0:
                aligned_count += 1
            elif metric.directional_alignment < 0:
                opposed_count += 1

        evaluated_count = aligned_count + opposed_count

        if evaluated_count == 0:
            raise ValueError(
                "metrics must contain at least one directional observation"
            )

        return aligned_count / evaluated_count

    @staticmethod
    def _validate_collection(
        metrics: list[PredictionMetrics] | tuple[PredictionMetrics, ...],
    ) -> None:
        if not isinstance(metrics, (list, tuple)):
            raise TypeError(
                "metrics must be a list or tuple"
            )

        if not metrics:
            raise ValueError(
                "metrics must not be empty"
            )

        for metric in metrics:
            if not isinstance(metric, PredictionMetrics):
                raise TypeError(
                    "all metrics must be PredictionMetrics"
                )
