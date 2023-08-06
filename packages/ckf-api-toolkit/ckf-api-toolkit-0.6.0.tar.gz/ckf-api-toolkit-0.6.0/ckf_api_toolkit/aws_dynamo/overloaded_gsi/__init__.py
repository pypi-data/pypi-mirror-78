"""
A set of utilities and a factory class to simplify implementation and usage of the Overloaded GSI pattern.

References:

https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-gsi-overloading.html
"""
from enum import Enum


class OverloadedGsiKeys(Enum):
    """Enum representing the chosen values used for constructing DynamoDB keys(hash/PK and sort/SK)"""
    PK = 'PK'
    SK = 'SK'
    GSI_PREFIX = 'GSI'
    DELIMITER = '_'


def get_gsi_pk(gsi: int) -> str:
    """Construct the PK for the given GSI

    Args:
        gsi (int): GSI number to create the PK for

    Returns:
        (str) The full GSI PK
    """
    return OverloadedGsiKeys.DELIMITER.value.join(
        [OverloadedGsiKeys.GSI_PREFIX.value, str(gsi), OverloadedGsiKeys.PK.value])


def get_gsi_sk(gsi: int) -> str:
    """Construct the SK for the given GSI

    Args:
        gsi (int): GSI number to create the SK for

    Returns:
        (str) The full GSI SK
    """
    return OverloadedGsiKeys.DELIMITER.value.join(
        [OverloadedGsiKeys.GSI_PREFIX.value, str(gsi), OverloadedGsiKeys.SK.value])
