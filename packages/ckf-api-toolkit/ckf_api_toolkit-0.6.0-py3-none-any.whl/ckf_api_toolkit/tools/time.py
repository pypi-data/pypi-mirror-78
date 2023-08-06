from datetime import datetime, timezone
from typing import Union, Any

from dateutil.parser import parse

'''
Datetime Utils
===========================================================
'''


def get_timestamp(date_time: Union[datetime, None]) -> Union[float, None]:
    if date_time:
        return date_time.timestamp()
    else:
        return None


def get_time_from_timestamp(db_value: Union[float, None]) -> Union[datetime, None]:
    if db_value:
        return datetime.fromtimestamp(db_value, tz=timezone.utc)
    else:
        return None


def get_time_str(date_time: Union[datetime, None]) -> Union[str, None]:
    if date_time:
        return date_time.isoformat()
    else:
        return None


class InvalidDateString(Exception):
    def __init__(self, supplied_date: Any):
        self.message = f"Supplied date string: '{str(supplied_date)}' is invalid."


def get_time_from_str(front_value: Union[str, None]) -> Union[datetime, None]:
    if front_value:
        try:
            return parse(front_value)
        except (ValueError, TypeError):
            raise InvalidDateString(front_value)
    else:
        return None
