import logging
import os

LOGGER_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOGGER_PATH = os.getenv("LOG_PATH", "tts.log")


class MyLogFormatter(logging.Formatter):
    """Custome log formatter

    Args:
        logging (logging): formatter of logging
    """

    complet_fmt = "[%(asctime)s] [%(levelname)s] [%(module)s/%(filename)s :\
%(lineno)s %(funcName)s()] - %(message)s"

    simple_fmt = "[%(asctime)s] [%(levelname)s] - %(message)s"

    FORMATS = {
        logging.DEBUG: complet_fmt,
        logging.INFO: simple_fmt,
        logging.WARNING: simple_fmt,
        logging.ERROR: complet_fmt,
        logging.CRITICAL: complet_fmt,
    }

    def __init__(self):
        super().__init__(
            fmt="[%(asctime)s] [%(levelname)s] - %(message)s",
            datefmt="%m/%d/%Y %I:%M:%S %p",
        )

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


def get_logger(logger_name=__name__, level=LOGGER_LEVEL):
    """Initial logger
    It redirects stdout to both file and console.

    Args:
        logger_name (string, optional): name of logger. Defaults to __name__.
        level (string, optional): log level. Defaults to LOGGER_LEVEL(=INFO).

    Returns:
        logger: logger configured
    """
    # create a custom logger and set level
    logger = logging.getLogger(logger_name)
    logger.setLevel(level)

    # logger existance check (avoid to add other handlers to the same logger)
    if not logger.handlers:
        # create handlers
        file_handler = logging.FileHandler(LOGGER_PATH)
        console_handeler = logging.StreamHandler()
        # create formatters and add it to handlers
        file_handler.setFormatter(MyLogFormatter())
        console_handeler.setFormatter(MyLogFormatter())
        # add handler to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handeler)

    return logger
