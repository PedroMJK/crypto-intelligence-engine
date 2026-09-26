import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CalibrationSample:
    horizon_minutes: int
    predicted_return: float
    observed_return: float

    def __post_init__(self) -> None:
        self._validate_horizon_minutes()
        self._validate_predicted_return()
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

    def _validate_predicted_return(self) -> None:
        if (
            isinstance(self.predicted_return, bool)
            or not isinstance(
                self.predicted_return,
                (int, float),
            )
        ):
            raise TypeError(
                "predicted_return must be a number"
            )

        if not math.isfinite(
            self.predicted_return
        ):
            raise ValueError(
                "predicted_return must be finite"
            )

    def _validate_observed_return(self) -> None:
        if (
            isinstance(self.observed_return, bool)
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
