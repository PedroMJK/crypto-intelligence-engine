import re


class MultiTimeframeAnalyzer:
    def analyze(
        self,
        states: list[dict],
        reference_timestamp: int,
    ) -> list[dict]:
        if not isinstance(reference_timestamp, int):
            raise TypeError(
                "reference timestamp must be an integer"
            )

        if reference_timestamp < 0:
            raise ValueError(
                "reference timestamp cannot be negative"
            )

        latest_states = {}

        for state in states:
            if not isinstance(state, dict):
                raise TypeError(
                    "each state must be a dictionary"
                )

            if "timeframe" not in state:
                raise ValueError(
                    "state must contain timeframe"
                )

            if "state" not in state:
                raise ValueError(
                    "state must contain state"
                )

            if "confirmation_timestamp" not in state:
                raise ValueError(
                    "state must contain confirmation_timestamp"
                )

            timeframe = state["timeframe"]
            state_value = state["state"]
            confirmation_timestamp = state[
                "confirmation_timestamp"
            ]

            if not isinstance(timeframe, str):
                raise TypeError(
                    "timeframe must be a string"
                )

            if not timeframe:
                raise ValueError(
                    "timeframe must not be empty"
                )

            if not isinstance(state_value, str):
                raise TypeError(
                    "state must be a string"
                )

            if not state_value:
                raise ValueError(
                    "state must not be empty"
                )

            if not isinstance(
                confirmation_timestamp,
                int,
            ):
                raise TypeError(
                    "confirmation timestamp must be an integer"
                )

            if confirmation_timestamp < 0:
                raise ValueError(
                    "confirmation timestamp cannot be negative"
                )

            if confirmation_timestamp > reference_timestamp:
                continue

            previous_state = latest_states.get(timeframe)

            if (
                previous_state is None
                or confirmation_timestamp
                > previous_state[
                    "confirmation_timestamp"
                ]
            ):
                latest_states[timeframe] = state

        return sorted(
            latest_states.values(),
            key=self._timeframe_sort_key,
        )

    @staticmethod
    def _timeframe_sort_key(state: dict) -> int:
        timeframe = state["timeframe"]

        match = re.fullmatch(
            r"(\d+)([mhd])",
            timeframe,
        )

        if match is None:
            return float("inf")

        value = int(match.group(1))
        unit = match.group(2)

        multiplier = {
            "m": 1,
            "h": 60,
            "d": 1440,
        }[unit]

        return value * multiplier
