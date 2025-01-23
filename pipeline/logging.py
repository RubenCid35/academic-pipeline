import logging
import sys

# Setup basic logging configuration
logging.basicConfig(
    level=logging.WARN,  # Set the default logging level
    format="%(asctime)s %(name)s.%(funcName)s +%(lineno)s: %(levelname)-8s %(message)s",
    stream=sys.stdout  # Log to stdout (Google Cloud Run captures stdout by default)
)

# Get a logger instance for your application
logger = logging.getLogger(__name__)