"""Top-level package for Simple Logging."""
import inspect
import logging
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING
from logging.handlers import RotatingFileHandler

import colorlog

DEFAULT_CONSOLE_FORMAT = (
    "%(log_color)s%(asctime)s [%(levelname)-8s] "
    "%(filename)20s(%(lineno)3s):%(funcName)-20s ::"
    " %(message)s%(reset)s"
)

DEFAULT_FILE_FORMAT = (
    "%(asctime)s [%(levelname)-8s] "
    "%(filename)20s(%(lineno)3s):%(funcName)-20s ::"
    " %(message)s"
)


def get_logger(
    name=None,
    logger_level=DEBUG,
    console=True,
    console_format=DEFAULT_CONSOLE_FORMAT,
    console_level=INFO,
    file_name=None,
    file_format=DEFAULT_FILE_FORMAT,
    file_level=DEBUG,
):
    if name:
        caller_name = name
    else:
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        caller_name = caller_module.__name__
    if caller_name != "__main__":
        logger = logging.getLogger(caller_name)
    else:
        logger = colorlog.getLogger()
        configure_main_logger(
            logger,
            logger_level,
            console,
            console_format,
            console_level,
            file_name,
            file_format,
            file_level,
        )
    return logger


def configure_main_logger(
    logger,
    logger_level=DEBUG,
    console=True,
    console_format=DEFAULT_CONSOLE_FORMAT,
    console_level=INFO,
    file_name=None,
    file_format=DEFAULT_FILE_FORMAT,
    file_level=DEBUG,
):
    logger.setLevel(logger_level)

    if console:
        console_formatter = colorlog.ColoredFormatter(
            console_format,
            datefmt=None,
            reset=True,
            log_colors={
                "DEBUG": "blue",
                "INFO": "black,bg_green",
                "WARNING": "black,bg_yellow",
                "ERROR": "white,bg_red",
                "CRITICAL": "red,bg_white",
            },
            secondary_log_colors={},
            style="%",
        )
        console_handler = colorlog.StreamHandler()
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(console_level)
        logger.addHandler(console_handler)

    if file_name:
        file_formatter = logging.Formatter(file_format)
        file_handler = RotatingFileHandler(
            file_name, "a", maxBytes=10 * 1024 * 1024, backupCount=10
        )
        file_handler.setLevel(file_level)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    def _reduced_logging():
        logger.setLevel(WARNING)

    def _normal_logging():
        logger.setLevel(INFO)

    def _full_logging():
        logger.setLevel(DEBUG)

    logger.reduced_logging = _reduced_logging
    logger.normal_logging = _normal_logging
    logger.full_logging = _full_logging
