"""
S3 Actor Models

S3 specific versions of the classes used by an Actor.
"""
from functools import wraps
from json import dumps, loads
from typing import Callable, Union

import boto3
from botocore.client import BaseClient
from botocore.exceptions import ClientError

from ckf_api_toolkit.aws_s3.s3_constants import S3GetObjectResponse
from ckf_api_toolkit.aws_s3.s3_payload_construction import S3Payload, S3GetObjectPayload, S3PutObjectPayload, \
    S3DeleteObjectPayload
from ckf_api_toolkit.core import ActionType, Instruction, Client, Repository
from ckf_api_toolkit.tools.logger import Logger, LogLevel


class S3ActionType(ActionType):
    """Enum representing the action types supported for S3"""
    READ_OBJECT = "READ_OBJECT"
    WRITE_OBJECT = "WRITE_OBJECT"
    DELETE_OBJECT = "DELETE_OBJECT"


class S3Instruction(Instruction):
    """Instruction implementation for AWS S3"""
    def __init__(self, action_type: S3ActionType, payload: S3Payload, parser: Callable):
        super().__init__(action_type, payload, parser)


def _log_s3_payload(func: Callable):
    """Decorator to log an S3 payload"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload_dict = vars(args[1])
        try:
            Logger().log(LogLevel.debug, payload_dict, title=f"S3 Payload for: {func.__name__}", pretty_json=True)
        except TypeError:
            Logger().log(LogLevel.debug, 'Payload contents were not JSON serializable',
                         title=f"S3 Payload for: {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


class S3Client(Client):
    """Client Implementation for AWS S3"""
    __client: BaseClient

    def __init__(self):
        """Inits client with known S3 actions"""
        super().__init__()
        self.__client = boto3.client('s3')
        self.add_action_type(S3ActionType.WRITE_OBJECT, self.__write_object)
        self.add_action_type(S3ActionType.READ_OBJECT, self.__read_object)
        self.add_action_type(S3ActionType.DELETE_OBJECT, self.__delete_object)

    @_log_s3_payload
    def __read_object(self, payload: S3GetObjectPayload) -> S3GetObjectResponse:
        """Get an object from S3

        Args:
            payload (S3GetObjectPayload): The payload for an S3 GetObject call

        Returns:
            (S3GetObjectResponse) The response from the get object call
        """
        return S3GetObjectResponse(**self.__client.get_object(**vars(payload)))

    @_log_s3_payload
    def __write_object(self, payload: S3PutObjectPayload):
        """Write an object from S3

        Args:
            payload (S3PutObjectPayload): The payload for an S3 PutObject call
        """
        return self.__client.put_object(**vars(payload))

    @_log_s3_payload
    def __delete_object(self, payload: S3DeleteObjectPayload):
        """Delete an object from S3

        Args:
            payload (S3DeleteObjectPayload): The payload for an S3 DeleteObject call
        """
        return self.__client.delete_object(**vars(payload))


ENCODING: str = 'utf-8'


class S3ItemNotFound(Exception):
    """Error representing the S3 object can't be found"""
    pass


class S3Repository(Repository):
    """
    A Repository that represents an S3 bucket
    """
    def __init__(self):
        """Inits S3Repository"""
        super().__init__()
        self.add_error_conversion(ClientError, S3ItemNotFound, [self.__not_found_error_parser])

    @staticmethod
    def __not_found_error_parser(error: ClientError) -> Union[S3ItemNotFound, bool]:
        """Parse an S3 client error to check for item not found error code

        Args:
            error (ClientError): The client error to parse

        Returns:
            (Union[S3ItemNotFound, bool])
        """
        return S3ItemNotFound if error.response['Error']['Code'] == 'NoSuchKey' else False

    @staticmethod
    def _convert_item_to_bytes(event_item: dict) -> bytes:
        """Convert an event item dict to bytes

        Args:
            event_item (dict): The dict to encode

        Returns:
            (bytes) Binary representation of the event item dict
        """
        return dumps(event_item).encode(ENCODING)

    @staticmethod
    def __parse_item(bytes_response: bytes) -> dict:
        """Parse a binary-encoded object into a dictionary

        Args:
            bytes_response (bytes): The binary object to parse

        Returns:
            (dict) The parsed dictionary
        """
        event_item = loads(bytes_response.decode(ENCODING), encoding=ENCODING)
        Logger().log(LogLevel.debug, event_item, title="S3 Item", pretty_json=True)
        return event_item

    @staticmethod
    def __get_data_from_get_response(get_object_response: S3GetObjectResponse) -> bytes:
        """Parse the data out from a binary get response

        Args:
            get_object_response (S3GetObjectResponse): The object response to parse

        Returns:
            (S3GetObjectResponse) The response to parse
        """
        try:
            data = get_object_response.Body.read()
        finally:
            get_object_response.Body.close()

        return data

    def _get_item_parser(self, s3_response: S3GetObjectResponse) -> dict:
        """Return a parser for an S3 get object request

        Args:
            s3_response (S3GetObjectResponse): The object response to parse

        Returns:
            (dict) The parsed event response
        """
        return self.__parse_item(self.__get_data_from_get_response(s3_response))
