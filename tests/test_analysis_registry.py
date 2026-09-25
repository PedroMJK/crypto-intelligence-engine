import pytest

from backend.app.predictions.analysis_record import AnalysisRecord
from backend.app.predictions.analysis_registry import AnalysisRegistry


def create_analysis_record(**overrides):
    values = {
        "symbol": "FETUSDT",
        "reference_timestamp": 1_800_000_000_000,
        "reference_price": 0.5821,
        "technical_score": 0.6,
        "flow_score": 0.7,
        "momentum_score": 0.5,
        "structure_score": 0.8,
        "direction_score": 0.65,
        "volume_score": 0.75,
        "confidence": 0.7,
        "contradiction": 0.1,
    }
    values.update(overrides)

    return AnalysisRecord(**values)


def test_analysis_registry_starts_empty():
    registry = AnalysisRegistry()

    assert registry.records == ()


def test_analysis_registry_registers_analysis_record():
    registry = AnalysisRegistry()
    record = create_analysis_record()

    registry.register(record)

    assert registry.records == (record,)


def test_analysis_registry_preserves_registration_order():
    registry = AnalysisRegistry()

    first_record = create_analysis_record(
        symbol="FETUSDT",
        reference_timestamp=1_800_000_000_000,
    )
    second_record = create_analysis_record(
        symbol="BTCUSDT",
        reference_timestamp=1_800_000_000_100,
    )
    third_record = create_analysis_record(
        symbol="ETHUSDT",
        reference_timestamp=1_800_000_000_200,
    )

    registry.register(first_record)
    registry.register(second_record)
    registry.register(third_record)

    assert registry.records == (
        first_record,
        second_record,
        third_record,
    )


def test_analysis_registry_preserves_insertion_order_not_timestamp_order():
    registry = AnalysisRegistry()

    first_record = create_analysis_record(
        symbol="FETUSDT",
        reference_timestamp=300,
    )
    second_record = create_analysis_record(
        symbol="BTCUSDT",
        reference_timestamp=100,
    )
    third_record = create_analysis_record(
        symbol="ETHUSDT",
        reference_timestamp=200,
    )

    registry.register(first_record)
    registry.register(second_record)
    registry.register(third_record)

    assert registry.records == (
        first_record,
        second_record,
        third_record,
    )


def test_analysis_registry_returns_immutable_records_collection():
    registry = AnalysisRegistry()
    record = create_analysis_record()

    registry.register(record)

    records = registry.records

    assert isinstance(records, tuple)

    with pytest.raises(AttributeError):
        records.append(record)


def test_analysis_registry_allows_repeated_records():
    registry = AnalysisRegistry()
    record = create_analysis_record()

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
def test_analysis_registry_rejects_non_analysis_records(
    invalid_record,
):
    registry = AnalysisRegistry()

    with pytest.raises(TypeError):
        registry.register(invalid_record)

    assert registry.records == ()
