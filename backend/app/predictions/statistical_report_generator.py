from backend.app.predictions.prediction_metrics import PredictionMetrics
from backend.app.predictions.statistical_report import StatisticalReport


class StatisticalReportGenerator:
    @staticmethod
    def generate(
        metrics: list[PredictionMetrics]
        | tuple[PredictionMetrics, ...],
    ) -> StatisticalReport:
        StatisticalReportGenerator._validate_collection(
            metrics
        )
        StatisticalReportGenerator._validate_metrics(
            metrics
        )

        horizon_minutes = metrics[0].horizon_minutes

        StatisticalReportGenerator._validate_horizons(
            metrics,
            horizon_minutes,
        )

        sample_count = len(metrics)

        return StatisticalReport(
            horizon_minutes=horizon_minutes,
            sample_count=sample_count,
            mean_direction_score=(
                sum(
                    metric.direction_score
                    for metric in metrics
                )
                / sample_count
            ),
            mean_future_return=(
                sum(
                    metric.future_return
                    for metric in metrics
                )
                / sample_count
            ),
            mean_absolute_return=(
                sum(
                    metric.absolute_return
                    for metric in metrics
                )
                / sample_count
            ),
            mean_directional_alignment=(
                sum(
                    metric.directional_alignment
                    for metric in metrics
                )
                / sample_count
            ),
        )

    @staticmethod
    def _validate_collection(
        metrics: list[PredictionMetrics]
        | tuple[PredictionMetrics, ...],
    ) -> None:
        if not isinstance(metrics, (list, tuple)):
            raise TypeError(
                "metrics must be a list or tuple"
            )

        if not metrics:
            raise ValueError(
                "metrics must not be empty"
            )

    @staticmethod
    def _validate_metrics(
        metrics: list[PredictionMetrics]
        | tuple[PredictionMetrics, ...],
    ) -> None:
        for metric in metrics:
            if not isinstance(metric, PredictionMetrics):
                raise TypeError(
                    "all metrics must be PredictionMetrics"
                )

    @staticmethod
    def _validate_horizons(
        metrics: list[PredictionMetrics]
        | tuple[PredictionMetrics, ...],
        horizon_minutes: int,
    ) -> None:
        for metric in metrics:
            if metric.horizon_minutes != horizon_minutes:
                raise ValueError(
                    "all metrics must have the same horizon"
                )
