"""
Error conversion tools
"""
from traceback import format_exc
from typing import Callable, NamedTuple, List, Union, Type

from ckf_api_toolkit.tools.logger import Logger, LogLevel


def get_trace() -> str:
    """Returns a formatted trace

    Returns:
        (str) The formatted trace
    """
    return format_exc()


ErrorParser = Callable[[Exception], Union[Type[Exception], Union[Type[Exception], bool]]]


class ErrorConversion(NamedTuple):
    """NamedTuple wrapping an error conversion"""
    incoming_error: Type[Exception]
    outgoing_error: Type[Exception]
    error_parsers: List[ErrorParser] = []


class ErrorConverter:
    """Class to convert errors from a source client to a custom implementation

    Attributes:
        error_conversions (List[ErrorConversion]):
    """
    error_conversions: List[ErrorConversion]

    def __init__(self):
        """Inits ErrorConverter with empty error_conversions"""
        self.error_conversions = []

    def add_error_conversion(self, incoming_error: Type[Exception], outgoing_error: Type[Exception],
                             error_parsers: List[ErrorParser] = None):
        """Convert an incoming error to an outgoing error, using the given error parsers

        Args:
            incoming_error (Exception): The error to convert from
            outgoing_error (Exception): The error to convert to
            error_parsers (List[ErrorParser]): A list of error parsers to check against
        """
        self.error_conversions.append(
            ErrorConversion(incoming_error=incoming_error, outgoing_error=outgoing_error,
                            error_parsers=error_parsers if error_parsers else []))

    def handle_error(self, error: Exception):
        """Convert the error if it exists in the list of error conversions

        Args:
            error (Exception): The error to convert
        """
        Logger().log(LogLevel.debug, error, title=f"Error Handler - Error Class: {type(error)}")
        current_error = error
        for conversion in self.error_conversions:
            Logger().log(LogLevel.debug, (
                f"Incoming error type: {conversion.incoming_error}\n"
                f"Outgoing error type: {conversion.outgoing_error}"
            ), title=f"Error Handler - Converter")
            if isinstance(current_error, conversion.incoming_error):
                incoming_error = current_error
                Logger().log(LogLevel.debug, conversion.outgoing_error, title="Error Handler - Conversion Matched")
                current_error = conversion.outgoing_error()
                for error_parser in conversion.error_parsers:
                    parsed_error = error_parser(incoming_error)
                    if parsed_error:
                        Logger().log(LogLevel.debug, parsed_error, title="Error Handler - Parsed Error")
                        current_error = parsed_error()
        raise current_error
