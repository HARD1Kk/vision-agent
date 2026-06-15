import sys

from loguru import logger

# 1. Remove the default logger configured by loguru
logger.remove()

# 2. Add a Console Handler (Colorful and easy to read)
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

# 3. Add a File Handler (Rotates automatically when it hits 10MB, keeps logs for 7 days)
logger.add(
    "logs/app.log",
    level="DEBUG",  # Save more detailed logs to the file
    rotation="10 MB",
    retention="7 days",
    compression="zip",  # Compress old logs to save space
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
)
