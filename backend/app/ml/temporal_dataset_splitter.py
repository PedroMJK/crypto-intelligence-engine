import math

from backend.app.ml.dataset_split import DatasetSplit
from backend.app.ml.ml_dataset import MLDataset


class TemporalDatasetSplitter:
    @staticmethod
    def split(
        dataset: MLDataset,
        train_ratio: float,
        validation_ratio: float,
        test_ratio: float,
    ) -> DatasetSplit:
        TemporalDatasetSplitter._validate_dataset(
            dataset
        )
        TemporalDatasetSplitter._validate_ratios(
            train_ratio,
            validation_ratio,
            test_ratio,
        )
        TemporalDatasetSplitter._validate_temporal_order(
            dataset
        )

        sample_count = len(dataset.samples)

        train_size = int(
            sample_count * train_ratio
        )
        validation_size = int(
            sample_count * validation_ratio
        )

        validation_end = (
            train_size + validation_size
        )

        train_samples = dataset.samples[
            :train_size
        ]
        validation_samples = dataset.samples[
            train_size:validation_end
        ]
        test_samples = dataset.samples[
            validation_end:
        ]

        TemporalDatasetSplitter._validate_partition_sizes(
            train_samples,
            validation_samples,
            test_samples,
        )
        TemporalDatasetSplitter._validate_split_boundaries(
            train_samples,
            validation_samples,
            test_samples,
        )
        TemporalDatasetSplitter._validate_target_boundaries(
            train_samples,
            validation_samples,
            test_samples,
        )

        return DatasetSplit(
            train=MLDataset(
                samples=train_samples,
            ),
            validation=MLDataset(
                samples=validation_samples,
            ),
            test=MLDataset(
                samples=test_samples,
            ),
        )

    @staticmethod
    def _validate_dataset(
        dataset: MLDataset,
    ) -> None:
        if not isinstance(dataset, MLDataset):
            raise TypeError(
                "dataset must be an MLDataset"
            )

    @staticmethod
    def _validate_ratios(
        train_ratio: float,
        validation_ratio: float,
        test_ratio: float,
    ) -> None:
        ratios = (
            train_ratio,
            validation_ratio,
            test_ratio,
        )

        for ratio in ratios:
            TemporalDatasetSplitter._validate_ratio(
                ratio
            )

        if not math.isclose(
            sum(ratios),
            1.0,
            rel_tol=0.0,
            abs_tol=1e-9,
        ):
            raise ValueError(
                "ratios must sum to one"
            )

    @staticmethod
    def _validate_ratio(
        ratio: float,
    ) -> None:
        if (
            isinstance(ratio, bool)
            or not isinstance(ratio, (int, float))
        ):
            raise TypeError(
                "ratio must be a number"
            )

        if not math.isfinite(ratio):
            raise ValueError(
                "ratio must be finite"
            )

        if ratio <= 0:
            raise ValueError(
                "ratio must be greater than zero"
            )

    @staticmethod
    def _validate_temporal_order(
        dataset: MLDataset,
    ) -> None:
        timestamps = tuple(
            sample.features.feature_timestamp
            for sample in dataset.samples
        )

        for previous, current in zip(
            timestamps,
            timestamps[1:],
        ):
            if current < previous:
                raise ValueError(
                    "dataset samples must be in chronological order"
                )

    @staticmethod
    def _validate_partition_sizes(
        train_samples: tuple,
        validation_samples: tuple,
        test_samples: tuple,
    ) -> None:
        if (
            not train_samples
            or not validation_samples
            or not test_samples
        ):
            raise ValueError(
                "split partitions must not be empty"
            )

    @staticmethod
    def _validate_split_boundaries(
        train_samples: tuple,
        validation_samples: tuple,
        test_samples: tuple,
    ) -> None:
        train_last_timestamp = (
            train_samples[-1].features.feature_timestamp
        )
        validation_first_timestamp = (
            validation_samples[0].features.feature_timestamp
        )
        validation_last_timestamp = (
            validation_samples[-1].features.feature_timestamp
        )
        test_first_timestamp = (
            test_samples[0].features.feature_timestamp
        )

        if (
            train_last_timestamp
            >= validation_first_timestamp
            or validation_last_timestamp
            >= test_first_timestamp
        ):
            raise ValueError(
                "split boundaries must be strictly chronological"
            )

    @staticmethod
    def _validate_target_boundaries(
        train_samples: tuple,
        validation_samples: tuple,
        test_samples: tuple,
    ) -> None:
        latest_train_target_timestamp = max(
            sample.target_timestamp
            for sample in train_samples
        )
        validation_first_feature_timestamp = (
            validation_samples[0].features.feature_timestamp
        )

        if (
            latest_train_target_timestamp
            >= validation_first_feature_timestamp
        ):
            raise ValueError(
                "training targets must be observed before validation starts"
            )

        latest_validation_target_timestamp = max(
            sample.target_timestamp
            for sample in validation_samples
        )
        test_first_feature_timestamp = (
            test_samples[0].features.feature_timestamp
        )

        if (
            latest_validation_target_timestamp
            >= test_first_feature_timestamp
        ):
            raise ValueError(
                "validation targets must be observed before test starts"
            )
