"""
Class representing a general error
"""
from ckf_api_toolkit.tools.logger import Logger, LogLevel


class GeneralError(Exception):
    """Class representing a general error

    Attributes:
        message (str): The error message
    """
    message: str

    def __init__(self, message: str):
        """Inits GeneralError with the given message and logging"""
        self.message = message
        self.log()

    def log(self):
        """Initialize logging for this error"""
        Logger().log(LogLevel.error, self.message, title="Exception")
