import logging
import os
from logging import Logger


def init_logger() -> Logger:
    logger = logging.getLogger(os.getenv("SERVICE_NAME"))
    logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    logger.addHandler(log_handler)
    return logger
