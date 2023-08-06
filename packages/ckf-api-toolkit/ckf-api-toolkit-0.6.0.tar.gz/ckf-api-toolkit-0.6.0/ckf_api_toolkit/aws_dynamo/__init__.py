"""Tools to help construct DynamoDB payloads and queries, as well as aid with implementing the overloaded GSI pattern"""
from functools import wraps
from typing import Callable, Union, List, Type

import boto3
from botocore.exceptions import ClientError

from ckf_api_toolkit.core import ActionType, Instruction, Client, Repository
from ckf_api_toolkit.aws_dynamo.constants import DynamoAttributesResponse, DynamoItemResponse, DynamoItemsResponse, \
    DynamoDataType
from ckf_api_toolkit.aws_dynamo.converter import convert_dynamo_data_to_python
from ckf_api_toolkit.aws_dynamo.payload_construction import DynamoPayload, DynamoQueryPayload
from ckf_api_toolkit.tools.logger import Logger, LogLevel
from ckf_api_toolkit.tools.model import Model


class DynamoActionType(ActionType):
    """Enum for the action types supported by DynamoDB"""
    PUT = "PUT"
    GET = "GET"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    # TODO: Put this back in once the payload factory used by the Client method is finished
    # TRANSACT_GET = "TRANSACT_GET"
    TRANSACT_WRITE = "TRANSACT_WRITE"
    QUERY = "QUERY"
    SCAN = "SCAN"


class DynamoInstruction(Instruction):
    """Instruction implementation for AWS DynamoDB"""

    def __init__(self, action_type: DynamoActionType, payload: DynamoPayload, parser: Callable):
        super().__init__(action_type, payload, parser)


class DynamoRequestNotFound(Exception):
    """Custom error to represent 'items not found'"""
    pass


def _error_on_not_found(func: Callable):
    """Decorator to return DynamoRequestNotFound to be caught and handled upstream

    Args:
        func (Callable): The function to decorate
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            response: Union[DynamoAttributesResponse, DynamoItemResponse, DynamoItemsResponse] = func(*args, **kwargs)
        except TypeError:
            raise DynamoRequestNotFound()

        if isinstance(response, DynamoItemsResponse) and not response.Items:
            raise DynamoRequestNotFound()

        return response

    return wrapper


def _log_dynamo_payload(func: Callable):
    """Decorator to log the DynamoDB payload for a handler

    Args:
        func (Callable): The function to decorate
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        payload_dict = vars(args[1])
        Logger().log(LogLevel.debug, payload_dict, title=f"Dynamo Payload for: {func.__name__}", pretty_json=True)
        return func(*args, **kwargs)

    return wrapper


