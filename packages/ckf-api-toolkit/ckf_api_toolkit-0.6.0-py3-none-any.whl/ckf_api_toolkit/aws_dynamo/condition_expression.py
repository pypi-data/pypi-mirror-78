"""
Condition Expression Factory

References:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.OperatorsAndFunctions.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html
"""
from enum import Enum
from typing import NewType, NamedTuple, Union, List, Any

from ckf_api_toolkit.aws_dynamo.constants import DynamoValue, DynamoScalarStringDataType, DynamoDataType
from ckf_api_toolkit.aws_dynamo.converter import convert_python_data_to_dynamo
from ckf_api_toolkit.aws_dynamo.expression_attributes import ExpressionAttributes
from ckf_api_toolkit.tools.general_error import GeneralError


class DynamoConditionExpressionFunction(Enum):
    """
    Enum to wrap Condition Expression Functions
    """
    ATTRIBUTE_EXISTS = "attribute_exists"
    ATTRIBUTE_NOT_EXISTS = "attribute_not_exists"
    ATTRIBUTE_TYPE = "attribute_type"
    BEGINS_WITH = "begins_with"
    CONTAINS = "contains"
    SIZE = "size"


class DynamoConditionExpressionComparisonComparator(Enum):
    """
    Enum to wrap Condition Expression Comparison Comparators
    """
    EQ = "="
    NOT_EQ = "<>"
    LT = "<"
    LTE = "<="
    GT = ">"
    GTE = ">="


class DynamoConditionExpressionComparisonKeyword(Enum):
    """
    Enum to wrap Condition Expression Comparison Keywords
    """
    BETWEEN = "BETWEEN"
    IN = "IN"


class DynamoConditionExpressionLogicalOperator(Enum):
    """
    Enum to wrap Condition Expression Comparison Operators
    """
    AND = "AND"
    OR = "OR"
    NOT = "NOT"


AttributeNameOperand = NewType("AttributeNameOperand", str)
AttributeValueOperand = NewType("AttributeValueOperand", DynamoValue)


class ConditionOperandType(Enum):
    """
    Enum to wrap Condition Expression Comparison Comparator
    """
    NAME = 'name'
    VALUE = 'value'


class ConditionOperand(NamedTuple):
    """
    Represents the type and value of a Condition Operand
    """
    type: ConditionOperandType
    value: Union[AttributeValueOperand, AttributeNameOperand]


class ConditionExpressionObject(NamedTuple):
    """
    Represents the ConditionExpression object
    """
    ConditionExpression: str


class DynamoConditionExpressionEmptyOperandList(GeneralError):
    """
    An empty operand list was used to create an IN ConditionExpression
    """
    def __init__(self):
        super().__init__(f"An empty operand list was used to create an IN ConditionExpression")


