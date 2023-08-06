"""
HTTP Actor

HTTP REST specific versions of the classes used by an Actor.
Uses: requests 2.22.0
"""
from typing import Callable

from requests import Session, Response
from requests.adapters import HTTPAdapter
from requests.structures import CaseInsensitiveDict
from urllib3 import Retry

from ckf_api_toolkit.core import ActionType, Instruction, Client
from ckf_api_toolkit.http.requests_payload_construction import RequestsPayload


class HttpActionType(ActionType):
    """Action types for an HTTP request"""
    PUT = "PUT"
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"


class HttpInstruction(Instruction):
    """Instruction """
    def __init__(self, action_type: HttpActionType, payload: RequestsPayload, parser: Callable):
        super().__init__(action_type, payload, parser)


def _get_client_session(retries: int, backoff_factor: float = 0) -> Session:
    session = Session()
    retry = Retry(total=retries, backoff_factor=backoff_factor)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


class RequestsClient(Client):
    timeout: float
    headers: CaseInsensitiveDict

    def __init__(self, retries: int, timeout: float, backoff_factor: float = 0, *, headers: dict = None):
        super().__init__()
        self.__client = _get_client_session(retries, backoff_factor)
        if headers:
            self.__client.headers.update(CaseInsensitiveDict(headers))
        self.timeout = timeout
        self.add_action_type(HttpActionType.GET, self.__get)
        self.add_action_type(HttpActionType.PUT, self.__put)
        self.add_action_type(HttpActionType.POST, self.__post)
        self.add_action_type(HttpActionType.DELETE, self.__delete)

    def __get(self, payload: RequestsPayload) -> Response:
        response = self.__client.get(**vars(payload), timeout=self.timeout)
        response.raise_for_status()

        return response

    def __put(self, payload: RequestsPayload) -> Response:
        response = self.__client.put(**vars(payload), timeout=self.timeout)
        response.raise_for_status()

        return response

    def __post(self, payload: RequestsPayload) -> Response:
        response = self.__client.post(**vars(payload), timeout=self.timeout)
        response.raise_for_status()

        return response

    def __delete(self, payload: RequestsPayload) -> Response:
        response = self.__client.delete(**vars(payload), timeout=self.timeout)
        response.raise_for_status()

        return response
