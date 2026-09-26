import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionMetrics:
    symbol: str
    prediction_timestamp: int
    horizon_minutes: int
    direction_score: float
    future_return: float
    directional_alignment: float
    absolute_return: float

    def __post_init__(self) -> None:
        self._validate_symbol()
        self._validate_prediction_timestamp()
        self._validate_horizon_minutes()
        self._validate_direction_score()
        self._validate_metric(
            "future return",
            self.future_return,
        )
        self._validate_metric(
            "directional alignment",
            self.directional_alignment,
        )
        self._validate_absolute_return()

    def _validate_symbol(self) -> None:
        if not isinstance(self.symbol, str):
            raise TypeError(
                "symbol must be a string"
            )

        if not self.symbol:
            raise ValueError(
                "symbol must not be empty"
            )

    def _validate_prediction_timestamp(self) -> None:
        if (
            not isinstance(self.prediction_timestamp, int)
            or isinstance(self.prediction_timestamp, bool)
        ):
            raise TypeError(
                "prediction timestamp must be an integer"
            )

        if self.prediction_timestamp < 0:
            raise ValueError(
                "prediction timestamp cannot be negative"
            )

    def _validate_horizon_minutes(self) -> None:
        if (
            not isinstance(self.horizon_minutes, int)
            or isinstance(self.horizon_minutes, bool)
        ):
            raise TypeError(
                "horizon minutes must be an integer"
            )

        if self.horizon_minutes <= 0:
            raise ValueError(
                "horizon minutes must be greater than zero"
            )

    def _validate_direction_score(self) -> None:
        if (
            not isinstance(self.direction_score, (int, float))
            or isinstance(self.direction_score, bool)
        ):
            raise TypeError(
                "direction score must be a number"
            )

        if not math.isfinite(self.direction_score):
            raise ValueError(
                "direction score must be finite"
            )

        if not -1.0 <= self.direction_score <= 1.0:
            raise ValueError(
                "direction score must be between -1.0 and 1.0"
            )

    @staticmethod
    def _validate_metric(
        metric_name: str,
        metric_value: float,
    ) -> None:
        if (
            not isinstance(metric_value, (int, float))
            or isinstance(metric_value, bool)
        ):
            raise TypeError(
                f"{metric_name} must be a number"
            )

        if not math.isfinite(metric_value):
            raise ValueError(
                f"{metric_name} must be finite"
            )

    def _validate_absolute_return(self) -> None:
        self._validate_metric(
            "absolute return",
            self.absolute_return,
        )

        if self.absolute_return < 0:
            raise ValueError(
                "absolute return cannot be negative"
            )
