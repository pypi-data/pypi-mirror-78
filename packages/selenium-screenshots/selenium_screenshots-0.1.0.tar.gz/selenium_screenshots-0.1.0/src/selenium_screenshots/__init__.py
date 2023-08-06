"""Python package to handle creation of many screenshots for selenium"""
# Standard library imports
import logging

# Third party imports

# Local imports
from selenium_screenshots.main import Screenshots

__all__ = ["Screenshots"]


#####
# Prepare basic logger in case user is not setting it itself.
#####
LOGGER = logging.getLogger("selenium_screenshots")
LOGGER.propagate = False
LOGGER.setLevel(level=logging.WARNING)  # Or any level you see suitable now

stdout_handler = logging.StreamHandler()
stdout_handler.setFormatter(
    logging.Formatter("%(asctime)s - [%(levelname)s]: %(message)s"))
LOGGER.addHandler(stdout_handler)