class DynamoClient(Client):
    """Client Implementation for AWS DynamoDB"""
    def __init__(self, region_name: str):
        """Inits Client with known DynamoDB actions, for the given region"""
        super().__init__()
        self.__client = boto3.client("dynamodb", region_name=region_name)
        self.add_action_type(DynamoActionType.PUT, self.__put_item)
        self.add_action_type(DynamoActionType.GET, self.__get_item)
        self.add_action_type(DynamoActionType.UPDATE, self.__update_item)
        self.add_action_type(DynamoActionType.DELETE, self.__delete_item)
        # TODO: Put this back in once the payload factory used by the Client method is finished
        # self.add_action_type(DynamoActionType.TRANSACT_GET, self.__transact_get_items)
        self.add_action_type(DynamoActionType.TRANSACT_WRITE, self.__transact_write_items)
        self.add_action_type(DynamoActionType.QUERY, self.__query)
        self.add_action_type(DynamoActionType.SCAN, self.__scan)

    def __sanitize_payload(self, payload_object: Union[dict, list]) -> Union[dict, list]:
        """Sanitize a DynamoClient payload

        Args:
            payload_object (Union[dict, list]): Original payload to be sanitized

        Returns:
            (Union[dict, list] The sanitized payload
        """
        # Dump empty kwargs from payload object
        if not isinstance(payload_object, (dict, list)):
            return payload_object
        if isinstance(payload_object, list):
            return [v for v in (self.__sanitize_payload(v) for v in payload_object) if v]

        # Keep empty Dynamo Values
        for data_type_value in [data_type.value for data_type in DynamoDataType]:
            if data_type_value in payload_object.keys():
                return payload_object

        return {k: v for k, v in ((k, self.__sanitize_payload(v)) for k, v in payload_object.items()) if v}

    @_log_dynamo_payload
    def __put_item(self, payload: DynamoPayload):
        """Perform a DynamoDB PUT action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction
        """
        return self.__client.put_item(**self.__sanitize_payload(vars(payload)))

    @_log_dynamo_payload
    @_error_on_not_found
    def __get_item(self, payload: DynamoPayload) -> DynamoItemResponse:
        """Perform a DynamoDB GET action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction

        Returns:
            (DynamoItemResponse) The response from the interaction containing the requested item
        """
        return DynamoItemResponse(**self.__client.get_item(**self.__sanitize_payload(vars(payload))))

    @_log_dynamo_payload
    def __update_item(self, payload: DynamoPayload) -> DynamoAttributesResponse:
        """Perform a DynamoDB UPDATE action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction

        Returns:
            (DynamoAttributesResponse) The response from the interaction containing the item's attributes
        """
        return DynamoAttributesResponse(**self.__client.update_item(**self.__sanitize_payload(vars(payload))))

    @_log_dynamo_payload
    def __delete_item(self, payload: DynamoPayload):
        """Perform a DynamoDB DELETE action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction
        """
        return self.__client.delete_item(**self.__sanitize_payload(vars(payload)))

    # TODO: create payload factory for a transactional GET and fix the return type on this method
    @_log_dynamo_payload
    def __transact_get_items(self, payload: DynamoPayload):
        """Perform a DynamoDB TRANSACT_GET action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction
        """
        return self.__client.transact_get_items(**self.__sanitize_payload(vars(payload)))

    @_log_dynamo_payload
    def __transact_write_items(self, payload: DynamoPayload):
        """Perform a DynamoDB TRANSACT_WRITE action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction
        """
        return self.__client.transact_write_items(**self.__sanitize_payload(vars(payload)))

    @_log_dynamo_payload
    @_error_on_not_found
    def __query(self, payload: DynamoQueryPayload) -> List[DynamoItemsResponse]:
        """Perform a DynamoDB QUERY action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction

        Returns:
            (List[DynamoItemsResponse]) A list of results from the query
        """
        items = []
        page_key = 'start'
        while page_key:
            if page_key and page_key != 'start':
                payload.set_page_start_key(page_key)
            current_response = DynamoItemsResponse(**self.__client.query(**self.__sanitize_payload(vars(payload))))
            items.append(current_response)
            page_key = current_response.LastEvaluatedKey if current_response.LastEvaluatedKey else None
        return items

    @_log_dynamo_payload
    def __scan(self, payload: DynamoPayload) -> DynamoItemsResponse:
        """Perform a DynamoDB SCAN action

        Args:
            payload (DynamoPayload): The payload to submit for the interaction

        Returns:
            (DynamoItemsResponse) The items response from the scan
        """
        return DynamoItemsResponse(**self.__client.scan(**self.__sanitize_payload(vars(payload))))


class DynamoClientErrorException(Exception):
    """Custom error to represent a DynamoDB generic client error"""
    pass


class DynamoConditionCheckFailed(DynamoClientErrorException):
    """Custom error to represent a DynamoDB condition check failing"""
    pass


class DynamoExceededProvisionedThroughput(DynamoClientErrorException):
    """Custom error to represent a DynamoDB provisioned throughput exceeded error"""
    pass


