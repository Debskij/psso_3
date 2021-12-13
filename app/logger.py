import logging
import sys

LOG_LEVEL = logging.DEBUG
"""Message logging level"""


def create_logger(name: str) -> logging.Logger:
    """
    Create logger for given name
    :param name: name of logger
    :return: logger
    """

    log_format = '%(asctime)s - %(name)s - %(levelname)s: %(message)s'
    formatter = logging.Formatter(log_format)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(LOG_LEVEL)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(f'./data/events.log')
    file_handler.setLevel(LOG_LEVEL)
    file_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVEL)
    if not len(logger.handlers):
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger
