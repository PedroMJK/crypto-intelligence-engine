from dataclasses import dataclass
import math

from backend.app.backtesting.directional_classification import (
    DirectionalClassification,
)


@dataclass(frozen=True)
class ModelEvaluation:
    model_name: str
    sample_count: int
    accuracy: float | None
    precision: float | None
    recall: float | None
    confusion_matrix: DirectionalClassification

    def __post_init__(self) -> None:
        self._validate_model_name()
        self._validate_sample_count()
        self._validate_metric(
            "accuracy",
            self.accuracy,
        )
        self._validate_metric(
            "precision",
            self.precision,
        )
        self._validate_metric(
            "recall",
            self.recall,
        )
        self._validate_confusion_matrix()

    def _validate_model_name(self) -> None:
        if not isinstance(self.model_name, str):
            raise TypeError(
                "model_name must be a str"
            )

        if not self.model_name.strip():
            raise ValueError(
                "model_name must not be blank"
            )

    def _validate_sample_count(self) -> None:
        if (
            isinstance(self.sample_count, bool)
            or not isinstance(self.sample_count, int)
        ):
            raise TypeError(
                "sample_count must be an int"
            )

        if self.sample_count <= 0:
            raise ValueError(
                "sample_count must be greater than zero"
            )

    @staticmethod
    def _validate_metric(
        name: str,
        value: float | None,
    ) -> None:
        if value is None:
            return

        if isinstance(value, bool) or not isinstance(value, float):
            raise TypeError(
                f"{name} must be a float or None"
            )

        if not math.isfinite(value):
            raise ValueError(
                f"{name} must be finite"
            )

        if not 0.0 <= value <= 1.0:
            raise ValueError(
                f"{name} must be between 0 and 1"
            )

    def _validate_confusion_matrix(self) -> None:
        if not isinstance(
            self.confusion_matrix,
            DirectionalClassification,
        ):
            raise TypeError(
                "confusion_matrix must be a DirectionalClassification"
            )
