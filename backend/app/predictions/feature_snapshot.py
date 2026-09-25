import math
from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class FeatureSnapshot:
    symbol: str
    feature_timestamp: int
    features: Mapping[str, float]

    def __post_init__(self) -> None:
        self._validate_symbol()
        self._validate_feature_timestamp()
        self._validate_features()

        immutable_features = MappingProxyType(
            dict(self.features)
        )

        object.__setattr__(
            self,
            "features",
            immutable_features,
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

    def _validate_feature_timestamp(self) -> None:
        if (
            not isinstance(self.feature_timestamp, int)
            or isinstance(self.feature_timestamp, bool)
        ):
            raise TypeError(
                "feature timestamp must be an integer"
            )

        if self.feature_timestamp < 0:
            raise ValueError(
                "feature timestamp cannot be negative"
            )

    def _validate_features(self) -> None:
        if not isinstance(self.features, Mapping):
            raise TypeError(
                "features must be a mapping"
            )

        if not self.features:
            raise ValueError(
                "features must not be empty"
            )

        for feature_name, feature_value in self.features.items():
            self._validate_feature_name(feature_name)
            self._validate_feature_value(
                feature_name,
                feature_value,
            )

    @staticmethod
    def _validate_feature_name(feature_name: str) -> None:
        if not isinstance(feature_name, str):
            raise TypeError(
                "feature name must be a string"
            )

        if not feature_name:
            raise ValueError(
                "feature name must not be empty"
            )

    @staticmethod
    def _validate_feature_value(
        feature_name: str,
        feature_value: float,
    ) -> None:
        if (
            not isinstance(feature_value, (int, float))
            or isinstance(feature_value, bool)
        ):
            raise TypeError(
                f"{feature_name} must be a number"
            )

        if not math.isfinite(feature_value):
            raise ValueError(
                f"{feature_name} must be finite"
            )
