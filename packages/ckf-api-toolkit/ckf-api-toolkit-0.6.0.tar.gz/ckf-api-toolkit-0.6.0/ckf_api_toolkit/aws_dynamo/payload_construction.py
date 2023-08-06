"""
Dynamo Actor Payloads

Classes for constructing Actor payloads for various DynamoDB actions
"""
from enum import Enum
from typing import Any, Union, List

from ckf_api_toolkit.aws_dynamo.condition_expression import DynamoConditionExpressionFactory, \
    DynamoConditionExpressionComparisonComparator
from ckf_api_toolkit.aws_dynamo.constants import DynamoScalarSetDataType, DynamoAttribute, DynamoReturnValues
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.aws_dynamo.expression_attributes import DynamoExpressionAttributesNamesObject, \
    DynamoExpressionAttributesValuesObject, ExpressionAttributes
from ckf_api_toolkit.aws_dynamo.update_expression import DynamoUpdateExpressionFactory
from ckf_api_toolkit.tools.general_error import GeneralError

'''
============================
General
============================
'''


class DynamoKeyTooLong(GeneralError):
    def __init__(self):
        super().__init__(f"DynamoDB keys can only be a maximum of two attributes.")


class DynamoPayload:
    """
    Generic parent class for DynamoDB payloads, to be implemented for specific types
    """
    pass


class DynamoTableNamePayload(DynamoPayload):
    """A payload for a DynamoDB table

    Attributes:
          TableName (str): Name of the DynamoDB table to receive the payload
          IndexName (str): Name of the index on the table
    """
    TableName: str
    IndexName: str

    def __init__(self, *, table_name: str, index_name: str = None):
        """Inits DynamoTableNamePayload with table_name and index_name"""
        super().__init__()
        self.TableName = table_name
        if index_name:
            self.IndexName = index_name


class DynamoExpressionAttributeNamePayload(DynamoTableNamePayload):
    """A payload for a DynamoDB table using expression attribute names

    Attributes:
        ExpressionAttributeNames (DynamoExpressionAttributesNamesObject): The expression attribute names
    """
    ExpressionAttributeNames: DynamoExpressionAttributesNamesObject

    def __init__(self, **kwargs):
        """Inits DynamoExpressionAttributeNamePayload with kwargs and empty ExpressionAttributeNames"""
        super().__init__(**kwargs)
        self.ExpressionAttributeNames = {}

    def add_expression_attributes(self, expression_attributes: ExpressionAttributes):
        """Add the given expression attributes to the instance's expression attribute names

        Args:
            expression_attributes (ExpressionAttributes): The expression attributes to add
        """
        expression_attributes.merge_expression_attributes(
            expression_attribute_names=self.ExpressionAttributeNames,
        )
        if expression_attributes.expression_attribute_names:
            self.ExpressionAttributeNames = expression_attributes.expression_attribute_names


class DynamoExpressionAttributeValuePayload(DynamoExpressionAttributeNamePayload):
    """A payload for a DynamoDB table using expression attribute values

    Attributes:
        ExpressionAttributeValues (DynamoExpressionAttributesValuesObject): The expression attribute values
    """
    ExpressionAttributeValues: DynamoExpressionAttributesValuesObject

    def __init__(self, **kwargs):
        """Inits DynamoExpressionAttributeValuePayload with kwargs and empty ExpressionAttributeValues"""
        super().__init__(**kwargs)
        self.ExpressionAttributeValues = {}

    def add_expression_attributes(self, expression_attributes: ExpressionAttributes):
        """Add the given expression attributes to the instance's expression attribute names

        Args:
            expression_attributes (ExpressionAttributes): The expression attributes to add
        """
        expression_attributes.merge_expression_attributes(
            expression_attribute_values=self.ExpressionAttributeValues,
            expression_attribute_names=self.ExpressionAttributeNames,
        )
        if expression_attributes.expression_attribute_names:
            self.ExpressionAttributeNames = expression_attributes.expression_attribute_names
        if expression_attributes.expression_attribute_values:
            self.ExpressionAttributeValues = expression_attributes.expression_attribute_values


class DynamoConditionExpressionPayload(DynamoExpressionAttributeValuePayload, DynamoExpressionAttributeNamePayload):
    """A payload for a DynamoDB table with a condition expression

    Attributes:
        ConditionExpression (str): The condition expression to use in the payload
    """
    ConditionExpression: str

    def set_condition_expression(self, condition_expression_factory: DynamoConditionExpressionFactory):
        """Set the condition expression for this payload

        Args:
            condition_expression_factory (DynamoConditionExpressionFactory): The factory to create the condition
                expression with
        """
        self.ConditionExpression = condition_expression_factory.condition_expression
        self.add_expression_attributes(condition_expression_factory.expression_attributes)


