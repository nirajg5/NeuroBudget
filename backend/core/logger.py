"""
Centralized Logger
"""

import sys

from loguru import logger

# Remove default logger
logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
           "{message}"
)

# File Logger
logger.add(
    "logs/neurobudget.log",
    level="INFO",
    rotation="10 MB",
    retention="30 days",
    compression="zip",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    format="{time:YYYY-MM-DD HH:mm:ss} | "
           "{level} | "
           "{name}:{function}:{line} | "
           "{message}"
)