class DynamoRepository(Repository):
    """A Repository that represents a DynamoDB table

    Attributes:
        table_name (str): Name of the DynamoDB table to use for this Repository
    """
    table_name: str

    def __init__(self, table_name: str):
        """Inits DynamoRepository with table_name"""
        super().__init__()
        self.table_name = table_name
        self.add_error_conversion(ClientError, DynamoClientErrorException, [self.__parse_client_error])

    @staticmethod
    def __parse_client_error(error: ClientError) -> Union[Type[DynamoClientErrorException], bool]:
        """Parse the given ClientError and return an appropriate
            error (ClientError): The ClientError to parse

        Returns:
            Union[Type[DynamoClientErrorException], bool] The resultant custom client error, or False
        """
        error_code = error.response['Error']['Code']
        # TODO: Add more error type parsing
        if error_code == 'ConditionalCheckFailedException':
            return DynamoConditionCheckFailed
        elif error_code == 'ProvisionedThroughputExceededException':
            return DynamoExceededProvisionedThroughput
        else:
            return False

    @staticmethod
    def _dynamo_item_parser(dynamo_response: DynamoItemResponse) -> dict:
        """Return the parsed Dynamo Item as a dictionary

        Args:
            dynamo_response (DynamoItemResponse): A DynamoItemResponse to parse

        Returns:
            (dict) dictionary representation of Dynamo Item
        """
        Logger().log(LogLevel.debug, dynamo_response._asdict(), title="Dynamo Item Response", pretty_json=True)
        return {key: convert_dynamo_data_to_python(dynamo_value) for key, dynamo_value in dynamo_response.Item.items()}

    def _dynamo_items_parser(self, dynamo_response: DynamoItemsResponse) -> List[dict]:
        """Return the parsed Dynamo Items as a list of dictionaries

        Args:
            dynamo_response (DynamoItemsResponse): A DynamoItemsResponse to parse

        Returns:
            (List[dict]) A list of dictionary representations of the DynamoItemsResponse
        """
        Logger().log(LogLevel.debug, dynamo_response._asdict(), title="Dynamo Items Response", pretty_json=True)
        return [self._dynamo_item_parser(DynamoItemResponse(Item=item)) for item in dynamo_response.Items]

    def _dynamo_query_parser(self, query_responses: List[DynamoItemsResponse]) -> List[dict]:
        """Return the parsed list of DynamoItemsResponse as a list of dictionaries

        Args:
            query_responses (List[DynamoItemsResponse]): A list of DynamoItemsResponse to parse

        Returns:
            (List[dict]) A list of dictionary representations of the list of DynamoItemsResponse
        """
        return [item for single_response in query_responses for item in self._dynamo_items_parser(single_response)]

    @staticmethod
    def _dynamo_attributes_parser(dynamo_response: DynamoAttributesResponse) -> [dict]:
        """Return the parsed DynamoAttributesResponse as a list of dictionaries

        Args:
            dynamo_response (DynamoAttributesResponse): A DynamoAttributesResponse to parse

        Returns:
            ([dict]) A list of dictionary representations of the DynamoAttributesResponse
        """
        Logger().log(LogLevel.debug, dynamo_response._asdict(), title="Dynamo Attributes Response", pretty_json=True)
        return {key: convert_dynamo_data_to_python(dynamo_value) for key, dynamo_value in
                dynamo_response.Attributes.items()}

    def _get_model_item_parser(self, dynamo_response: DynamoItemResponse, model_class: Type[Model], *,
                               private: bool = False, as_instance: bool = False) -> Union[dict, Model]:
        """Return either a dictionary representation or Model instance of the given class from the given
        DynamoItemResponse following item retrieval

        Args:
            dynamo_response (DynamoItemResponse): A DynamoItemResponse to parse for instantiation
            model_class (Type[Model]): A Model to instantiate based on the given DynamoItemResponse
            private (bool): Whether or not to include private/non-public attrs for the Model(dependant on child class
                implementation
            as_instance (bool): Whether to return a Model instance(True) or a dictionary representation(False)

        Returns:
            (Union[dict, Model]) Either a dictionary representation or Model instance of the DynamoItemResponse
        """
        model_instance = model_class.init_from_db(self._dynamo_item_parser(dynamo_response))
        model_dict = model_instance.get_dict_for_front_end(private=private)
        Logger().log(LogLevel.debug, model_dict, title=f"{model_class.__name__}", pretty_json=True)
        return model_dict if not as_instance else model_instance

    def _update_model_item_parser(self, dynamo_response: DynamoAttributesResponse, model_class: Type[Model], *,
                                  private: bool = False, as_instance: bool = False) -> Union[dict, Model]:
        """Return either a dictionary representation or Model instance of the given class from the given
        DynamoAttributesResponse following an item update

        Args:
            dynamo_response (DynamoAttributesResponse): A DynamoAttributesResponse to parse for instantiation
            model_class (Type[Model]): A Model to instantiate based on the given DynamoAttributesResponse
            private (bool): Whether or not to include private/non-public attrs for the Model(dependant on child class
                implementation
            as_instance (bool): Whether to return a Model instance(True) or a dictionary representation(False)

        Returns:
            (Union[dict, Model]) Either a dictionary representation or Model instance of the DynamoAttributesResponse
        """
        model_instance: Model = model_class.init_from_db(self._dynamo_attributes_parser(dynamo_response))
        model_dict = model_instance.get_dict_for_front_end(private=private)
        Logger().log(LogLevel.debug, model_dict, title=f"{model_class.__name__}", pretty_json=True)
        return model_dict if not as_instance else model_instance

    def _query_model_item_list_parser(self, dynamo_response: List[DynamoItemsResponse], model_class: Type[Model], *,
                                      private: bool = False,
                                      as_instance: bool = False) -> Union[List[dict], List[Model]]:
        """Return either a dictionary representation or Model instance of the given class from the given
        List[DynamoItemsResponse] following a query

        Args:
            dynamo_response (List[DynamoItemsResponse]): A DynamoAttributesResponse to parse for instantiation
            model_class (Type[Model]): A Model to instantiate based on the given List[DynamoItemsResponse]
            private (bool): Whether or not to include private/non-public attrs for the Model(dependant on child class
                implementation
            as_instance (bool): Whether to return a Model instance(True) or a dictionary representation(False)

        Returns:
            (Union[List[dict], List[Model]]) Either a list of dictionary representations or Model instances of the
                List[DynamoItemsResponse]
        """
        model_instances: List[Model] = [model_class.init_from_db(db_object) for db_object in
                                        self._dynamo_query_parser(dynamo_response)]
        model_dicts: List[dict] = [model_instance.get_dict_for_front_end(private=private) for model_instance in
                                   model_instances]
        Logger().log(LogLevel.debug, model_dicts, title=f"List of {model_class.__name__}", pretty_json=True)
        return model_dicts if not as_instance else model_instances

    def _query_single_model_item_parser(self, dynamo_response: List[DynamoItemsResponse], model_class: Type[Model], *,
                                        as_instance=False, private=False) -> Union[dict, Model]:
        """Return either a dictionary representation or Model instance of the given class from the given
        List[DynamoItemsResponse] following a query

        Args:
            dynamo_response (List[DynamoItemsResponse]): A DynamoAttributesResponse to parse for instantiation
            model_class (Type[Model]): A Model to instantiate based on the given List[DynamoItemsResponse]
            private (bool): Whether or not to include private/non-public attrs for the Model(dependant on child class
                implementation
            as_instance (bool): Whether to return a Model instance(True) or a dictionary representation(False)

        Returns:
            (Union[dict, Model]) Either a dictionary representation or Model instance of the list of
                DynamoAttributesResponse
        """
        parsed_response = self._dynamo_query_parser(dynamo_response)
        if not parsed_response:
            raise DynamoRequestNotFound()
        model_instance: Model = model_class.init_from_db(parsed_response[0])
        model_dict = model_instance.get_dict_for_front_end(private=private)
        Logger().log(LogLevel.debug, model_dict, title=f"{model_class.__name__}", pretty_json=True)
        return model_dict if not as_instance else model_instance
