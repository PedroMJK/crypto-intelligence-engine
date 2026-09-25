import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisRecord:
    symbol: str
    reference_timestamp: int
    reference_price: float
    technical_score: float
    flow_score: float
    momentum_score: float
    structure_score: float
    direction_score: float
    volume_score: float
    confidence: float
    contradiction: float

    def __post_init__(self) -> None:
        self._validate_symbol()
        self._validate_reference_timestamp()
        self._validate_reference_price()
        self._validate_scores()

    def _validate_symbol(self) -> None:
        if not isinstance(self.symbol, str):
            raise TypeError(
                "symbol must be a string"
            )

        if not self.symbol:
            raise ValueError(
                "symbol must not be empty"
            )

    def _validate_reference_timestamp(self) -> None:
        if (
            not isinstance(self.reference_timestamp, int)
            or isinstance(self.reference_timestamp, bool)
        ):
            raise TypeError(
                "reference timestamp must be an integer"
            )

        if self.reference_timestamp < 0:
            raise ValueError(
                "reference timestamp cannot be negative"
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

    def _validate_scores(self) -> None:
        directional_scores = {
            "technical_score": self.technical_score,
            "flow_score": self.flow_score,
            "momentum_score": self.momentum_score,
            "structure_score": self.structure_score,
            "direction_score": self.direction_score,
        }

        non_directional_scores = {
            "volume_score": self.volume_score,
            "confidence": self.confidence,
            "contradiction": self.contradiction,
        }

        all_scores = {
            **directional_scores,
            **non_directional_scores,
        }

        for score_name, score_value in all_scores.items():
            if (
                not isinstance(score_value, (int, float))
                or isinstance(score_value, bool)
            ):
                raise TypeError(
                    f"{score_name} must be a number"
                )

            if not math.isfinite(score_value):
                raise ValueError(
                    f"{score_name} must be finite"
                )

        for score_name, score_value in directional_scores.items():
            if not -1.0 <= score_value <= 1.0:
                raise ValueError(
                    f"{score_name} must be between -1.0 and 1.0"
                )

        for score_name, score_value in non_directional_scores.items():
            if not 0.0 <= score_value <= 1.0:
                raise ValueError(
                    f"{score_name} must be between 0.0 and 1.0"
                )
