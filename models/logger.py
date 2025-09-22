import logging
from logging.handlers import RotatingFileHandler
from config import Config
import os
from models.exceptions import FileHandlingError

def get_logger(name=__name__):
    log_file = Config.LOG_FILE
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger = logging.getLogger(name)
    if not logger.handlers:  # avoid adding multiple handlers
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

def write_log(message, level="info"):
    """Write a log entry with given level"""
    logger = get_logger("app")
    try:
        if level == "info":
            logger.info(message)
        elif level == "warning":
            logger.warning(message)
        elif level == "error":
            logger.error(message)
        else:
            logger.debug(message)
    except Exception as e:
        raise FileHandlingError(f"Cannot write to log file: {e}")
