from backend.app.predictions.feature_snapshot import FeatureSnapshot


class FeatureRegistry:
    def __init__(self) -> None:
        self._snapshots: list[FeatureSnapshot] = []

    @property
    def snapshots(self) -> tuple[FeatureSnapshot, ...]:
        return tuple(self._snapshots)

    def register(self, snapshot: FeatureSnapshot) -> None:
        if not isinstance(snapshot, FeatureSnapshot):
            raise TypeError(
                "snapshot must be a FeatureSnapshot"
            )

        self._snapshots.append(snapshot)
