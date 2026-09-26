from unittest.mock import Mock

import pytest

from backend.app.ml.ml_dataset import MLDataset
from backend.app.ml.ml_sample import MLSample
from backend.app.ml.model_comparison_dataset_builder import (
    ModelComparisonDatasetBuilder,
)
from backend.app.predictions.analysis_record import AnalysisRecord
from backend.app.predictions.feature_snapshot import FeatureSnapshot


def create_analysis(
    *,
    symbol: str = "BTCUSDT",
    reference_timestamp: int = 1_000_000,
    direction_score: float = 0.60,
) -> AnalysisRecord:
    return AnalysisRecord(
        symbol=symbol,
        reference_timestamp=reference_timestamp,
        reference_price=100.0,
        technical_score=0.50,
        flow_score=0.40,
        momentum_score=0.30,
        structure_score=0.20,
        direction_score=direction_score,
        volume_score=0.70,
        confidence=0.80,
        contradiction=0.10,
    )


def create_sample(
    *,
    symbol: str = "BTCUSDT",
    feature_timestamp: int = 1_000_000,
    horizon_minutes: int = 15,
    target: float = 0.02,
) -> MLSample:
    features = FeatureSnapshot(
        symbol=symbol,
        feature_timestamp=feature_timestamp,
        features={
            "technical_score": 0.50,
            "flow_score": 0.40,
            "momentum_score": 0.30,
            "structure_score": 0.20,
            "direction_score": 0.60,
            "volume_score": 0.70,
            "confidence": 0.80,
            "contradiction": 0.10,
        },
    )

    return MLSample(
        features=features,
        horizon_minutes=horizon_minutes,
        target=target,
        target_timestamp=(
            feature_timestamp
            + horizon_minutes * 60_000
        ),
    )


def create_model(
    *,
    predicted_return: float = 0.015,
):
    model = Mock()
    model.predict.return_value = predicted_return

    return model


