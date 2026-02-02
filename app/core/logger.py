import logging
import os
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from app.core.config import Config


def setup_logger():
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_filename = os.path.join(log_dir, f"{datetime.now().strftime('%Y%m%d')}.log")

    logger = logging.getLogger(Config.APP_NAME)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        handler = TimedRotatingFileHandler(
            log_filename, when="midnight", interval=1, backupCount=30, encoding="utf-8"
        )
        handler.setFormatter(formatter)

        def namer(default_name):
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


logger = setup_logger()
