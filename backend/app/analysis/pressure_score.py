class PressureScore:
    def calculate(
        self,
        flow_signal: float,
        momentum_signal: float,
        volume_signal: float,
    ) -> float:
        signals = {
            "flow_signal": flow_signal,
            "momentum_signal": momentum_signal,
            "volume_signal": volume_signal,
        }

        for signal_name, signal_value in signals.items():
            if not -1.0 <= signal_value <= 1.0:
                raise ValueError(
                    f"{signal_name} must be between -1.0 and 1.0"
                )

        return sum(signals.values()) / len(signals)
