"""
Dynamo Expression Attributes

References:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeNames.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ExpressionAttributeValues.html

Note: Dynamo does support dots (".") in attribute names. This library does not support this currently and always treats
a dot as a document path separator.
"""
import re
from typing import Dict
from uuid import uuid4

from ckf_api_toolkit.aws_dynamo.constants import DynamoValue
from ckf_api_toolkit.tools.general_error import GeneralError


class InvalidIndexFormat(GeneralError):
    """
    Custom error indicating an invalid index in the path
    """
    def __init__(self, path: str):
        super().__init__(f"Provided path has improperly formatted index: {path}")


DynamoExpressionAttributesNamesObject = Dict[str, str]
DynamoExpressionAttributesValuesObject = Dict[str, DynamoValue]


class ExpressionAttributes:
    """Class representing DynamoDB expression attributes

    Attributes:
        expression_attribute_names (DynamoExpressionAttributesNamesObject): Dictionary of expression attribute names
        expression_attribute_values (DynamoExpressionAttributesValuesObject): Dictionary of expression attribute values

    """
    expression_attribute_names: DynamoExpressionAttributesNamesObject
    expression_attribute_values: DynamoExpressionAttributesValuesObject

    def __init__(self):
        self.expression_attribute_values = {}
        self.expression_attribute_names = {}

    def set_expression_attribute_name(self, path: str) -> str:
        """Add an attribute name to the expression attribute names, and return the unique expression attribute name

        Args:
            path (str): The path of the attribute to set the name for

        Returns:
            (str)
        """
        full_expression_attribute_name = ""

        def __parse_index(possibly_indexed_string: str) -> (str, str):
            """Parse the given index and return the root name and index string

            Args:
                possibly_indexed_string (str): The supplied name to search for

            Returns:
                (str, str) A tuple of the root name and index string
            """
            # noinspection RegExpRedundantEscape
            index_match = re.search(r"\[(.*?)\]", possibly_indexed_string)
            if not index_match:
                return possibly_indexed_string, ""
            else:
                start_index = index_match.start()
                end_index = index_match.end()
                matched_index_str = index_match.group()
                if end_index != len(possibly_indexed_string):
                    raise InvalidIndexFormat(possibly_indexed_string)
                return possibly_indexed_string[:start_index], matched_index_str

        def __set_name_and_expression(supplied_name: str) -> str:
            """Set the full expression attribute from the supplied name

            Args:
                supplied_name (str): Supplied name for the attribute

            Returns:
                (str) Full expression attribute name
            """
            root_name, index_str = __parse_index(supplied_name)
            expression_attribute_name = f"#{uuid4().hex}"
            self.expression_attribute_names[expression_attribute_name] = root_name
            return f"{expression_attribute_name}{index_str}"

        # TODO: Dynamo supports dots in attribute names - kwargs flagging is required if we want to support this
        if "." in path:
            # Handle nesting
            for index, object_name in enumerate(path.split(".")):
                if index != 0:
                    full_expression_attribute_name += "."
                full_expression_attribute_name += __set_name_and_expression(object_name)
        else:
            full_expression_attribute_name += __set_name_and_expression(path)
        return full_expression_attribute_name

    # TODO: Handle nested attribute names on Maps and Lists - current they get added as raw names
    def set_expression_attribute_value(self, value: DynamoValue) -> str:
        """Add a Dynamo value to the expression attribute values, and return the unique expression attribute value

        Args:
            value (DynamoValue): The value to add to the expression attribute values

        Returns:
            (str) A unique expression attribute value
        """
        expression_attribute_value = f":{uuid4().hex}"
        self.expression_attribute_values[expression_attribute_value] = value
        return expression_attribute_value

    def merge_expression_attributes(self, *,
                                    expression_attribute_names: DynamoExpressionAttributesNamesObject = None,
                                    expression_attribute_values: DynamoExpressionAttributesValuesObject = None
                                    ):
        """Merge the given expression attribute names and values

        Args:
            expression_attribute_names (DynamoExpressionAttributesNamesObject): Names object to merge
            expression_attribute_values (DynamoExpressionAttributesValuesObject): Values object to merge
        """
        if expression_attribute_names:
            self.expression_attribute_names = {
                **self.expression_attribute_names,
                **expression_attribute_names,
            }
        if expression_attribute_values:
            self.expression_attribute_values = {
                **self.expression_attribute_values,
                **expression_attribute_values,
            }
