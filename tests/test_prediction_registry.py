import pytest

from backend.app.predictions.prediction_record import PredictionRecord
from backend.app.predictions.prediction_registry import PredictionRegistry


def create_prediction_record(**overrides):
    values = {
        "symbol": "FETUSDT",
        "prediction_timestamp": 1_800_000_000_000,
        "reference_price": 0.5821,
        "direction_score": 0.65,
    }
    values.update(overrides)

    return PredictionRecord(**values)


def test_prediction_registry_starts_empty():
    registry = PredictionRegistry()

    assert registry.records == ()


def test_prediction_registry_registers_prediction_record():
    registry = PredictionRegistry()
    record = create_prediction_record()

    registry.register(record)

    assert registry.records == (record,)


def test_prediction_registry_preserves_registration_order():
    registry = PredictionRegistry()

    first_record = create_prediction_record(
        symbol="FETUSDT",
        prediction_timestamp=1_800_000_000_000,
    )
    second_record = create_prediction_record(
        symbol="BTCUSDT",
        prediction_timestamp=1_800_000_000_100,
    )
    third_record = create_prediction_record(
        symbol="ETHUSDT",
        prediction_timestamp=1_800_000_000_200,
    )

    registry.register(first_record)
    registry.register(second_record)
    registry.register(third_record)

    assert registry.records == (
        first_record,
        second_record,
        third_record,
    )


def test_prediction_registry_preserves_insertion_order_not_timestamp_order():
    registry = PredictionRegistry()

    first_record = create_prediction_record(
        symbol="FETUSDT",
        prediction_timestamp=300,
    )
    second_record = create_prediction_record(
        symbol="BTCUSDT",
        prediction_timestamp=100,
    )
    third_record = create_prediction_record(
        symbol="ETHUSDT",
        prediction_timestamp=200,
    )

    registry.register(first_record)
    registry.register(second_record)
    registry.register(third_record)

    assert registry.records == (
        first_record,
        second_record,
        third_record,
    )


def test_prediction_registry_returns_immutable_records_collection():
    registry = PredictionRegistry()
    record = create_prediction_record()

    registry.register(record)

    records = registry.records

    assert isinstance(records, tuple)

    with pytest.raises(AttributeError):
        records.append(record)


def test_prediction_registry_allows_repeated_records():
    registry = PredictionRegistry()
    record = create_prediction_record()

    registry.register(record)
    registry.register(record)

    assert registry.records == (
        record,
        record,
    )


@pytest.mark.parametrize(
    "invalid_record",
    [
        None,
        {},
        "FETUSDT",
        123,
        True,
    ],
)
def test_prediction_registry_rejects_non_prediction_records(
    invalid_record,
):
    registry = PredictionRegistry()

    with pytest.raises(TypeError):
        registry.register(invalid_record)

    assert registry.records == ()