def test_build_creates_comparison_dataset():
    analysis = create_analysis()
    sample = create_sample()
    model = create_model(
        predicted_return=0.015
    )

    result = ModelComparisonDatasetBuilder.build(
        model=model,
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    assert len(result.samples) == 1

    comparison = result.samples[0]

    assert comparison.horizon_minutes == 15
    assert (
        comparison.traditional_direction_score
        == 0.60
    )
    assert comparison.ml_predicted_return == 0.015
    assert comparison.observed_return == 0.02


def test_build_uses_analysis_direction_score():
    analysis = create_analysis(
        direction_score=-0.75
    )
    sample = create_sample()

    result = ModelComparisonDatasetBuilder.build(
        model=create_model(),
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    assert (
        result.samples[0].traditional_direction_score
        == -0.75
    )


def test_build_uses_ml_sample_target_as_observed_return():
    analysis = create_analysis()
    sample = create_sample(
        target=-0.035
    )

    result = ModelComparisonDatasetBuilder.build(
        model=create_model(),
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    assert result.samples[0].observed_return == -0.035


def test_build_uses_sample_horizon():
    analysis = create_analysis()
    sample = create_sample(
        horizon_minutes=30
    )

    result = ModelComparisonDatasetBuilder.build(
        model=create_model(),
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    assert result.samples[0].horizon_minutes == 30


def test_build_calls_model_with_features_and_horizon():
    analysis = create_analysis()
    sample = create_sample(
        horizon_minutes=30
    )
    model = create_model()

    ModelComparisonDatasetBuilder.build(
        model=model,
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    model.predict.assert_called_once_with(
        features=sample.features,
        horizon_minutes=30,
    )


def test_build_does_not_fit_model():
    analysis = create_analysis()
    sample = create_sample()
    model = create_model()

    ModelComparisonDatasetBuilder.build(
        model=model,
        pairs=[
            (
                analysis,
                sample,
            ),
        ],
    )

    model.fit.assert_not_called()


def test_build_preserves_order():
    first_analysis = create_analysis(
        symbol="BTCUSDT",
        reference_timestamp=1_000_000,
        direction_score=0.60,
    )
    first_sample = create_sample(
        symbol="BTCUSDT",
        feature_timestamp=1_000_000,
        horizon_minutes=5,
    )

    second_analysis = create_analysis(
        symbol="ETHUSDT",
        reference_timestamp=2_000_000,
        direction_score=-0.40,
    )
    second_sample = create_sample(
        symbol="ETHUSDT",
        feature_timestamp=2_000_000,
        horizon_minutes=30,
    )

    model = Mock()
    model.predict.side_effect = [
        0.01,
        -0.02,
    ]

    result = ModelComparisonDatasetBuilder.build(
        model=model,
        pairs=[
            (
                first_analysis,
                first_sample,
            ),
            (
                second_analysis,
                second_sample,
            ),
        ],
    )

    assert tuple(
        sample.horizon_minutes
        for sample in result.samples
    ) == (
        5,
        30,
    )

    assert tuple(
        sample.ml_predicted_return
        for sample in result.samples
    ) == (
        0.01,
        -0.02,
    )


def test_build_preserves_duplicates():
    analysis = create_analysis()
    sample = create_sample()
    model = Mock()
    model.predict.side_effect = [
        0.01,
        0.01,
    ]

    result = ModelComparisonDatasetBuilder.build(
        model=model,
        pairs=[
            (
                analysis,
                sample,
            ),
            (
                analysis,
                sample,
            ),
        ],
    )

    assert len(result.samples) == 2
    assert result.samples[0] == result.samples[1]


def test_build_accepts_tuple_of_pairs():
    analysis = create_analysis()
    sample = create_sample()

    result = ModelComparisonDatasetBuilder.build(
        model=create_model(),
        pairs=(
            (
                analysis,
                sample,
            ),
        ),
    )

    assert len(result.samples) == 1


def test_build_rejects_symbol_mismatch():
    analysis = create_analysis(
        symbol="BTCUSDT"
    )
    sample = create_sample(
        symbol="ETHUSDT"
    )

    with pytest.raises(
        ValueError,
        match=(
            "analysis and sample symbols must match"
        ),
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=[
                (
                    analysis,
                    sample,
                ),
            ],
        )


def test_build_rejects_timestamp_mismatch():
    analysis = create_analysis(
        reference_timestamp=1_000_000
    )
    sample = create_sample(
        feature_timestamp=2_000_000
    )

    with pytest.raises(
        ValueError,
        match=(
            "analysis reference timestamp must match "
            "sample feature timestamp"
        ),
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=[
                (
                    analysis,
                    sample,
                ),
            ],
        )


@pytest.mark.parametrize(
    "model",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_build_rejects_model_without_predict(
    model,
):
    with pytest.raises(
        TypeError,
        match=(
            "model must provide a callable predict method"
        ),
    ):
        ModelComparisonDatasetBuilder.build(
            model=model,
            pairs=[
                (
                    create_analysis(),
                    create_sample(),
                ),
            ],
        )


@pytest.mark.parametrize(
    "pairs",
    [
        None,
        "invalid",
        123,
        True,
        {},
    ],
)
def test_build_rejects_invalid_pairs_collection(
    pairs,
):
    with pytest.raises(
        TypeError,
        match="pairs must be a list or tuple",
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=pairs,
        )


@pytest.mark.parametrize(
    "pairs",
    [
        [],
        (),
    ],
)
def test_build_rejects_empty_pairs(
    pairs,
):
    with pytest.raises(
        ValueError,
        match="pairs must not be empty",
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=pairs,
        )


@pytest.mark.parametrize(
    "pair",
    [
        None,
        "invalid",
        123,
        True,
        (),
        (1,),
        (1, 2, 3),
        [1, 2],
    ],
)
def test_build_rejects_invalid_pair_structure(
    pair,
):
    with pytest.raises(
        TypeError,
        match=(
            "each pair must be a tuple with two items"
        ),
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=[
                pair,
            ],
        )


@pytest.mark.parametrize(
    "analysis",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_build_rejects_invalid_analysis(
    analysis,
):
    with pytest.raises(
        TypeError,
        match=(
            "analysis must be an AnalysisRecord"
        ),
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=[
                (
                    analysis,
                    create_sample(),
                ),
            ],
        )


@pytest.mark.parametrize(
    "sample",
    [
        None,
        "invalid",
        123,
        True,
    ],
)
def test_build_rejects_invalid_sample(
    sample,
):
    with pytest.raises(
        TypeError,
        match="sample must be an MLSample",
    ):
        ModelComparisonDatasetBuilder.build(
            model=create_model(),
            pairs=[
                (
                    create_analysis(),
                    sample,
                ),
            ],
        )


@pytest.mark.parametrize(
    "prediction",
    [
        None,
        "invalid",
        True,
    ],
)
def test_build_rejects_invalid_model_prediction_type(
    prediction,
):
    model = create_model(
        predicted_return=prediction
    )

    with pytest.raises(
        TypeError,
        match="model prediction must be a number",
    ):
        ModelComparisonDatasetBuilder.build(
            model=model,
            pairs=[
                (
                    create_analysis(),
                    create_sample(),
                ),
            ],
        )


@pytest.mark.parametrize(
    "prediction",
    [
        float("nan"),
        float("inf"),
        float("-inf"),
    ],
)
def test_build_rejects_non_finite_model_prediction(
    prediction,
):
    model = create_model(
        predicted_return=prediction
    )

    with pytest.raises(
        ValueError,
        match="model prediction must be finite",
    ):
        ModelComparisonDatasetBuilder.build(
            model=model,
            pairs=[
                (
                    create_analysis(),
                    create_sample(),
                ),
            ],
        )
