import pytest

from backend.app.data.market_message_validator import MarketMessageValidator


def test_validate_returns_parsed_market_message():
    validator = MarketMessageValidator()

    message = validator.validate(
        '{"e":"aggTrade","s":"BTCUSDT"}'
    )

    assert message == {
        "e": "aggTrade",
        "s": "BTCUSDT",
    }


def test_validate_rejects_invalid_json():
    validator = MarketMessageValidator()

    with pytest.raises(ValueError, match="Invalid JSON message"):
        validator.validate('{"e":"aggTrade","s":"BTCUSDT"')


def test_validate_rejects_non_object_json():
    validator = MarketMessageValidator()

    with pytest.raises(ValueError, match="Market message must be a JSON object"):
        validator.validate('["BTCUSDT","ETHUSDT"]')


@pytest.mark.parametrize(
    "raw_message",
    [
        '{"s":"BTCUSDT"}',
        '{"e":"aggTrade"}',
    ],
)
def test_validate_rejects_missing_required_fields(raw_message):
    validator = MarketMessageValidator()

    with pytest.raises(
        ValueError,
        match="Market message is missing required fields",
    ):
        validator.validate(raw_message)


@pytest.mark.parametrize(
    "raw_message",
    [
        '{"e":"","s":"BTCUSDT"}',
        '{"e":"aggTrade","s":""}',
        '{"e":123,"s":"BTCUSDT"}',
        '{"e":"aggTrade","s":123}',
    ],
)
def test_validate_rejects_invalid_required_field_values(raw_message):
    validator = MarketMessageValidator()

    with pytest.raises(
        ValueError,
        match="Market message has invalid required fields",
    ):
        validator.validate(raw_message)
