"""
Update Expression Factory

references:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.UpdateExpressions.html

Multiple types of updates can be included in one expression, as long as all expressions of that type follow the
keyword for that update type.

E.g.
SET #name = :val, #name2 = :val2 REMOVE #name3, #name4 DELETE #name5 :val3, #name6 :val4
"""
from enum import Enum
from typing import Any, NamedTuple

from ckf_api_toolkit.aws_dynamo.constants import DynamoScalarSetDataType
from ckf_api_toolkit.aws_dynamo.expression_attributes import ExpressionAttributes
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.tools.general_error import GeneralError


"""
Constants
============================
"""


class DynamoUpdateTypeKeyword(Enum):
    """Enum representing the types of update actions that can be taken"""
    ADD = "ADD"  # NOTE: Not recommended, and therefore not currently implemented - Use SET
    DELETE = "DELETE"  # Only for Set data types - removes elements
    SET = "SET"  # Set an attribute to a value or another attribute's value
    REMOVE = "REMOVE"  # Remove item attribute, or remove property from Map


class DynamoUpdateSetFunction(Enum):
    """Enum representing the functions for set updates"""
    LIST_APPEND = "list_append"
    IF_NOT_EXISTS = "if_not_exists"


class DynamoUpdateSetOperator(Enum):
    """Enum representing the operators for set updates"""
    EQ = "="
    ADD = "+"
    SUB = "-"


'''
============================
Helper functions
============================
'''


def _get_safe_string(string: str) -> str:
    """Return the ends-trimmed string with single whitespace removed

    Args:
        string (str): The string to be cleaned

    Returns:
        (str) The cleaned string
    """
    # Only single whitespace and trimmed
    return " ".join(f"{string}".split())


'''
============================
Set value class
============================
Per reference:

- The path element is the document path to the item.
- An operand element can be either a document path to an item or a function.

set-action ::=
    path = value

value ::=
    operand 
    | operand '+' operand 
    | operand '-' operand
 
operand ::=
    path | function
'''


class InvalidModificationToDynamoUpdateExpressionSetActionValue(GeneralError):
    """Error representing 'Attempt to modify set action value was not valid.'"""
    def __init__(self):
        super().__init__("Attempt to modify set action value was not valid.")


class DynamoUpdateExpressionSetActionValueObject(NamedTuple):
    """Object for expression attributes and operand expression to set value action"""
    expression_attributes: ExpressionAttributes
    operand_expression: str


