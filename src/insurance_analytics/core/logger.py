"""
Application logger setup.
"""

import logging
import os
from core.config import LOG_DIR


def get_logger(name="app"):
    """
    Create or retrieve a logging instance.

    Args:
        name (str): Logger name.

    Returns:
        logging.Logger | None: Logger instance or None on failure.
    """
    try:
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        log_path = os.path.join(LOG_DIR, "app.log")
        handler = logging.FileHandler(log_path)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)

        if not logger.handlers:
            logger.addHandler(handler)

        return logger
    except Exception as e:
        print(f"[LOGGER] Logger setup failed: {e}")
        return None
