import logging

from backend.app.core.logging_config import configure_logging


configure_logging()

logger = logging.getLogger(__name__)

logger.info("Crypto Intelligence Engine started")