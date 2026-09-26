from dataclasses import dataclass

from backend.app.ml.ml_dataset import MLDataset


@dataclass(frozen=True)
class DatasetSplit:
    train: MLDataset
    validation: MLDataset
    test: MLDataset

    def __post_init__(self) -> None:
        self._validate_train()
        self._validate_validation()
        self._validate_test()

    def _validate_train(self) -> None:
        if not isinstance(self.train, MLDataset):
            raise TypeError(
                "train must be an MLDataset"
            )

    def _validate_validation(self) -> None:
        if not isinstance(self.validation, MLDataset):
            raise TypeError(
                "validation must be an MLDataset"
            )

    def _validate_test(self) -> None:
        if not isinstance(self.test, MLDataset):
            raise TypeError(
                "test must be an MLDataset"
            )