class DynamoUpdateExpressionPayload(DynamoExpressionAttributeValuePayload, DynamoExpressionAttributeNamePayload):
    """A payload for a DynamoDB table with an update expression

    Attributes:
        UpdateExpression (str): The update expression to use in the payload
    """
    UpdateExpression: str

    def set_update_expression(self, update_expression_factory: DynamoUpdateExpressionFactory):
        """Set the update expression for this payload

        Args:
            update_expression_factory (DynamoUpdateExpressionFactory): The factory to create the update expression with
        """
        self.UpdateExpression = update_expression_factory.update_expression
        self.add_expression_attributes(update_expression_factory.expression_attributes)


class DynamoKeyedPayload(DynamoExpressionAttributeNamePayload):
    """A payload for a DynamoDB table using a key

    Attributes:
        Key (DynamoAttribute): The key to use for this payload
    """
    Key: DynamoAttribute

    def __init__(self, **kwargs):
        """Inits DynamoKeyedPayload with kwargs and an empty Key"""
        super().__init__(**kwargs)
        self.Key = {}

    def add_key_item(self, key_name: str, key_value: Any, *,
                     dynamo_set_type: DynamoScalarSetDataType = None):
        """Add key item to payload

        Args:
            key_name (str): The key name
            key_value (Any): The key value
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        if len(self.Key) >= 2:
            raise DynamoKeyTooLong()
        dynamo_value = convert_python_data_to_dynamo(key_value, dynamo_set_type=dynamo_set_type)
        self.Key[key_name] = dynamo_value


class DynamoReturnValuesPayload(DynamoExpressionAttributeNamePayload):
    """A payload for a DynamoDB table with return values

    Attributes:
        ReturnValues (str): The return values to deliver to the caller
    """
    ReturnValues: str

    def set_return_values(self, return_values: DynamoReturnValues):
        """Set the return values for ths payload

        Args:
            return_values (DynamoReturnValues): The return values to set
        """
        self.ReturnValues = return_values.value


'''
============================
Put Item
============================
'''


class DynamoPutItemPayload(DynamoConditionExpressionPayload, DynamoReturnValuesPayload):
    """A payload for a PUT operation

    Attributes:
        Item (DynamoAttribute): The item to put in the table
    """
    Item: DynamoAttribute

    def __init__(self, **kwargs):
        """Inits DynamoPutItemPayload with kwargs and empty Item"""
        super().__init__(**kwargs)
        self.Item = {}

    def set_attribute(self, attribute_name: str, attribute_value: Any, *,
                      dynamo_set_type: DynamoScalarSetDataType = None):
        """

        Args:
            attribute_name (str): The attribute name to use
            attribute_value (Any): The attribute value to use
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        dynamo_value = convert_python_data_to_dynamo(attribute_value, dynamo_set_type=dynamo_set_type)
        self.Item[attribute_name] = dynamo_value


'''
============================
Get Item
============================
'''


class DynamoGetItemPayload(DynamoKeyedPayload):
    """A payload for a GET operation"""
    pass


'''
============================
Scan
============================
'''


class DynamoScanPayload(DynamoTableNamePayload):
    """A payload for a SCAN operation"""


'''
============================
Query
============================
'''


class DynamoQueryKeyCondition(DynamoConditionExpressionFactory):
    """A query key condition for a condition expression

    Attributes:
        key_name (str): The key name to query on
    """
    key_name: str

    def __init__(self, key_name: str):
        """Inits DynamoQueryKeyCondition with key_name"""
        super().__init__()
        self.key_name = key_name

    def __add_key_comparison(self, comparator: DynamoConditionExpressionComparisonComparator, value: Any):
        """Add a comparison to the key

        Args:
            comparator (DynamoConditionExpressionComparisonComparator): The comparator to use for the key comparison
            value (Any): The value to compare against
        """
        self.add_comparison(
            self.get_name_operand(self.key_name),
            comparator,
            self.get_value_operand(value)
        )

    def add_key_equals(self, value: Any):
        """Add a comparison for the key equals the given value

        Args:
            value (Any): The value to compare against
        """
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.EQ, value)

    def add_key_less_than(self, value: Any):
        """Add a comparison for the key is less than the given value

        Args:
            value (Any): The value to compare against
        """
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.LT, value)

    def add_key_less_than_equals(self, value: Any):
        """Add a comparison for the key is less than or equals the given value

        Args:
            value (Any): The value to compare against
        """
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.LTE, value)

    def add_key_greater_than(self, value: Any):
        """Add a comparison for the key is greater than the given value

        Args:
            value (Any): The value to compare against
        """
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.GT, value)

    def add_key_greater_than_equals(self, value: Any):
        """Add a comparison for the key is greater than or equals the given value

        Args:
            value (Any): The value to compare against
        """
        self.__add_key_comparison(DynamoConditionExpressionComparisonComparator.GTE, value)

    def add_key_between(self, lower_value: Any, upper_value: Any):
        """Add a comparison for the key is between than the given value

        Args:
            lower_value (Any): The lower bound for the comparison
            upper_value (Any): The upper bound for the comparison
        """
        self.add_between(
            self.get_name_operand(self.key_name),
            self.get_value_operand(lower_value),
            self.get_value_operand(upper_value)
        )

    def add_key_begins_with(self, substring: str):
        """Add a comparison for the key beginning with the given substring

        Args:
            substring (str): The substring to check for inclusion in the key
        """
        self.add_begins_with(self.key_name, substring)


