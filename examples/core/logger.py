"""
Logging configuration module.

This module sets up a logger that outputs to both the console and rotating log files.
Log files are stored in the 'logs' directory and are rotated daily.
"""

import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler


def setup_logger(app_name: str = "pyflow-ai-stack"):
    """
    Configure and return the application logger.

    Sets up:
    1. A TimedRotatingFileHandler for daily log rotation.
    2. A StreamHandler for console output.
    3. Custom naming for rotated log files.

    Args:
        app_name (str): The name of the application for the logger.

    Returns:
        logging.Logger: The configured application logger.
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(app_name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        def namer(default_name):
            """Custom naming function for rotated log files."""
            base_dir = os.path.dirname(default_name)
            parts = default_name.split(".")
            rotate_date_str = parts[-1]
            try:
                date_obj = datetime.strptime(rotate_date_str, "%Y-%m-%d")
                new_name = date_obj.strftime("%Y%m%d") + ".log"
            except ValueError:
                new_name = default_name
            return os.path.join(base_dir, new_name)

        handler.namer = namer
        logger.addHandler(handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


# Initialize and export the logger instance
logger = setup_logger()
