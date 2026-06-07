# logger.py
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

console_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(console_handler)