class DynamoQueryPayload(DynamoExpressionAttributeValuePayload):
    """A payload for a QUERY operation

    Attributes:
        KeyConditionExpression (str): The key condition expression to use for the query
        ExclusiveStartKey (str): An exclusive start key to use for the query
        Limit (int): The limit for the number of results to return
    """
    KeyConditionExpression: str
    ExclusiveStartKey: str
    Limit: int

    def __init__(self, **kwargs):
        """Inits DynamoQueryPayload with kwargs"""
        super().__init__(**kwargs)

    def add_partition_key_eq_condition_expression(self, partition_key_name: str, partition_key_value: Any,
                                                  sort_condition: DynamoQueryKeyCondition = None):
        """Add a partition key equals expression to the key condition expression

        Args:
            partition_key_name (str): The name of the partition key for key condition
            partition_key_value (Any): The value of the partition key for key condition
            sort_condition (DynamoQueryKeyCondition): Optional sort condition for the query
        """
        key_condition_expression = DynamoConditionExpressionFactory()
        key_condition_expression.add_comparison(
            key_condition_expression.get_name_operand(partition_key_name),
            DynamoConditionExpressionComparisonComparator.EQ,
            key_condition_expression.get_value_operand(partition_key_value)
        )
        if sort_condition:
            key_condition_expression.append_logical_and(sort_condition)

        self.add_expression_attributes(key_condition_expression.expression_attributes)
        self.KeyConditionExpression = key_condition_expression.condition_expression

    def set_page_start_key(self, page_start_key: str):
        """Set the start key for a page of results

        Args:
            page_start_key (str): The page start key to use
        """
        self.ExclusiveStartKey = page_start_key

    def set_query_limit(self, limit: int):
        """Set the query limit for results

        Args:
            limit (int): The limit to use for the query
        """
        self.Limit = limit


'''
============================
Update Item
============================
Reference:
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html
'''


class DynamoUpdateItemPayload(DynamoUpdateExpressionPayload, DynamoConditionExpressionPayload, DynamoKeyedPayload,
                              DynamoReturnValuesPayload):
    """A payload for an UPDATE operation"""
    pass


'''
============================
Delete Item
============================
'''


class DynamoDeleteItemPayload(DynamoConditionExpressionPayload, DynamoKeyedPayload):
    """A payload for a DELETE operation"""
    pass


'''
============================
Transact Write Items
============================
'''

TransactWriteItemsPayloadType = Union[DynamoPutItemPayload, DynamoUpdateItemPayload, DynamoDeleteItemPayload]


class DynamoTransactItemType(Enum):
    """Enum representing DynamoDB transaction types for an item write.
    Note: you can only target a given item with a single operation per transaction, per docs:
    https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html"""
    ConditionCheck = 'ConditionCheck'
    Put = 'Put'
    Delete = 'Delete'
    Update = 'Update'


class DynamoTransactWriteItemsConditionCheck(DynamoKeyedPayload, DynamoConditionExpressionPayload):
    """A condition check for a write transaction"""
    pass


class DynamoTransactWriteItemsPayload(DynamoPayload):
    """A payload for a write transaction

    Attributes:
        TransactItems (List[dict])
    """
    TransactItems: List[dict]

    def __init__(self):
        """Inits DynamoTransactWriteItemsPayload with empty TransactItems"""
        super().__init__()
        self.TransactItems = []

    def add_item_payload(self, item_payload: TransactWriteItemsPayloadType,
                         # return_values: TransactItemReturnValues = TransactItemReturnValues.Key
                         ):
        """Add an item payload to the transaction

        Args:
            item_payload (TransactWriteItemsPayloadType): The item payload to add
        """
        transact_item = {}
        payload_type = type(item_payload)

        if payload_type is DynamoPutItemPayload:
            transact_item = {DynamoTransactItemType.Put.value: vars(item_payload)}
        elif payload_type is DynamoUpdateItemPayload:
            transact_item = {DynamoTransactItemType.Update.value: vars(item_payload)}
        elif payload_type is DynamoDeleteItemPayload:
            transact_item = {DynamoTransactItemType.Delete.value: vars(item_payload)}

        if transact_item:
            # transact_item['ReturnValue'] = return_values.value
            self.TransactItems.append(transact_item)

    def add_condition_check(self, condition_check: DynamoTransactWriteItemsConditionCheck):
        """Add the given condition check to the transaction

        Args:
            condition_check (DynamoTransactWriteItemsConditionCheck): The condition check to add
        """
        self.TransactItems.append({DynamoTransactItemType.ConditionCheck.value: vars(condition_check)})
