import logging
import sys

from .config import app_settings

LOG_LEVEL = {'debug': 10, 'info': 20, 'warning': 30, 'error': 40}


class LoggerSetup:
    """Class for setting up application logging."""

    def __init__(
        self,
        name: str = __name__,
    ) -> None:
        """
        Initialize the logger setup.

        :param name: Name of the logger
        :type name: str
        :param level: Logging level
        :type level: int
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(LOG_LEVEL[app_settings.log_level.value])

        if not self.logger.handlers:
            self._setup_handler()

    def _setup_handler(self) -> None:
        """Setup logging handler with formatter."""
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def get_logger(self) -> logging.Logger:
        """
        Get configured logger instance.

        :return: Configured logger
        :rtype: logging.Logger
        """
        return self.logger


def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a configured logger instance.

    :param name: Name of the logger
    :type name: str
    :return: Configured logger
    :rtype: logging.Logger
    """
    setup = LoggerSetup(name)
    return setup.get_logger()
