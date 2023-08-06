"""
Decorator for AWS Lambda handlers to deal with responses and mapping args and kwargs
"""
from functools import wraps
from typing import Callable, Any, Tuple, List, Optional

from ckf_api_toolkit.tools.api_response_handler import ApiResponseFactory, ApiResponseException
from ckf_api_toolkit.tools.error_handling import get_trace
from ckf_api_toolkit.tools.logger import Logger, LogLevel

# Takes *args, **kwargs from the platform event/input as arguments.
# Maps a value to be passed as an arg to the decorated handler.
ArgMapper = Callable[[Tuple[Any], dict], Any]

# Takes *args, **kwargs from the platform event/input as arguments.
# Maps a tuple of (kwarg, value) to be passed as a kwargs to the decorated handler
KwargMapper = Callable[[Tuple[Any], dict], Tuple[str, Any]]

HandlerFunction = Callable[[ApiResponseFactory, Tuple[Any], dict], ApiResponseFactory]


def handler(response_factory: ApiResponseFactory, *, arg_mappers: Optional[List[ArgMapper]] = None,
            kwarg_mappers: Optional[List[KwargMapper]] = None):
    """Decorator for AWS Lambda handlers to deal with responses and mapping args and kwargs

    Args:
        response_factory (ApiResponseFactory): Instance of required implementation specific ApiResponseFactory
        arg_mappers (Optional[List[ArgMapper]]): List of arg mappers
        kwarg_mappers (Optional[List[KwargMapper]]): List of kwarg mappers
    """
    arg_mappers = arg_mappers if arg_mappers else []
    kwarg_mappers = kwarg_mappers if kwarg_mappers else []

    def decorator(handler_function: HandlerFunction):
        @wraps(handler_function)
        def wrapper(*args, **kwargs):
            try:
                handler_args = tuple(mapper(*args, **kwargs) for mapper in arg_mappers)
                handler_kwargs = \
                    {kwarg: value for kwarg, value in [mapper(*args, **kwargs) for mapper in kwarg_mappers]}

                response = handler_function(response_factory, *handler_args, **handler_kwargs)
                return response.get_response()
            except ApiResponseException as error:
                response_factory.set_exception(error)
                return response_factory.get_response()
            except Exception as error:
                Logger().log(LogLevel.error, get_trace(), title="Uncaught Exception")
                response_factory.set_exception(error)
                return response_factory.get_response()

        return wrapper

    return decorator
