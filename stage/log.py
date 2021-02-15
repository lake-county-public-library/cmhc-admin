"""Custom logging."""
from sys import stdout, stderr
from loguru import logger as custom_logger
from pathlib import Path


def create_logger():
  """Create custom logger."""
  custom_logger.remove()
  custom_logger.add(
    stdout,
    colorize=True,
    level="INFO",
    format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | \
    <light-green>{level}</light-green>: \
    <light-black>{message}</light-black>"
  )
  BASE_DIR = Path(__file__).resolve().parent.parent
  custom_logger.add(
    str(BASE_DIR) + '/logs/errors.log',
    colorize=True,
    level="ERROR",
    rotation="200 MB",
    catch=True,
    format="<light-cyan>{time:MM-DD-YYYY HH:mm:ss}</light-cyan> | \
    <light-red>{level}</light-red>: \
    <light-black>{message}</light-black>"
  )
  return custom_logger

logger = create_logger()