class DynamoUpdateExpressionSetActionValueFactory:
    """Factory class to create the update expression for a set action value

    Attributes:
        expression_attributes (ExpressionAttributes):
        __operand_expression (str): The operand expression to use
        __modified (bool): Internal flag to set when the object has been modified
    """
    expression_attributes: ExpressionAttributes
    __operand_expression: str
    __modified: bool

    def __init__(self):
        """Inits DynamoUpdateExpressionSetActionValueFactory with empty expression_attributes"""
        self.expression_attributes = ExpressionAttributes()
        self.__operand_expression = ""
        self.__modified = False

    @property
    def operand_expression(self):
        """Return the cleaned operand expression"""
        return _get_safe_string(self.__operand_expression)

    def get_set_action_value_object(self) -> DynamoUpdateExpressionSetActionValueObject:
        """Return the set-action-value object

        Returns:
            (DynamoUpdateExpressionSetActionValueObject) The set-action-value object
        """
        return DynamoUpdateExpressionSetActionValueObject(
            expression_attributes=self.expression_attributes,
            operand_expression=self.operand_expression,
        )

    def __error_if_modified(self):
        """Raise an error if this object has been modified"""
        if self.__modified:
            raise InvalidModificationToDynamoUpdateExpressionSetActionValue()

    def __set_modified(self):
        """Set the internal modified flag"""
        self.__modified = True

    def set_to_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        """Convert a given value to a DynamoDB-compatible dict

        Args:
            value (Any): The value to convert to Dynamo
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        self.__error_if_modified()
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        self.__operand_expression = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__set_modified()

    def __merge_expression_attributes(self, value: DynamoUpdateExpressionSetActionValueObject):
        """Merge the expression attributes from the given object

        Args:
            value (DynamoUpdateExpressionSetActionValueObject): The object to merge attributes from
        """
        self.expression_attributes.merge_expression_attributes(**vars(value.expression_attributes))

    def set_if_not_exists(self, path: str, value: DynamoUpdateExpressionSetActionValueObject):
        """Create the operand expression to check if the set exists

        Args:
            path (str):
            value (DynamoUpdateExpressionSetActionValueObject):
        """
        self.__error_if_modified()
        self.__merge_expression_attributes(value)
        exp_attr_str = self.expression_attributes.set_expression_attribute_name(path)
        self.__operand_expression = (
            f"{DynamoUpdateSetFunction.IF_NOT_EXISTS.value}({exp_attr_str}, {value.operand_expression})"
        )
        self.__set_modified()

    def set_list_append(self,
                        list_appended_to: DynamoUpdateExpressionSetActionValueObject,
                        list_to_append: DynamoUpdateExpressionSetActionValueObject,
                        ):
        """Create the operand expression to append the second list to the first

        Args:
            list_appended_to (DynamoUpdateExpressionSetActionValueObject): The Dynamo set to be appended to
            list_to_append (DynamoUpdateExpressionSetActionValueObject): The Dynamo set to append
        """
        self.__error_if_modified()
        self.__merge_expression_attributes(list_appended_to)
        self.__merge_expression_attributes(list_to_append)
        self.__operand_expression = (
            f"{DynamoUpdateSetFunction.LIST_APPEND.value}({list_appended_to}, {list_to_append})"
        )
        self.__set_modified()

    def __arithmetic_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject,
                                         operator: DynamoUpdateSetOperator):
        """Perform an arithmetic operation using the given operator and value

        Args:
            value (DynamoUpdateExpressionSetActionValueObject): The value to use in the operation
            operator (DynamoUpdateSetOperator): The operator to use in the operation
        """
        self.__merge_expression_attributes(value)
        self.__operand_expression += f" {operator.value} {value.operand_expression}"
        self.__set_modified()

    def add_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject):
        """Add by arithmetic operation using the given operator and value

        Args:
            value (DynamoUpdateExpressionSetActionValueObject): The value to add via the expression
        """
        self.__arithmetic_by_expression_value(value, DynamoUpdateSetOperator.ADD)

    def subtract_by_expression_value(self, value: DynamoUpdateExpressionSetActionValueObject):
        """Subtract by arithmetic operation using the given operator and value

        Args:
            value (DynamoUpdateExpressionSetActionValueObject): The value to subtract via the expression
        """
        self.__arithmetic_by_expression_value(value, DynamoUpdateSetOperator.SUB)

    def __arithmetic_by_python_value(self, value: Any, operator: DynamoUpdateSetOperator, *,
                                     dynamo_set_type: DynamoScalarSetDataType = None):
        """Perform an arithmetic operation using the given operator and Python value

        Args:
            value (Any): The Python value to use in the operation
            operator (DynamoUpdateSetOperator): The operator to use in the operation
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        exp_attr_value = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__operand_expression += f" {operator.value} {exp_attr_value}"
        self.__set_modified()

    def add_by_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        """Add by arithmetic operation using the given operator and Python value

        Args:
            value (Any): The Python value to add via the expression
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        self.__arithmetic_by_python_value(value, DynamoUpdateSetOperator.ADD, dynamo_set_type=dynamo_set_type)

    def subtract_by_python_value(self, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        """Subtract by arithmetic operation using the given operator and Python value

        Args:
            value (Any): The Python value to subtract via the expression
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        self.__arithmetic_by_python_value(value, DynamoUpdateSetOperator.SUB, dynamo_set_type=dynamo_set_type)


'''
============================
Update expression class
============================
'''


