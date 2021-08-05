import os
import logging
from config import BASE_DIR


def createLogger(name: str, fileName: str, level: int = logging.DEBUG) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(level)

    fileHandler = logging.FileHandler(
        os.path.join(BASE_DIR, fileName), "a", encoding="utf8")
    fileHandler.setFormatter(logging.Formatter(
        '[%(asctime)s] [%(name)s] [%(levelname)s] > %(message)s', '%Y-%m-%d %H:%M:%S'))

    logger.addHandler(fileHandler)

    return logger
