from json import loads
from typing import Dict, Any, NamedTuple

'''
Misc
===========================================================
'''


# Used to allow local testing of Lambda
def get_event_body(event_object) -> Dict[Any, Any]:
    try:
        body = loads(event_object["body"])
    except TypeError:
        body = event_object["body"]
    return body


# Sanitize API data of new fields not yet implemented on client-side
# noinspection PyPep8Naming
def get_sanitized_model(ModelClass: type(NamedTuple), data: Dict[Any, Any]) -> NamedTuple:
    # noinspection PyProtectedMember
    return ModelClass(**{k: v for k, v in data.items() if k in ModelClass._fields})

# TODO: create a decorator that can wrap @property and return None if the initial property is None
# def safe_derived_property(initial_property: Any):
#     pass
