class MarketRegimeAnalyzer:
    VALID_TREND_STATES = {
        "bullish",
        "bearish",
        "indeterminate",
    }

    VALID_VOLATILITY_STATES = {
        "expanding",
        "stable",
        "contracting",
    }

    def analyze(
        self,
        trend_state: str,
        volatility_state: str,
    ) -> dict:
        if not isinstance(trend_state, str):
            raise TypeError(
                "trend state must be a string"
            )

        if not isinstance(volatility_state, str):
            raise TypeError(
                "volatility state must be a string"
            )

        if not trend_state:
            raise ValueError(
                "trend state must not be empty"
            )

        if not volatility_state:
            raise ValueError(
                "volatility state must not be empty"
            )

        if trend_state not in self.VALID_TREND_STATES:
            raise ValueError(
                "invalid trend state"
            )

        if (
            volatility_state
            not in self.VALID_VOLATILITY_STATES
        ):
            raise ValueError(
                "invalid volatility state"
            )

        return {
            "trend": trend_state,
            "volatility": volatility_state,
        }
