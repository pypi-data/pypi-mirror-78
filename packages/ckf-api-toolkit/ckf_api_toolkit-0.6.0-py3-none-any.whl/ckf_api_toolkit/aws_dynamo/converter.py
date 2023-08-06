from typing import Any, List, Union

from ckf_api_toolkit.aws_dynamo.constants import DynamoScalarBoolDataType, DynamoScalarStringDataType, \
    DynamoScalarSetDataType, DynamoMapDataType, DynamoListDataType, DynamoValue, DynamoScalarStringValue, \
    DynamoListValue, DynamoMapValue, DynamoBase64DataType, DynamoDataType, DynamoStreamAttributeValueMap
from ckf_api_toolkit.tools.general_error import GeneralError

'''
Automatic Dynamo/Python Data Conversion
===========================================================
Python to Dynamo
============================
'''


class UnspecifiedDynamoSetType(GeneralError):
    def __init__(self, value: set):
        super().__init__(f"Python set: {value} was provided for conversion without specifying a valid Dynamo Set type.")


class InvalidNumericValue(GeneralError):
    def __init__(self, value: Any):
        super().__init__(f"Python value: {value} was passed as Dynamo numeric type, but is not numeric.")


class InvalidBase64Value(GeneralError):
    def __init__(self, value: Any):
        super().__init__(f"Python value: {value} was passed as Dynamo Base64 data, but is not bytes type.")


class UnsupportedPythonType(GeneralError):
    def __init__(self, value: Any):
        super().__init__(f"Python type: {type(value)} is not supported. Convert to supported value.")


def __is_number(data: Any) -> bool:
    data_str = str(data)
    if not data_str.isnumeric():
        try:
            float(data_str)
        except ValueError:
            return False
    return True


def convert_python_data_to_dynamo(value: Any, *, dynamo_set_type: DynamoScalarSetDataType = None) -> DynamoValue:
    # Python NoneType to Dynamo NULL
    if value is None:
        return {DynamoScalarBoolDataType.NULL.value: True}
    else:
        value_type = type(value)

    # Scalar string
    if value_type is str:
        return {DynamoScalarStringDataType.STRING.value: value} if value \
            else {DynamoScalarBoolDataType.NULL.value: True}

    # Boolean
    elif value_type is bool:
        return {DynamoScalarBoolDataType.BOOL.value: value}

    # Numeric types
    elif value_type in [int, float]:
        return {DynamoScalarStringDataType.NUMBER.value: str(value)}

    # Python set to Dynamo typed set or cast a Python list to a Dynamo typed set
    elif value_type is set or (value_type is list and dynamo_set_type is not None):
        if dynamo_set_type is None:
            raise UnspecifiedDynamoSetType(value)

        return_value: List[Union[str, bytes]] = []
        if dynamo_set_type is DynamoScalarSetDataType.NUMBER_SET:
            for data in value:
                if not __is_number(data):
                    raise InvalidNumericValue(value)
                return_value.append(str(data))

        elif dynamo_set_type is DynamoScalarSetDataType.BASE64_SET:
            for data in value:
                if type(data) is not bytes:
                    raise InvalidBase64Value(value)
                return_value.append(data)

        else:
            return_value = list(value)

        return {dynamo_set_type.value: return_value}

    # Python bytes to Dynamo Base64
    elif value_type is bytes:
        return {DynamoBase64DataType.BASE64.value: value}

    # Lists
    elif value_type is list:
        value_list: list = value
        return_list = []
        for list_object in value_list:
            return_list.append(convert_python_data_to_dynamo(list_object))

        return {DynamoListDataType.LIST.value: return_list}

    # Python dict to Dynamo Map
    # NOTE: If a dictionary contains sets, they will be cast into lists
    elif value_type is dict:
        value_dict: dict = value
        return_map = {}
        for object_key, object_value in value_dict.items():
            if object_value is set:
                object_value = list(object_value)
            return_map[str(object_key)] = convert_python_data_to_dynamo(object_value)
        return {DynamoMapDataType.MAP.value: return_map}

    else:
        raise UnsupportedPythonType(value)


'''
============================
Dynamo to Python
============================
'''


def __get_number_from_string(number_string: str):
    try:
        number = int(number_string)
        return number
    except ValueError:
        return float(number_string)


def __init_set_conversion(dynamo_value: DynamoValue, set_data_type: DynamoDataType):
    return dynamo_value[set_data_type.value], set()


def convert_dynamo_data_to_python(dynamo_value: DynamoValue):
    dynamo_type = DynamoDataType(list(dynamo_value.keys())[0])

    # Recursively handle Map type
    if dynamo_type is DynamoDataType.MAP:
        dynamo_value: DynamoMapValue = dynamo_value
        untyped_dict: dict = dynamo_value[DynamoDataType.MAP.value]
        for key, value in untyped_dict.items():
            untyped_dict[key] = convert_dynamo_data_to_python(value)
        return untyped_dict

    # Convert Number from string to int or float
    elif dynamo_type is DynamoDataType.NUMBER:
        dynamo_value: DynamoScalarStringValue = dynamo_value
        number_string: str = dynamo_value[DynamoDataType.NUMBER.value]
        return __get_number_from_string(number_string)

    # Convert Dynamo Bool to Python
    elif dynamo_type is DynamoDataType.BOOL:
        # NOTE: Actual Python bool being returned instead of string, so we can just return that value
        # bool_string = dynamo_value[DynamoDataType.BOOL.value]
        # if bool_string is DynamoBoolStrings.TRUE.value:
        #     return True
        # else:
        #     return False
        return dynamo_value[DynamoDataType.BOOL.value]

    # Convert from NULL to None
    elif dynamo_type is DynamoDataType.NULL:
        return None

    # Convert List recursively
    elif dynamo_type is DynamoDataType.LIST:
        dynamo_value: DynamoListValue = dynamo_value
        dynamo_list = dynamo_value[DynamoDataType.LIST.value]
        python_list = list()
        for list_dynamo_value in dynamo_list:
            python_list.append(convert_dynamo_data_to_python(list_dynamo_value))
        return python_list

    # Convert Number Set
    elif dynamo_type is DynamoDataType.NUMBER_SET:
        number_set, python_set = __init_set_conversion(dynamo_value, DynamoDataType.NUMBER_SET)
        for dynamo_number_string in number_set:
            python_set.add(__get_number_from_string(dynamo_number_string))
        return python_set

    # Convert String Set
    elif dynamo_type is DynamoDataType.STRING_SET:
        string_set, python_set = __init_set_conversion(dynamo_value, DynamoDataType.STRING_SET)
        for string in string_set:
            python_set.add(string)
        return python_set

    # Convert Base64 Set
    elif dynamo_type is DynamoDataType.BASE64_SET:
        base64_set, python_set = __init_set_conversion(dynamo_value, DynamoDataType.BASE64_SET)
        for base64_string in base64_set:
            python_set.add(str(base64_string).encode('utf-8'))
        return python_set

    # Return everything else as string
    else:
        return dynamo_value[dynamo_type.value]


'''
Automatic Dynamo Stream Data to Python Data Conversion
===========================================================
'''


def convert_dynamo_stream_item_to_python(attribute_value_map: DynamoStreamAttributeValueMap) -> dict:
    return {key: convert_dynamo_data_to_python(value) for key, value in attribute_value_map.items()}
