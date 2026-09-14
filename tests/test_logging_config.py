import logging

from backend.app.core.logging_config import configure_logging


def test_configure_logging_sets_info_level():
    configure_logging()

    root_logger = logging.getLogger()

    assert root_logger.level == logging.INFO