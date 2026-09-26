import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ModelComparisonSample:
    horizon_minutes: int
    traditional_direction_score: float
    ml_predicted_return: float
    observed_return: float

    def __post_init__(self) -> None:
        self._validate_horizon_minutes()
        self._validate_traditional_direction_score()
        self._validate_ml_predicted_return()
        self._validate_observed_return()

    def _validate_horizon_minutes(self) -> None:
        if (
            isinstance(self.horizon_minutes, bool)
            or not isinstance(self.horizon_minutes, int)
        ):
            raise TypeError(
                "horizon_minutes must be an int"
            )

        if self.horizon_minutes <= 0:
            raise ValueError(
                "horizon_minutes must be greater than zero"
            )

    def _validate_traditional_direction_score(
        self,
    ) -> None:
        if (
            isinstance(
                self.traditional_direction_score,
                bool,
            )
            or not isinstance(
                self.traditional_direction_score,
                (int, float),
            )
        ):
            raise TypeError(
                "traditional_direction_score must be a number"
            )

        if not math.isfinite(
            self.traditional_direction_score
        ):
            raise ValueError(
                "traditional_direction_score must be finite"
            )

        if not (
            -1.0
            <= self.traditional_direction_score
            <= 1.0
        ):
            raise ValueError(
                "traditional_direction_score must be between "
                "-1 and 1"
            )

    def _validate_ml_predicted_return(
        self,
    ) -> None:
        if (
            isinstance(
                self.ml_predicted_return,
                bool,
            )
            or not isinstance(
                self.ml_predicted_return,
                (int, float),
            )
        ):
            raise TypeError(
                "ml_predicted_return must be a number"
            )

        if not math.isfinite(
            self.ml_predicted_return
        ):
            raise ValueError(
                "ml_predicted_return must be finite"
            )

    def _validate_observed_return(
        self,
    ) -> None:
        if (
            isinstance(
                self.observed_return,
                bool,
            )
            or not isinstance(
                self.observed_return,
                (int, float),
            )
        ):
            raise TypeError(
                "observed_return must be a number"
            )

        if not math.isfinite(
            self.observed_return
        ):
            raise ValueError(
                "observed_return must be finite"
            )
