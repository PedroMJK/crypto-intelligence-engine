from backend.app.analysis.structural_trend_detector import (
    StructuralTrendDetector,
)


class StructureChangeDetector:
    def __init__(self) -> None:
        self.trend_detector = StructuralTrendDetector()

    def detect(
        self,
        structural_points: list[dict],
        break_events: list[dict],
    ) -> list[dict]:
        previous_break_index = None
        change_events = []

        for break_event in break_events:
            break_index = break_event["index"]
            break_direction = break_event["direction"]

            if break_direction not in {"bullish", "bearish"}:
                raise ValueError(
                    "break direction must be bullish or bearish"
                )

            if (
                previous_break_index is not None
                and break_index <= previous_break_index
            ):
                raise ValueError(
                    "break events must be in chronological order"
                )

            confirmed_points = [
                point
                for point in structural_points
                if (
                    point.get("confirmation_index") is not None
                    and point["confirmation_index"] <= break_index
                )
            ]

            previous_trend = self.trend_detector.detect(
                confirmed_points
            )

            is_bullish_to_bearish = (
                previous_trend == "bullish"
                and break_direction == "bearish"
            )
            is_bearish_to_bullish = (
                previous_trend == "bearish"
                and break_direction == "bullish"
            )

            if (
                is_bullish_to_bearish
                or is_bearish_to_bullish
            ):
                change_events.append(
                    {
                        "index": break_index,
                        "previous_trend": previous_trend,
                        "new_direction": break_direction,
                        "break_direction": break_direction,
                        "level": break_event["level"],
                        "structural_point_index": break_event[
                            "structural_point_index"
                        ],
                    }
                )

            previous_break_index = break_index

        return change_events
