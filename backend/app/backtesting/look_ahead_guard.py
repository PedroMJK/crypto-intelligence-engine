from backend.app.backtesting.backtest_sample import BacktestSample


class LookAheadGuard:
    @staticmethod
    def validate(
        sample: BacktestSample,
    ) -> None:
        LookAheadGuard._validate_sample(sample)
        LookAheadGuard._validate_reference_time(sample)
        LookAheadGuard._validate_evaluation_time(sample)

    @staticmethod
    def _validate_sample(
        sample: BacktestSample,
    ) -> None:
        if not isinstance(sample, BacktestSample):
            raise TypeError(
                "sample must be a BacktestSample"
            )

    @staticmethod
    def _validate_reference_time(
        sample: BacktestSample,
    ) -> None:
        if (
            sample.features.feature_timestamp
            != sample.prediction.prediction_timestamp
        ):
            raise ValueError(
                "features must belong to the prediction reference time"
            )

    @staticmethod
    def _validate_evaluation_time(
        sample: BacktestSample,
    ) -> None:
        minimum_evaluation_timestamp = (
            sample.prediction.prediction_timestamp
            + sample.outcome.horizon_minutes * 60_000
        )

        if (
            sample.outcome.evaluation_timestamp
            < minimum_evaluation_timestamp
        ):
            raise ValueError(
                "outcome evaluation must not precede its horizon"
            )
