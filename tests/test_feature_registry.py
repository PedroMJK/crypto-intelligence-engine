import pytest

from backend.app.predictions.feature_registry import FeatureRegistry
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


def test_feature_registry_starts_empty():
    registry = FeatureRegistry()

    assert registry.snapshots == ()


def test_feature_registry_registers_feature_snapshot():
    registry = FeatureRegistry()
    snapshot = create_feature_snapshot()

    registry.register(snapshot)

    assert registry.snapshots == (snapshot,)


def test_feature_registry_preserves_registration_order():
    registry = FeatureRegistry()

    first_snapshot = create_feature_snapshot(
        symbol="FETUSDT",
        feature_timestamp=1_800_000_000_000,
    )
    second_snapshot = create_feature_snapshot(
        symbol="BTCUSDT",
        feature_timestamp=1_800_000_000_100,
    )
    third_snapshot = create_feature_snapshot(
        symbol="ETHUSDT",
        feature_timestamp=1_800_000_000_200,
    )

    registry.register(first_snapshot)
    registry.register(second_snapshot)
    registry.register(third_snapshot)

    assert registry.snapshots == (
        first_snapshot,
        second_snapshot,
        third_snapshot,
    )


def test_feature_registry_preserves_insertion_order_not_timestamp_order():
    registry = FeatureRegistry()

    first_snapshot = create_feature_snapshot(
        symbol="FETUSDT",
        feature_timestamp=300,
    )
    second_snapshot = create_feature_snapshot(
        symbol="BTCUSDT",
        feature_timestamp=100,
    )
    third_snapshot = create_feature_snapshot(
        symbol="ETHUSDT",
        feature_timestamp=200,
    )

    registry.register(first_snapshot)
    registry.register(second_snapshot)
    registry.register(third_snapshot)

    assert registry.snapshots == (
        first_snapshot,
        second_snapshot,
        third_snapshot,
    )


def test_feature_registry_returns_immutable_snapshots_collection():
    registry = FeatureRegistry()
    snapshot = create_feature_snapshot()

    registry.register(snapshot)

    snapshots = registry.snapshots

    assert isinstance(snapshots, tuple)

    with pytest.raises(AttributeError):
        snapshots.append(snapshot)


def test_feature_registry_allows_repeated_snapshots():
    registry = FeatureRegistry()
    snapshot = create_feature_snapshot()

    registry.register(snapshot)
    registry.register(snapshot)

    assert registry.snapshots == (
        snapshot,
        snapshot,
    )


@pytest.mark.parametrize(
    "invalid_snapshot",
    [
        None,
        {},
        "FETUSDT",
        123,
        True,
    ],
)
def test_feature_registry_rejects_non_feature_snapshots(
    invalid_snapshot,
):
    registry = FeatureRegistry()

    with pytest.raises(TypeError):
        registry.register(invalid_snapshot)

    assert registry.snapshots == ()
