import pytest

from backend.app.predictions.analysis_record import AnalysisRecord
from backend.app.ml.feature_pipeline import FeaturePipeline
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_analysis_record(
    *,
    symbol="FETUSDT",
    reference_timestamp=1_800_000_000_000,
    reference_price=0.42,
    technical_score=0.60,
    flow_score=-0.20,
    momentum_score=0.40,
    structure_score=0.10,
    direction_score=0.35,
    volume_score=0.80,
    confidence=0.70,
    contradiction=0.15,
):
    return AnalysisRecord(
        symbol=symbol,
        reference_timestamp=reference_timestamp,
        reference_price=reference_price,
        technical_score=technical_score,
        flow_score=flow_score,
        momentum_score=momentum_score,
        structure_score=structure_score,
        direction_score=direction_score,
        volume_score=volume_score,
        confidence=confidence,
        contradiction=contradiction,
    )


def test_feature_pipeline_returns_feature_snapshot():
    analysis = create_analysis_record()

    result = FeaturePipeline.build(analysis)

    assert isinstance(result, FeatureSnapshot)


def test_feature_pipeline_preserves_symbol():
    analysis = create_analysis_record(
        symbol="BTCUSDT",
    )

    result = FeaturePipeline.build(analysis)

    assert result.symbol == "BTCUSDT"


def test_feature_pipeline_uses_reference_timestamp():
    analysis = create_analysis_record(
        reference_timestamp=1_800_000_300_000,
    )

    result = FeaturePipeline.build(analysis)

    assert result.feature_timestamp == 1_800_000_300_000


def test_feature_pipeline_builds_expected_features():
    analysis = create_analysis_record(
        technical_score=0.60,
        flow_score=-0.20,
        momentum_score=0.40,
        structure_score=0.10,
        direction_score=0.35,
        volume_score=0.80,
        confidence=0.70,
        contradiction=0.15,
    )

    result = FeaturePipeline.build(analysis)

    assert dict(result.features) == {
        "technical_score": 0.60,
        "flow_score": -0.20,
        "momentum_score": 0.40,
        "structure_score": 0.10,
        "direction_score": 0.35,
        "volume_score": 0.80,
        "confidence": 0.70,
        "contradiction": 0.15,
    }


def test_feature_pipeline_does_not_include_reference_price_as_feature():
    analysis = create_analysis_record(
        reference_price=123.45,
    )

    result = FeaturePipeline.build(analysis)

    assert "reference_price" not in result.features


def test_feature_pipeline_preserves_zero_values():
    analysis = create_analysis_record(
        technical_score=0.0,
        flow_score=0.0,
        momentum_score=0.0,
        structure_score=0.0,
        direction_score=0.0,
        volume_score=0.0,
        confidence=0.0,
        contradiction=0.0,
    )

    result = FeaturePipeline.build(analysis)

    assert dict(result.features) == {
        "technical_score": 0.0,
        "flow_score": 0.0,
        "momentum_score": 0.0,
        "structure_score": 0.0,
        "direction_score": 0.0,
        "volume_score": 0.0,
        "confidence": 0.0,
        "contradiction": 0.0,
    }


def test_feature_pipeline_preserves_directional_boundaries():
    analysis = create_analysis_record(
        technical_score=-1.0,
        flow_score=1.0,
        momentum_score=-1.0,
        structure_score=1.0,
        direction_score=-1.0,
    )

    result = FeaturePipeline.build(analysis)

    assert result.features["technical_score"] == -1.0
    assert result.features["flow_score"] == 1.0
    assert result.features["momentum_score"] == -1.0
    assert result.features["structure_score"] == 1.0
    assert result.features["direction_score"] == -1.0


def test_feature_pipeline_preserves_unit_interval_boundaries():
    analysis = create_analysis_record(
        volume_score=1.0,
        confidence=0.0,
        contradiction=1.0,
    )

    result = FeaturePipeline.build(analysis)

    assert result.features["volume_score"] == 1.0
    assert result.features["confidence"] == 0.0
    assert result.features["contradiction"] == 1.0


@pytest.mark.parametrize(
    "analysis",
    [
        None,
        123,
        True,
        "analysis",
        {},
        [],
        (),
    ],
)
def test_feature_pipeline_rejects_invalid_analysis_record(
    analysis,
):
    with pytest.raises(TypeError):
        FeaturePipeline.build(analysis)


def test_feature_pipeline_builds_multiple_snapshots():
    analyses = [
        create_analysis_record(
            symbol="FETUSDT",
            reference_timestamp=1_800_000_000_000,
        ),
        create_analysis_record(
            symbol="BTCUSDT",
            reference_timestamp=1_800_000_300_000,
        ),
    ]

    result = FeaturePipeline.build_many(analyses)

    assert isinstance(result, tuple)
    assert len(result) == 2
    assert all(
        isinstance(snapshot, FeatureSnapshot)
        for snapshot in result
    )


def test_feature_pipeline_preserves_analysis_order():
    analyses = [
        create_analysis_record(
            symbol="BTCUSDT",
            reference_timestamp=1_800_000_000_000,
        ),
        create_analysis_record(
            symbol="FETUSDT",
            reference_timestamp=1_800_000_300_000,
        ),
        create_analysis_record(
            symbol="ETHUSDT",
            reference_timestamp=1_800_000_600_000,
        ),
    ]

    result = FeaturePipeline.build_many(analyses)

    assert tuple(
        snapshot.symbol
        for snapshot in result
    ) == (
        "BTCUSDT",
        "FETUSDT",
        "ETHUSDT",
    )


def test_feature_pipeline_build_many_accepts_tuple():
    analyses = (
        create_analysis_record(),
        create_analysis_record(
            reference_timestamp=1_800_000_300_000,
        ),
    )

    result = FeaturePipeline.build_many(analyses)

    assert len(result) == 2


@pytest.mark.parametrize(
    "analyses",
    [
        None,
        123,
        True,
        "analyses",
        {},
        set(),
    ],
)
def test_feature_pipeline_build_many_rejects_invalid_collection(
    analyses,
):
    with pytest.raises(TypeError):
        FeaturePipeline.build_many(analyses)


def test_feature_pipeline_build_many_rejects_empty_list():
    with pytest.raises(ValueError):
        FeaturePipeline.build_many([])


def test_feature_pipeline_build_many_rejects_empty_tuple():
    with pytest.raises(ValueError):
        FeaturePipeline.build_many(())
