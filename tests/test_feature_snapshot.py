import math
from dataclasses import FrozenInstanceError

import pytest

from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_feature_snapshot(**overrides):
    values = {
        "symbol": "FETUSDT",
        "feature_timestamp": 1_800_000_000_000,
        "features": {
            "rsi": 63.4,
            "volume_delta": 15_230.5,
            "price_velocity": 0.00042,
            "buy_sell_ratio": 1.37,
        },
    }
    values.update(overrides)

    return FeatureSnapshot(**values)


def test_feature_snapshot_preserves_feature_state():
    snapshot = create_feature_snapshot()

    assert snapshot.symbol == "FETUSDT"
    assert snapshot.feature_timestamp == 1_800_000_000_000
    assert snapshot.features == {
        "rsi": 63.4,
        "volume_delta": 15_230.5,
        "price_velocity": 0.00042,
        "buy_sell_ratio": 1.37,
    }


def test_feature_snapshot_is_immutable():
    snapshot = create_feature_snapshot()

    with pytest.raises(FrozenInstanceError):
        snapshot.symbol = "BTCUSDT"


def test_feature_snapshot_features_are_immutable():
    snapshot = create_feature_snapshot()

    with pytest.raises(TypeError):
        snapshot.features["rsi"] = 70.0


def test_feature_snapshot_copies_input_features():
    features = {
        "rsi": 63.4,
    }

    snapshot = create_feature_snapshot(
        features=features,
    )

    features["rsi"] = 99.0

    assert snapshot.features["rsi"] == 63.4


@pytest.mark.parametrize(
    "symbol",
    [
        "",
        123,
        None,
    ],
)
def test_feature_snapshot_rejects_invalid_symbol(symbol):
    expected_exception = (
        ValueError
        if isinstance(symbol, str)
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_feature_snapshot(symbol=symbol)


@pytest.mark.parametrize(
    "feature_timestamp",
    [
        -1,
        1.5,
        True,
        None,
    ],
)
def test_feature_snapshot_rejects_invalid_feature_timestamp(
    feature_timestamp,
):
    expected_exception = (
        ValueError
        if (
            isinstance(feature_timestamp, int)
            and not isinstance(feature_timestamp, bool)
        )
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_feature_snapshot(
            feature_timestamp=feature_timestamp,
        )


@pytest.mark.parametrize(
    "features",
    [
        None,
        [],
        "rsi",
        123,
    ],
)
def test_feature_snapshot_rejects_non_mapping_features(features):
    with pytest.raises(TypeError):
        create_feature_snapshot(
            features=features,
        )


def test_feature_snapshot_rejects_empty_features():
    with pytest.raises(ValueError):
        create_feature_snapshot(
            features={},
        )


@pytest.mark.parametrize(
    "feature_name",
    [
        "",
        123,
        None,
    ],
)
def test_feature_snapshot_rejects_invalid_feature_name(
    feature_name,
):
    expected_exception = (
        ValueError
        if isinstance(feature_name, str)
        else TypeError
    )

    with pytest.raises(expected_exception):
        create_feature_snapshot(
            features={
                feature_name: 1.0,
            },
        )


@pytest.mark.parametrize(
    "feature_value",
    [
        "63.4",
        True,
        None,
    ],
)
def test_feature_snapshot_rejects_non_numeric_feature_value(
    feature_value,
):
    with pytest.raises(TypeError):
        create_feature_snapshot(
            features={
                "rsi": feature_value,
            },
        )


@pytest.mark.parametrize(
    "feature_value",
    [
        math.nan,
        math.inf,
        -math.inf,
    ],
)
def test_feature_snapshot_rejects_non_finite_feature_value(
    feature_value,
):
    with pytest.raises(ValueError):
        create_feature_snapshot(
            features={
                "rsi": feature_value,
            },
        )


@pytest.mark.parametrize(
    "feature_value",
    [
        -10.0,
        -1.0,
        0.0,
        1.0,
        10.0,
    ],
)
def test_feature_snapshot_accepts_finite_feature_values(
    feature_value,
):
    snapshot = create_feature_snapshot(
        features={
            "generic_feature": feature_value,
        },
    )

    assert snapshot.features["generic_feature"] == feature_value
