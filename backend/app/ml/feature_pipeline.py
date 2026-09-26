from backend.app.predictions.analysis_record import AnalysisRecord
from backend.app.predictions.feature_snapshot import FeatureSnapshot


class FeaturePipeline:
    @staticmethod
    def build(
        analysis: AnalysisRecord,
    ) -> FeatureSnapshot:
        FeaturePipeline._validate_analysis(analysis)

        return FeatureSnapshot(
            symbol=analysis.symbol,
            feature_timestamp=analysis.reference_timestamp,
            features={
                "technical_score": analysis.technical_score,
                "flow_score": analysis.flow_score,
                "momentum_score": analysis.momentum_score,
                "structure_score": analysis.structure_score,
                "direction_score": analysis.direction_score,
                "volume_score": analysis.volume_score,
                "confidence": analysis.confidence,
                "contradiction": analysis.contradiction,
            },
        )

    @staticmethod
    def build_many(
        analyses: list[AnalysisRecord] | tuple[AnalysisRecord, ...],
    ) -> tuple[FeatureSnapshot, ...]:
        FeaturePipeline._validate_analyses(analyses)

        return tuple(
            FeaturePipeline.build(analysis)
            for analysis in analyses
        )

    @staticmethod
    def _validate_analysis(
        analysis: AnalysisRecord,
    ) -> None:
        if not isinstance(analysis, AnalysisRecord):
            raise TypeError(
                "analysis must be an AnalysisRecord"
            )

    @staticmethod
    def _validate_analyses(
        analyses: list[AnalysisRecord] | tuple[AnalysisRecord, ...],
    ) -> None:
        if not isinstance(analyses, (list, tuple)):
            raise TypeError(
                "analyses must be a list or tuple"
            )

        if not analyses:
            raise ValueError(
                "analyses must not be empty"
            )

        for analysis in analyses:
            FeaturePipeline._validate_analysis(analysis)
