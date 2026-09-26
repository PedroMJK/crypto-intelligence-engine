import math

from backend.app.ml.regression_metrics import RegressionMetrics


class RegressionMetricsCalculator:
    @staticmethod
    def calculate(
        actual: list[float] | tuple[float, ...],
        predicted: list[float] | tuple[float, ...],
    ) -> RegressionMetrics:
        RegressionMetricsCalculator._validate_collections(
            actual,
            predicted,
        )
        RegressionMetricsCalculator._validate_lengths(
            actual,
            predicted,
        )
        RegressionMetricsCalculator._validate_values(
            actual,
            predicted,
        )

        absolute_errors = tuple(
            abs(actual_value - predicted_value)
            for actual_value, predicted_value in zip(
                actual,
                predicted,
            )
        )
        squared_errors = tuple(
            (actual_value - predicted_value) ** 2
            for actual_value, predicted_value in zip(
                actual,
                predicted,
            )
        )

        mae = (
            sum(absolute_errors)
            / len(absolute_errors)
        )
        mse = (
            sum(squared_errors)
            / len(squared_errors)
        )
        rmse = math.sqrt(mse)

        return RegressionMetrics(
            mae=mae,
            mse=mse,
            rmse=rmse,
        )

    @staticmethod
    def _validate_collections(
        actual: list[float] | tuple[float, ...],
        predicted: list[float] | tuple[float, ...],
    ) -> None:
        if (
            not isinstance(actual, (list, tuple))
            or not isinstance(predicted, (list, tuple))
        ):
            raise TypeError(
                "actual and predicted must be lists or tuples"
            )

        if not actual or not predicted:
            raise ValueError(
                "actual and predicted must not be empty"
            )

    @staticmethod
    def _validate_lengths(
        actual: list[float] | tuple[float, ...],
        predicted: list[float] | tuple[float, ...],
    ) -> None:
        if len(actual) != len(predicted):
            raise ValueError(
                "actual and predicted must have the same length"
            )

    @staticmethod
    def _validate_values(
        actual: list[float] | tuple[float, ...],
        predicted: list[float] | tuple[float, ...],
    ) -> None:
        for value in (*actual, *predicted):
            if (
                isinstance(value, bool)
                or not isinstance(value, (int, float))
            ):
                raise TypeError(
                    "actual and predicted values must be numbers"
                )

            if not math.isfinite(value):
                raise ValueError(
                    "actual and predicted values must be finite"
                )
