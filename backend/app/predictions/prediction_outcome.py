import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionOutcome:
    symbol: str
    prediction_timestamp: int
    reference_price: float
    horizon_minutes: int
    evaluation_timestamp: int
    evaluation_price: float

    def __post_init__(self) -> None:
        self._validate_symbol()
        self._validate_prediction_timestamp()
        self._validate_reference_price()
        self._validate_horizon_minutes()
        self._validate_evaluation_timestamp()
        self._validate_evaluation_price()
        self._validate_evaluation_horizon()

    @property
    def future_return(self) -> float:
        return (
            self.evaluation_price
            / self.reference_price
            - 1.0
        )

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

    def _validate_reference_price(self) -> None:
        if (
            not isinstance(self.reference_price, (int, float))
            or isinstance(self.reference_price, bool)
        ):
            raise TypeError(
                "reference price must be a number"
            )

        if not math.isfinite(self.reference_price):
            raise ValueError(
                "reference price must be finite"
            )

        if self.reference_price <= 0:
            raise ValueError(
                "reference price must be greater than zero"
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

    def _validate_evaluation_timestamp(self) -> None:
        if (
            not isinstance(self.evaluation_timestamp, int)
            or isinstance(self.evaluation_timestamp, bool)
        ):
            raise TypeError(
                "evaluation timestamp must be an integer"
            )

        if self.evaluation_timestamp < 0:
            raise ValueError(
                "evaluation timestamp cannot be negative"
            )

    def _validate_evaluation_price(self) -> None:
        if (
            not isinstance(self.evaluation_price, (int, float))
            or isinstance(self.evaluation_price, bool)
        ):
            raise TypeError(
                "evaluation price must be a number"
            )

        if not math.isfinite(self.evaluation_price):
            raise ValueError(
                "evaluation price must be finite"
            )

        if self.evaluation_price <= 0:
            raise ValueError(
                "evaluation price must be greater than zero"
            )

    def _validate_evaluation_horizon(self) -> None:
        minimum_evaluation_timestamp = (
            self.prediction_timestamp
            + self.horizon_minutes * 60_000
        )

        if (
            self.evaluation_timestamp
            < minimum_evaluation_timestamp
        ):
            raise ValueError(
                "evaluation timestamp cannot be before "
                "the prediction horizon"
            )