class DynamoUpdateExpressionFactory:
    """Factory class to create an update expression

    Attributes:
        __current_set_expression (str): The current set expression for this object
        __current_delete_expression (str): The current delete expression for this object
        __current_remove_expression (str): The current remove expression for this object
        expression_attributes (ExpressionAttributes): The expression attributes for this object
    """
    __current_set_expression: str
    __current_delete_expression: str
    __current_remove_expression: str
    expression_attributes: ExpressionAttributes

    def __init__(self):
        """Inits DynamoUpdateExpressionFactory with empty ExpressionAttributes"""
        self.__current_delete_expression = ""
        self.__current_set_expression = ""
        self.__current_remove_expression = ""
        self.expression_attributes = ExpressionAttributes()

    @property
    def update_expression(self):
        """Return the cleaned update expression"""
        return _get_safe_string(
            f"{self.__current_set_expression} {self.__current_delete_expression} {self.__current_remove_expression}"
        )

    def add_set_expression(self, path: str, value_obj: DynamoUpdateExpressionSetActionValueObject):
        """Add a set expression to this object

        Args:
            path (str): The path to the object in the expression
            value_obj (DynamoUpdateExpressionSetActionValueObject): The value object to add to the expression
        """
        self.expression_attributes.merge_expression_attributes(**vars(value_obj.expression_attributes))
        path_exp_attr_str = self.expression_attributes.set_expression_attribute_name(path)
        if not self.__current_set_expression:
            self.__current_set_expression = f"{DynamoUpdateTypeKeyword.SET.value} "
        else:
            self.__current_set_expression += ", "
        self.__current_set_expression += (
            f"{path_exp_attr_str} {DynamoUpdateSetOperator.EQ.value} {value_obj.operand_expression}"
        )

    def set_path_to_python_value(self, path: str, value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None):
        """Set the given document path to the given value

        Args:
            path (str): The document path for the set
            value (Any): The value to use in the operation
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        set_action_value_obj = DynamoUpdateExpressionSetActionValueFactory()
        set_action_value_obj.set_to_python_value(value, dynamo_set_type=dynamo_set_type)
        self.add_set_expression(path, set_action_value_obj.get_set_action_value_object())

    def remove_path(self, path: str):
        """Add the given path to the current remove expression

        Args:
            path (str): The path to remove
        """
        if not self.__current_remove_expression:
            self.__current_remove_expression = f"{DynamoUpdateTypeKeyword.REMOVE.value} "
        else:
            self.__current_remove_expression += ", "
        self.__current_remove_expression += self.expression_attributes.set_expression_attribute_name(path)

    def __delete_from_set(self, path: str, value: Any, dynamo_set_type: DynamoScalarSetDataType = None):
        """Delete the document at the given path

        Args:
            path (str): The document path for the set
            value (Any): The value to check against in the expression
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        if not self.__current_delete_expression:
            self.__current_delete_expression = f"{DynamoUpdateTypeKeyword.DELETE.value} "
        else:
            self.__current_delete_expression += ", "
        exp_attr_name_str = self.expression_attributes.set_expression_attribute_name(path)
        dynamo_value = convert_python_data_to_dynamo(value, dynamo_set_type=dynamo_set_type)
        exp_attr_value_str = self.expression_attributes.set_expression_attribute_value(dynamo_value)
        self.__current_delete_expression += f"{exp_attr_name_str} {exp_attr_value_str}"

    def delete_set_from_set(self, path: str, set_to_delete: set, dynamo_set_type: DynamoScalarSetDataType):
        """Delete the given set from the document set at the path indicated

        Args:
            path (str): The document path for the set
            set_to_delete (set): The set to delete with this expression
            dynamo_set_type (DynamoScalarSetDataType): Optional Dynamo set type to convert to
        """
        self.__delete_from_set(path, set_to_delete, dynamo_set_type)

    def delete_python_value_from_set(self, path: str, value: Any):
        """Delete the given Python value from the document set at the path indicated

        Args:
            path (str): The document path for the set
            value (str): The Python value to delete
        """
        self.__delete_from_set(path, value)
