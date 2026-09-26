from dataclasses import dataclass


@dataclass(frozen=True)
class DirectionalClassification:
    true_positive: int
    false_positive: int
    true_negative: int
    false_negative: int

    def __post_init__(self) -> None:
        self._validate_count(
            "true_positive",
            self.true_positive,
        )
        self._validate_count(
            "false_positive",
            self.false_positive,
        )
        self._validate_count(
            "true_negative",
            self.true_negative,
        )
        self._validate_count(
            "false_negative",
            self.false_negative,
        )

    @staticmethod
    def _validate_count(
        name: str,
        value: int,
    ) -> None:
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(
                f"{name} must be an int"
            )

        if value < 0:
            raise ValueError(
                f"{name} must be greater than or equal to zero"
            )
