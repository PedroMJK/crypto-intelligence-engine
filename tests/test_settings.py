from backend.app.config.settings import settings


def test_application_name():
    assert settings.app_name == "Crypto Intelligence Engine"


def test_binance_urls_are_configured():
    assert settings.binance_rest_url.startswith("https://")
    assert settings.binance_ws_url.startswith("wss://")


def test_mongodb_configuration_exists():
    assert settings.mongodb_uri
    assert settings.mongodb_database