import inspect
import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_FILE = os.path.join(BASE_DIR, os.environ["LOG_FILE"])

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

loggers_cache = {}


def get_caller_module() -> str:
    stack = inspect.stack()
    for frame in stack:
        module = inspect.getmodule(frame[0])
        if module and module.__file__ != __file__:
            return os.path.splitext(os.path.basename(module.__file__))[0]
    return "unknown"


def get_logger() -> logging.Logger:
    module_name = get_caller_module()

    if module_name in loggers_cache:
        return loggers_cache[module_name]

    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)

        file_handler = RotatingFileHandler(LOG_FILE, maxBytes=10 * 1024 * 1024, backupCount=3)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(formatter)

        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    loggers_cache[module_name] = logger
    return logger


def log_debug(message: str):
    get_logger().debug(message)


def log_info(message: str):
    get_logger().info(message)


def log_warning(message: str):
    get_logger().warning(message)


def log_error(message: str):
    get_logger().error(message)


def log_critical(message: str):
    get_logger().critical(message)
