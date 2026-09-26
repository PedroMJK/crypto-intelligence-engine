from backend.app.backtesting.backtest_dataset import BacktestDataset
from backend.app.predictions.metrics_calculator import MetricsCalculator
from backend.app.predictions.prediction_metrics import PredictionMetrics


class BacktestSimulator:
    @staticmethod
    def run(
        dataset: BacktestDataset,
    ) -> tuple[PredictionMetrics, ...]:
        BacktestSimulator._validate_dataset(dataset)

        return tuple(
            MetricsCalculator.calculate(
                sample.prediction,
                sample.outcome,
            )
            for sample in dataset.samples
        )

    @staticmethod
    def _validate_dataset(
        dataset: BacktestDataset,
    ) -> None:
        if not isinstance(dataset, BacktestDataset):
            raise TypeError(
                "dataset must be a BacktestDataset"
            )
