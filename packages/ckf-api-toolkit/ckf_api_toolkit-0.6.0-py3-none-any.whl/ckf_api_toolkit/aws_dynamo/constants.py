"""
DynamoDB Constants

Boto3 v1.9.232 Reference:
https://boto3.amazonaws.com/v1/documentation/api/1.9.232/reference/services/dynamodb.html
"""
from enum import Enum
from typing import Any, Dict, Union, List, NamedTuple

"""
Data Type constants
"""


class DynamoDataType(Enum):
    """Enum representing DynamoDB Data Types"""
    NULL = "NULL"
    BOOL = "BOOL"
    STRING = "S"
    NUMBER = "N"
    BASE64 = "B"
    STRING_SET = "SS"
    NUMBER_SET = "NS"
    BASE64_SET = "BS"
    MAP = "M"
    LIST = "L"


class DynamoScalarBoolDataType(Enum):
    """Enum representing DynamoDB Scalar Bool Data Type"""
    NULL = DynamoDataType.NULL.value
    BOOL = DynamoDataType.BOOL.value


class DynamoScalarStringDataType(Enum):
    """Enum representing DynamoDB Scalar String Data Type"""
    STRING = DynamoDataType.STRING.value
    NUMBER = DynamoDataType.NUMBER.value


class DynamoBase64DataType(Enum):
    """Enum representing DynamoDB Base64 Data Type"""
    BASE64 = DynamoDataType.BASE64.value


class DynamoScalarSetDataType(Enum):
    """Enum representing DynamoDB Scalar Set Data Type"""
    STRING_SET = DynamoDataType.STRING_SET.value
    NUMBER_SET = DynamoDataType.NUMBER_SET.value
    BASE64_SET = DynamoDataType.BASE64_SET.value


class DynamoMapDataType(Enum):
    """Enum representing DynamoDB Map Data Type"""
    MAP = DynamoDataType.MAP.value


class DynamoListDataType(Enum):
    """Enum representing DynamoDB List Data Type"""
    LIST = DynamoDataType.LIST.value


# NOTE: It appears that these get returned as Python bool instead of str
class DynamoBoolStrings(Enum):
    """Enum representing DynamoDB Bool Strings"""
    TRUE = "true"
    FALSE = "false"


'''
Value constants
'''

DynamoScalarStringValue = Dict[str, str]
DynamoBase64Value = Dict[str, bytes]
DynamoScalarSetValue = Dict[str, List[str]]
DynamoScalarBoolValue = Dict[str, bool]
'''
Since Lists and Maps can recursively contains themselves and each other, a generic type check is required.
NewType does not support Union or recursive type checking.
'''
DynamoListValue = Dict[str, List[Any]]
DynamoMapValue = Dict[str, Any]

DynamoValue = Union[
    DynamoScalarStringValue,
    DynamoBase64Value,
    DynamoScalarSetValue,
    DynamoScalarBoolValue,
    DynamoListValue,
    DynamoMapValue,
]

'''
Attribute constants
'''

DynamoAttribute = Dict[str, DynamoValue]

'''
Return Values constants
'''


class DynamoReturnValues(Enum):
    """Enum representing possible DynamoDB return values"""
    NONE = "NONE"
    ALL_OLD = "ALL_OLD"
    UPDATED_OLD = "UPDATED_OLD"
    ALL_NEW = "ALL_NEW"
    UPDATED_NEW = "UPDATED_NEW"


'''
Stream constants
'''


class DynamoStreamEventAttributes(Enum):
    """Enum representing DynamoDB Stream event attributes"""
    Records = "Records"


class DynamoRecord(NamedTuple):
    """NamedTuple representing DynamoDB record"""
    awsRegion: str = None
    eventID: str = None
    eventName: str = None
    eventSource: str = None
    eventSourceARN: str = None
    eventVersion: str = None
    # TODO: model as per docs
    #  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_Identity.html
    dynamodb: dict = None
    userIdentity: dict = None


# TODO: Implement full definition
#  https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_streams_StreamRecord.html
class DynamoStreamRecordAttributes(Enum):
    """Enum representing DynamoDB Stream record attributes"""
    NewImage = "NewImage"
    OldImage = "OldImage"


DynamoStreamAttributeValueMap = Dict[str, DynamoValue]

DynamoStreamRecord = Dict[DynamoStreamRecordAttributes, DynamoStreamAttributeValueMap]


class DynamoStreamEventName(Enum):
    """Enum representing DynamoDB Stream event name"""
    INSERT = "INSERT"
    MODIFY = "MODIFY"
    REMOVE = "REMOVE"


'''
Responses
'''


class DynamoItemResponse(NamedTuple):
    """NamedTuple representing DynamoDB item response"""
    Item: Dict[str, DynamoValue]
    ResponseMetadata: dict = None


class DynamoItemsResponse(NamedTuple):
    """NamedTuple representing DynamoDB items response"""
    Items: List[Dict[str, DynamoValue]]
    LastEvaluatedKey: str = None
    Count: int = None
    ResponseMetadata: dict = None
    ScannedCount: int = None


class DynamoAttributesResponse(NamedTuple):
    """NamedTuple representing DynamoDB attributes response"""
    ResponseMetadata: dict = None
    Attributes: Dict[str, DynamoValue] = None


'''
Payload Constants
'''


class DynamoPayloadSelect(Enum):
    """Enum representing DynamoDB payload selection"""
    # TODO: Implement 'Select' on payload
    ALL_ATTRIBUTES = 'ALL_ATTRIBUTES'
    ALL_PROJECTED_ATTRIBUTES = 'ALL_PROJECTED_ATTRIBUTES'
    SPECIFIC_ATTRIBUTES = 'SPECIFIC_ATTRIBUTES'
    COUNT = 'COUNT'
