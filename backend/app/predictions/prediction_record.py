import math
from dataclasses import dataclass


@dataclass(frozen=True)
class PredictionRecord:
    symbol: str
    prediction_timestamp: int
    reference_price: float
    direction_score: float

    def __post_init__(self) -> None:
        self._validate_symbol()
        self._validate_prediction_timestamp()
        self._validate_reference_price()
        self._validate_direction_score()

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