class DynamoConditionExpressionFactory:
    """
    Factory class to create Condition Expressions. Note in DynamoDB operands can be either names or values, i.e.
    attributeName != 5 requires a name for the first operand, and a value for the second one.

    Attributes:
        expression_attributes (ExpressionAttributes): The name/value attributes to be used for this expression
        condition_expression (str): The condition expression to build
    """
    expression_attributes: ExpressionAttributes
    condition_expression: str

    def __init__(self):
        """Init DynamoConditionExpressionFactory with empty values"""
        self.expression_attributes = ExpressionAttributes()
        self.condition_expression = ""

    @staticmethod
    def get_value_operand(value: Any) -> ConditionOperand:
        """Create and return a ConditionOperand

        Args:
            value (Any): The value to create the ConditionOperand with

        Returns:
            (ConditionOperand) A ConditionOperand created with the `value` specified
        """
        return ConditionOperand(ConditionOperandType.VALUE, AttributeValueOperand(convert_python_data_to_dynamo(value)))

    @staticmethod
    def get_name_operand(name: str) -> ConditionOperand:
        """Create and return a ConditionOperand

        Args:
            name (str): The name to create the ConditionOperand with

        Returns:
            (ConditionOperand) A ConditionOperand created with the `name` specified
        """
        return ConditionOperand(ConditionOperandType.NAME, AttributeNameOperand(name))

    def __add_to_condition_expression(self, new_expression: str):
        """Add an expression to the ConditionExpression

        Args:
            new_expression (str): The new expression to add
        """
        self.condition_expression += f" {new_expression}"
        self.condition_expression = self.condition_expression.strip()

    def __set_operand_to_expression_attributes(self, operand: ConditionOperand) -> str:
        """Set the expression attribute according to whether the operand is a name or value

        Args:
            operand (ConditionOperand): The operand to set

        Returns:
            (str) The full expression attribute name
        """
        if operand.type == ConditionOperandType.NAME:
            return self.expression_attributes.set_expression_attribute_name(operand.value)
        elif operand.type == ConditionOperandType.VALUE:
            return self.expression_attributes.set_expression_attribute_value(operand.value)

    def add_string(self, expression: str):
        """Add a string to the expression

        Args:
            expression (str): The expression to add to
        """
        self.__add_to_condition_expression(expression)

    def add_comparison(
            self, operand1: ConditionOperand, comparator: DynamoConditionExpressionComparisonComparator,
            operand2: ConditionOperand
    ):
        """Add a comparison to the ConditionExpression

        Args:
            operand1 (ConditionOperand): First operand
            comparator (DynamoConditionExpressionComparisonComparator): The comparator to use
            operand2 (ConditionOperand): Second operand
        """
        operand1_expression_string = self.__set_operand_to_expression_attributes(operand1)
        operand2_expression_string = self.__set_operand_to_expression_attributes(operand2)
        self.__add_to_condition_expression(
            f"{operand1_expression_string} {comparator.value} {operand2_expression_string}"
        )

    def add_between(
            self, between_operand: ConditionOperand, lower_operand: ConditionOperand, upper_operand: ConditionOperand
    ):
        """Add a range to the ConditionExpression

        Args:
            between_operand (ConditionOperand): Operand representing "between"
            lower_operand (ConditionOperand): The lower bound operand
            upper_operand (ConditionOperand): The upper bound operand
        """
        between_operand_expression_string = self.__set_operand_to_expression_attributes(between_operand)
        lower_operand_expression_string = self.__set_operand_to_expression_attributes(lower_operand)
        upper_operand_expression_string = self.__set_operand_to_expression_attributes(upper_operand)
        self.__add_to_condition_expression(
            f"{between_operand_expression_string} {DynamoConditionExpressionComparisonKeyword.BETWEEN.value} "
            f"{lower_operand_expression_string} {DynamoConditionExpressionLogicalOperator.AND.value} "
            f"{upper_operand_expression_string}"
        )

    def add_in(self, operand: ConditionOperand, in_list: List[ConditionOperand]):
        """Add an inclusion list to the ConditionExpression

        Args:
            operand (ConditionOperand): Operand representing "in"
            in_list (List[ConditionOperand]): List of values to check for inclusion in
        """
        if len(in_list) < 1:
            raise DynamoConditionExpressionEmptyOperandList()
        operand_expression_string = self.__set_operand_to_expression_attributes(operand)
        in_expression_string = " ("
        for current_operand in in_list:
            current_operand_expression_string = self.__set_operand_to_expression_attributes(current_operand)
            in_expression_string += f"{current_operand_expression_string}, "
        self.__add_to_condition_expression(
            f"{operand_expression_string} {DynamoConditionExpressionComparisonKeyword.IN.value} "
            f"{in_expression_string[:-2]})"
        )

    def add_expression_in_parenthesis(
            self, expression: str, expression_attributes: ExpressionAttributes = ExpressionAttributes()
    ):
        """Add a parenthetical expression to the ConditionExpression

        Args:
            expression (str): The expression to add in parenthesis
            expression_attributes (ExpressionAttributes): The expression attributes to use
        """
        self.expression_attributes.merge_expression_attributes(**vars(expression_attributes))
        self.__add_to_condition_expression(f"({expression})")

    def __parse_condition(self, condition: Union[str, 'DynamoConditionExpressionFactory']) -> str:
        """Parse the given condition to return its expression
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to parse

        Returns:
            (str) The condition expression
        """
        if isinstance(condition, DynamoConditionExpressionFactory):
            self.expression_attributes.merge_expression_attributes(
                expression_attribute_names=condition.expression_attributes.expression_attribute_names,
                expression_attribute_values=condition.expression_attributes.expression_attribute_values,
            )
            return condition.condition_expression
        else:
            return condition

    def __add_logical(self, *,
                      condition_1: Union[str, 'DynamoConditionExpressionFactory'] = "",
                      operator: DynamoConditionExpressionLogicalOperator,
                      condition_2: Union[str, 'DynamoConditionExpressionFactory']
                      ):
        """Add a logical statement to the ConditionExpression

        Args:
            condition_1 (Union[str, DynamoConditionExpressionFactory]): The first condition
            operator (DynamoConditionExpressionLogicalOperator): The logical operator to use
            condition_2 (Union[str, DynamoConditionExpressionFactory]): The second condition
        """
        condition_1_str = self.__parse_condition(condition_1)
        condition_2_str = self.__parse_condition(condition_2)
        self.__add_to_condition_expression(f"({condition_1_str}) {operator.value} ({condition_2_str})")

    def __append_logical(self, *, operator: DynamoConditionExpressionLogicalOperator,
                         condition: Union[str, 'DynamoConditionExpressionFactory']):
        """Append a logical condition to the ConditionExpression

        Args:
            operator (DynamoConditionExpressionLogicalOperator): The logical operator to use
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to add
        """
        condition_str = self.__parse_condition(condition)
        self.__add_to_condition_expression(f" {operator.value} ({condition_str})")

    def add_logical_and(self, condition_1: Union[str, 'DynamoConditionExpressionFactory'],
                        condition_2: Union[str, 'DynamoConditionExpressionFactory']):
        """Add a logical AND to the ConditionExpression

        Args:
            condition_1 (Union[str, DynamoConditionExpressionFactory]): The first condition
            condition_2(Union[str, DynamoConditionExpressionFactory]): The second condition
        """
        self.__add_logical(
            condition_1=condition_1, operator=DynamoConditionExpressionLogicalOperator.AND, condition_2=condition_2
        )

    def add_logical_or(self, condition_1: Union[str, 'DynamoConditionExpressionFactory'],
                       condition_2: Union[str, 'DynamoConditionExpressionFactory']):
        """Add a logical OR to the ConditionExpression

        Args:
            condition_1 (Union[str, DynamoConditionExpressionFactory]): The first condition
            condition_2 (Union[str, DynamoConditionExpressionFactory]): The second condition
        """
        self.__add_logical(
            condition_1=condition_1, operator=DynamoConditionExpressionLogicalOperator.OR, condition_2=condition_2
        )

    def add_logical_not(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        """Add a logical NOT to the ConditionExpression

        Args:
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to add
        """
        self.__add_logical(condition_2=condition, operator=DynamoConditionExpressionLogicalOperator.NOT)

    def append_logical_and(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        """Append a logical AND to the ConditionExpression

        Args:
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to append
        """
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.AND, condition=condition)

    def append_logical_or(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        """Append a logical OR to the ConditionExpression

        Args:
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to append
        """
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.OR, condition=condition)

    def append_logical_not(self, condition: Union[str, 'DynamoConditionExpressionFactory']):
        """Append a logical NOT to the ConditionExpression

        Args:
            condition (Union[str, DynamoConditionExpressionFactory]): The condition to append
        """
        self.__append_logical(operator=DynamoConditionExpressionLogicalOperator.NOT, condition=condition)

    def __add_path_only_function(self, *, path_name: str, function: DynamoConditionExpressionFunction):
        """Add a path only function to the ConditionExpression

        Args:
            path_name (str): Name of the path
            function (DynamoConditionExpressionFunction): Function to add
        """
        path_expression_attribute_name = self.expression_attributes.set_expression_attribute_name(path_name)
        self.__add_to_condition_expression(f"{function.value}({path_expression_attribute_name})")

    def add_attribute_exists(self, attribute_path: str):
        """Add a check that an attribute exists in the ConditionExpression

        Args:
            attribute_path (str): The path of the attribute
        """
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.ATTRIBUTE_EXISTS)

    def add_attribute_not_exists(self, attribute_path: str):
        """Add a check that an attribute does not exist in the ConditionExpression

        Args:
            attribute_path (str): The path of the attribute
        """
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.ATTRIBUTE_NOT_EXISTS)

    def add_size(self, attribute_path: str):
        """Add a check for the size of an attribute in the ConditionExpression

        Args:
            attribute_path (str): The path of the attribute
        """
        self.__add_path_only_function(path_name=attribute_path,
                                      function=DynamoConditionExpressionFunction.SIZE)

    def __add_function_with_string_arg(self, *,
                                       attribute_path: str, function: DynamoConditionExpressionFunction, arg_str: str
                                       ):
        """Add a function with a string argument to the ConditionExpression

        Args:
            attribute_path (str): Path of the attribute
            function (DynamoConditionExpressionFunction): Function to add
            arg_str (str): The function's argument string
        """
        path_expression_attribute_name = self.expression_attributes.set_expression_attribute_name(attribute_path)
        arg_str_scalar_string_value = {DynamoScalarStringDataType.STRING.value: arg_str}
        arg_str_expression_attribute_value = self.expression_attributes.set_expression_attribute_value(
            arg_str_scalar_string_value
        )
        self.__add_to_condition_expression(
            f"{function.value}({path_expression_attribute_name}, {arg_str_expression_attribute_value})"
        )

    def add_attribute_type(self, attribute_path: str, data_type: DynamoDataType):
        """Add the data type of an attribute

        Args:
            attribute_path (str): Path of the attribute
            data_type (DynamoDataType): Data type of the attribute
        """
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.ATTRIBUTE_TYPE,
            arg_str=data_type.value
        )

    def add_begins_with(self, attribute_path: str, substring: str):
        """Add a "begins with" check to the ConditionExpression

        Args:
            attribute_path (str): Path of the attribute
            substring (str): substring to check for
        """
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.BEGINS_WITH, arg_str=substring
        )

    def add_contains(self, attribute_path: str, operand: str):
        """Add a "contains" check to the ConditionExpression

        Args:
            attribute_path (str): Path of the attribute
            operand (str): Operand to check for
        """
        self.__add_function_with_string_arg(
            attribute_path=attribute_path, function=DynamoConditionExpressionFunction.CONTAINS, arg_str=operand
        )
