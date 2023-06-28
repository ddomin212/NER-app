import logging
from logging.handlers import SysLogHandler
import os


def initialize_logging():
    """Initialize papertrail logging."""
    logger = logging.getLogger("ner_app")
    logger.setLevel(logging.DEBUG)
    syslog = SysLogHandler(
        address=(os.getenv("PAPERTRAIL_HOST"), int(os.getenv("PAPERTRAIL_PORT")))
    )
    logger.addHandler(syslog)
    logger.info("Logging initialized.")
    return logger
