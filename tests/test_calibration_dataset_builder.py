from unittest.mock import Mock

import pytest

from backend.app.ml.calibration_dataset import CalibrationDataset
from backend.app.ml.calibration_dataset_builder import (
    CalibrationDatasetBuilder,
)
from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_feature_snapshot(
    *,
    symbol: str = "BTCUSDT",
    feature_timestamp: int = 1_000_000,
    direction_score: float = 0.25,
) -> FeatureSnapshot:
    return FeatureSnapshot(
        symbol=symbol,
        feature_timestamp=feature_timestamp,
        features={
            "direction_score": direction_score,
            "volume_score": 0.60,
        },
    )


def create_sample(
    *,
    symbol: str = "BTCUSDT",
    feature_timestamp: int = 1_000_000,
    horizon_minutes: int = 15,
    target: float = 0.01,
    direction_score: float = 0.25,
) -> MLSample:
    return MLSample(
        features=create_feature_snapshot(
            symbol=symbol,
            feature_timestamp=feature_timestamp,
            direction_score=direction_score,
        ),
        horizon_minutes=horizon_minutes,
        target=target,
        target_timestamp=(
            feature_timestamp
            + horizon_minutes * 60_000
        ),
    )


def create_model(
    predictions: list[float],
) -> Mock:
    model = Mock()
    model.predict.side_effect = predictions

    return model


def test_build_creates_calibration_dataset():
    dataset = MLDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
                target=0.012,
            ),
            create_sample(
                feature_timestamp=2_000_000,
                horizon_minutes=15,
                target=-0.008,
            ),
        ]
    )
    model = create_model(
        [
            0.010,
            -0.006,
        ]
    )

    result = CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    assert isinstance(
        result,
        CalibrationDataset,
    )
    assert len(result.samples) == 2

    assert result.samples[0].horizon_minutes == 5
    assert result.samples[0].predicted_return == 0.010
    assert result.samples[0].observed_return == 0.012

    assert result.samples[1].horizon_minutes == 15
    assert result.samples[1].predicted_return == -0.006
    assert result.samples[1].observed_return == -0.008


def test_build_uses_sample_features_and_horizon_for_prediction():
    first = create_sample(
        horizon_minutes=5,
        direction_score=0.20,
    )
    second = create_sample(
        feature_timestamp=2_000_000,
        horizon_minutes=30,
        direction_score=-0.30,
    )

    dataset = MLDataset(
        samples=[
            first,
            second,
        ]
    )
    model = create_model(
        [
            0.01,
            -0.02,
        ]
    )

    CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    assert model.predict.call_count == 2

    model.predict.assert_any_call(
        features=first.features,
        horizon_minutes=5,
    )
    model.predict.assert_any_call(
        features=second.features,
        horizon_minutes=30,
    )


def test_build_preserves_dataset_order():
    dataset = MLDataset(
        samples=[
            create_sample(
                horizon_minutes=5,
                target=0.01,
            ),
            create_sample(
                feature_timestamp=2_000_000,
                horizon_minutes=15,
                target=0.02,
            ),
            create_sample(
                feature_timestamp=3_000_000,
                horizon_minutes=30,
                target=-0.03,
            ),
        ]
    )
    model = create_model(
        [
            0.001,
            0.002,
            -0.003,
        ]
    )

    result = CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    assert tuple(
        sample.horizon_minutes
        for sample in result.samples
    ) == (
        5,
        15,
        30,
    )

    assert tuple(
        sample.observed_return
        for sample in result.samples
    ) == (
        0.01,
        0.02,
        -0.03,
    )


def test_build_preserves_duplicate_samples():
    sample = create_sample(
        target=0.01,
    )

    dataset = MLDataset(
        samples=[
            sample,
            sample,
        ]
    )
    model = create_model(
        [
            0.005,
            0.005,
        ]
    )

    result = CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    assert len(result.samples) == 2
    assert result.samples[0] == result.samples[1]


def test_build_does_not_fit_model():
    dataset = MLDataset(
        samples=[
            create_sample(),
        ]
    )
    model = create_model(
        [
            0.01,
        ]
    )

    CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    model.fit.assert_not_called()


def test_build_uses_observed_target_without_transforming_it():
    dataset = MLDataset(
        samples=[
            create_sample(
                target=0.0,
            ),
            create_sample(
                feature_timestamp=2_000_000,
                target=-0.25,
            ),
            create_sample(
                feature_timestamp=3_000_000,
                target=0.40,
            ),
        ]
    )
    model = create_model(
        [
            0.01,
            -0.02,
            0.03,
        ]
    )

    result = CalibrationDatasetBuilder.build(
        model=model,
        dataset=dataset,
    )

    assert tuple(
        sample.observed_return
        for sample in result.samples
    ) == (
        0.0,
        -0.25,
        0.40,
    )


@pytest.mark.parametrize(
    "dataset",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_build_rejects_invalid_dataset(
    dataset,
):
    model = create_model(
        [
            0.01,
        ]
    )

    with pytest.raises(
        TypeError,
        match="dataset must be an MLDataset",
    ):
        CalibrationDatasetBuilder.build(
            model=model,
            dataset=dataset,
        )


@pytest.mark.parametrize(
    "model",
    [
        None,
        "invalid",
        123,
        True,
        object(),
    ],
)
def test_build_rejects_model_without_callable_predict(
    model,
):
    dataset = MLDataset(
        samples=[
            create_sample(),
        ]
    )

    with pytest.raises(
        TypeError,
        match="model must provide a callable predict method",
    ):
        CalibrationDatasetBuilder.build(
            model=model,
            dataset=dataset,
        )


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        "0.01",
        True,
    ],
)
def test_build_rejects_invalid_prediction_type(
    prediction,
):
    dataset = MLDataset(
        samples=[
            create_sample(),
        ]
    )
    model = create_model(
        [
            prediction,
        ]
    )

    with pytest.raises(
        TypeError,
        match="model prediction must be a number",
    ):
        CalibrationDatasetBuilder.build(
            model=model,
            dataset=dataset,
        )


@pytest.mark.parametrize(
    "prediction",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_build_rejects_non_finite_prediction(
    prediction,
):
    dataset = MLDataset(
        samples=[
            create_sample(),
        ]
    )
    model = create_model(
        [
            prediction,
        ]
    )

    with pytest.raises(
        ValueError,
        match="model prediction must be finite",
    ):
        CalibrationDatasetBuilder.build(
            model=model,
            dataset=dataset,
        )
