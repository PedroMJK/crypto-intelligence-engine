import math
from dataclasses import dataclass

from backend.app.predictions.feature_snapshot import FeatureSnapshot


@dataclass(frozen=True)
class MLSample:
    features: FeatureSnapshot
    horizon_minutes: int
    target: float
    target_timestamp: int

    def __post_init__(self) -> None:
        self._validate_features()
        self._validate_horizon_minutes()
        self._validate_target()
        self._validate_target_timestamp()

    def _validate_features(self) -> None:
        if not isinstance(self.features, FeatureSnapshot):
            raise TypeError(
                "features must be a FeatureSnapshot"
            )

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

    def _validate_target(self) -> None:
        if (
            isinstance(self.target, bool)
            or not isinstance(self.target, (int, float))
        ):
            raise TypeError(
                "target must be a number"
            )

        if not math.isfinite(self.target):
            raise ValueError(
                "target must be finite"
            )

    def _validate_target_timestamp(self) -> None:
        if (
            isinstance(self.target_timestamp, bool)
            or not isinstance(self.target_timestamp, int)
        ):
            raise TypeError(
                "target_timestamp must be an int"
            )

        minimum_target_timestamp = (
            self.features.feature_timestamp
            + self.horizon_minutes * 60_000
        )

        if self.target_timestamp < minimum_target_timestamp:
            raise ValueError(
                "target_timestamp must be at or after the horizon end"
            )
