import math

import pytest

from backend.app.ml.ml_sample import MLSample
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_feature_snapshot(
    *,
    symbol="FETUSDT",
    feature_timestamp=1_800_000_000_000,
    features=None,
):
    if features is None:
        features = {
            "technical_score": 0.60,
            "flow_score": -0.20,
            "momentum_score": 0.40,
            "structure_score": 0.10,
            "direction_score": 0.35,
            "volume_score": 0.80,
            "confidence": 0.70,
            "contradiction": 0.15,
        }

    return FeatureSnapshot(
        symbol=symbol,
        feature_timestamp=feature_timestamp,
        features=features,
    )


def test_ml_sample_preserves_features():
    features = create_feature_snapshot()

    sample = MLSample(
        features=features,
        horizon_minutes=15,
        target=0.025,
        target_timestamp=1_800_000_900_000,
    )

    assert sample.features is features


def test_ml_sample_preserves_horizon_minutes():
    sample = MLSample(
        features=create_feature_snapshot(),
        horizon_minutes=30,
        target=-0.01,
        target_timestamp=1_800_001_800_000,
    )

    assert sample.horizon_minutes == 30


def test_ml_sample_preserves_continuous_target():
    sample = MLSample(
        features=create_feature_snapshot(),
        horizon_minutes=15,
        target=-0.0275,
        target_timestamp=1_800_000_900_000,
    )

    assert sample.target == -0.0275


def test_ml_sample_preserves_target_timestamp():
    sample = MLSample(
        features=create_feature_snapshot(),
        horizon_minutes=15,
        target=0.025,
        target_timestamp=1_800_000_900_000,
    )

    assert sample.target_timestamp == 1_800_000_900_000


@pytest.mark.parametrize(
    "target_timestamp",
    [
        None,
        1.5,
        True,
        "1800000900000",
        [],
        {},
    ],
)
def test_ml_sample_rejects_non_integer_target_timestamp(
    target_timestamp,
):
    with pytest.raises(TypeError):
        MLSample(
            features=create_feature_snapshot(),
            horizon_minutes=15,
            target=0.025,
            target_timestamp=target_timestamp,
        )


def test_ml_sample_rejects_target_timestamp_before_horizon_end():
    with pytest.raises(ValueError):
        MLSample(
            features=create_feature_snapshot(
                feature_timestamp=1_800_000_000_000,
            ),
            horizon_minutes=15,
            target=0.025,
            target_timestamp=1_800_000_899_999,
        )


def test_ml_sample_accepts_target_timestamp_at_horizon_end():
    sample = MLSample(
        features=create_feature_snapshot(
            feature_timestamp=1_800_000_000_000,
        ),
        horizon_minutes=15,
        target=0.025,
        target_timestamp=1_800_000_900_000,
    )

    assert sample.target_timestamp == 1_800_000_900_000


def test_ml_sample_accepts_target_timestamp_after_horizon_end():
    sample = MLSample(
        features=create_feature_snapshot(
            feature_timestamp=1_800_000_000_000,
        ),
        horizon_minutes=15,
        target=0.025,
        target_timestamp=1_800_001_200_000,
    )

    assert sample.target_timestamp == 1_800_001_200_000


@pytest.mark.parametrize(
    "target",
    [
        -1.0,
        -0.000001,
        0.0,
        0.000001,
        1.0,
        2.5,
    ],
)
def test_ml_sample_accepts_finite_continuous_target(
    target,
):
    sample = MLSample(
        features=create_feature_snapshot(),
        horizon_minutes=15,
        target=target,
        target_timestamp=1_800_000_900_000,
    )

    assert sample.target == target


@pytest.mark.parametrize(
    "features",
    [
        None,
        123,
        True,
        "features",
        {},
        [],
        (),
    ],
)
def test_ml_sample_rejects_invalid_features(
    features,
):
    with pytest.raises(TypeError):
        MLSample(
            features=features,
            horizon_minutes=15,
            target=0.01,
            target_timestamp=1_800_000_900_000,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        None,
        1.5,
        True,
        "15",
        [],
        {},
    ],
)
def test_ml_sample_rejects_non_integer_horizon(
    horizon_minutes,
):
    with pytest.raises(TypeError):
        MLSample(
            features=create_feature_snapshot(),
            horizon_minutes=horizon_minutes,
            target=0.01,
            target_timestamp=1_800_000_900_000,
        )


@pytest.mark.parametrize(
    "horizon_minutes",
    [
        -15,
        -1,
        0,
    ],
)
def test_ml_sample_rejects_non_positive_horizon(
    horizon_minutes,
):
    with pytest.raises(ValueError):
        MLSample(
            features=create_feature_snapshot(),
            horizon_minutes=horizon_minutes,
            target=0.01,
            target_timestamp=1_800_000_900_000,
        )


@pytest.mark.parametrize(
    "target",
    [
        None,
        True,
        "0.01",
        [],
        {},
    ],
)
def test_ml_sample_rejects_non_numeric_target(
    target,
):
    with pytest.raises(TypeError):
        MLSample(
            features=create_feature_snapshot(),
            horizon_minutes=15,
            target=target,
            target_timestamp=1_800_000_900_000,
        )


@pytest.mark.parametrize(
    "target",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_ml_sample_rejects_non_finite_target(
    target,
):
    with pytest.raises(ValueError):
        MLSample(
            features=create_feature_snapshot(),
            horizon_minutes=15,
            target=target,
            target_timestamp=1_800_000_900_000,
        )
