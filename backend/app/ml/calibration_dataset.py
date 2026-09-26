from dataclasses import dataclass

from backend.app.ml.calibration_sample import CalibrationSample


@dataclass(frozen=True)
class CalibrationDataset:
    samples: tuple[CalibrationSample, ...]

    def __post_init__(self) -> None:
        self._validate_collection()
        self._validate_samples()
        self._freeze_samples()

    def _validate_collection(self) -> None:
        if not isinstance(
            self.samples,
            (list, tuple),
        ):
            raise TypeError(
                "samples must be a list or tuple"
            )

        if not self.samples:
            raise ValueError(
                "samples must not be empty"
            )

    def _validate_samples(self) -> None:
        for sample in self.samples:
            if not isinstance(
                sample,
                CalibrationSample,
            ):
                raise TypeError(
                    "all samples must be CalibrationSample"
                )

    def _freeze_samples(self) -> None:
        object.__setattr__(
            self,
            "samples",
            tuple(self.samples),
        )
