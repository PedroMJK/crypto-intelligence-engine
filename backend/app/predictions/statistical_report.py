import math
from dataclasses import dataclass


@dataclass(frozen=True)
class StatisticalReport:
    horizon_minutes: int
    sample_count: int
    mean_direction_score: float
    mean_future_return: float
    mean_absolute_return: float
    mean_directional_alignment: float

    def __post_init__(self) -> None:
        self._validate_horizon_minutes()
        self._validate_sample_count()
        self._validate_mean_direction_score()
        self._validate_mean(
            "mean future return",
            self.mean_future_return,
        )
        self._validate_mean_absolute_return()
        self._validate_mean(
            "mean directional alignment",
            self.mean_directional_alignment,
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

    def _validate_sample_count(self) -> None:
        if (
            not isinstance(self.sample_count, int)
            or isinstance(self.sample_count, bool)
        ):
            raise TypeError(
                "sample count must be an integer"
            )

        if self.sample_count <= 0:
            raise ValueError(
                "sample count must be greater than zero"
            )

    def _validate_mean_direction_score(self) -> None:
        self._validate_mean(
            "mean direction score",
            self.mean_direction_score,
        )

        if not -1.0 <= self.mean_direction_score <= 1.0:
            raise ValueError(
                "mean direction score must be between -1.0 and 1.0"
            )

    @staticmethod
    def _validate_mean(
        mean_name: str,
        mean_value: float,
    ) -> None:
        if (
            not isinstance(mean_value, (int, float))
            or isinstance(mean_value, bool)
        ):
            raise TypeError(
                f"{mean_name} must be a number"
            )

        if not math.isfinite(mean_value):
            raise ValueError(
                f"{mean_name} must be finite"
            )

    def _validate_mean_absolute_return(self) -> None:
        self._validate_mean(
            "mean absolute return",
            self.mean_absolute_return,
        )

        if self.mean_absolute_return < 0:
            raise ValueError(
                "mean absolute return cannot be negative"
            )
