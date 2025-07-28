
import logging
from logging.handlers import RotatingFileHandler
import os

# Import sentry_sdk only if available
try:
    from sentry_sdk import init as sentry_init
    SENTRY_AVAILABLE = True
except ImportError:
    SENTRY_AVAILABLE = False

from utils.config import settings

# Initialize Sentry if DSN is provided and available
if SENTRY_AVAILABLE and getattr(settings, "SENTRY_DSN", None):
    sentry_init(dsn=settings.SENTRY_DSN)

# Create logs directory if it doesn't exist
logs_dir = "logs"
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure root logger
logger = logging.getLogger("snowbird")
logger.setLevel(getattr(logging, getattr(settings, "LOG_LEVEL", "INFO").upper()))

# File handler
log_file_path = os.path.join(logs_dir, "snowbird.log")
file_handler = RotatingFileHandler(log_file_path, maxBytes=1_000_000, backupCount=3)
file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(file_handler)

# Console handler for development
if settings.DEBUG:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.addHandler(console_handler)
