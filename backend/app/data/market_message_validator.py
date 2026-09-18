import json


class MarketMessageValidator:
    def validate(self, raw_message: str) -> dict:
        try:
            message = json.loads(raw_message)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON message") from exc

        if not isinstance(message, dict):
            raise ValueError("Market message must be a JSON object")

        required_fields = {"e", "s"}

        if not required_fields.issubset(message):
            raise ValueError("Market message is missing required fields")

        if not all(
            isinstance(message[field], str) and message[field]
            for field in required_fields
        ):
            raise ValueError("Market message has invalid required fields")

        return message