"""Generics to be extended for connecting to remote data stores and services

These can be adapted to support different backends by inheriting these to backends-specific versions. Use these generics
in your use cases to decouple use cases from specific backend requirements.
"""
from enum import Enum
from typing import Any, Callable, Dict, List, Type

from ckf_api_toolkit.tools.error_handling import ErrorConverter, ErrorParser


class ActionType(Enum):
    """Enum encapsulating the actions that can be performed for a given Instruction.

    Inherit, then define backend-specific action types. E.x. C, R, U, D
    """
    pass


class Instruction:
    """Class representing an instruction to a service.

    Attributes:
        action_type (ActionType): Used by actor to determine specific client methods if required. E.x. requests.get()
        payload (Any): Used by actor to give instructions to the client. Can be any kind of required object.
        parser (Callable): Parser function will be used to parse return values to the actor. Use for additional logic
         and formatting.
    """
    action_type: ActionType
    payload: Any
    parser: Callable

    def __init__(self, action_type: ActionType, payload: Any, parser: Callable):
        """Inits Instruction with action_type, payload and parser"""
        self.parser = parser
        self.payload = payload
        self.action_type = action_type


class UseCase:
    """Class representing a use case

    Attributes:
        name (str): The name of the use case
    """
    name: str


class Repository:
    """Class representing a repository of some sort(database, web service, other datastore, etc).

    Inherit, then define specific Instance state required for specific connections.

    Attributes:
        use_cases (Dict[str, Callable[[UseCase], Any]]): Dict of all use cases and their callables for this Repository
        error_converter (ErrorConverter): The error converter to use for this Repository
    """
    use_cases: Dict[str, Callable[[UseCase], Any]]
    error_converter: ErrorConverter

    def __init__(self):
        """Inits Repository with use cases and error converter"""
        self.use_cases = {}
        self.error_converter = ErrorConverter()

    def add_use_case(self, use_case: Type[UseCase], function: Callable[[Any], Instruction]):
        """Add a use case to this repository

        Args:
            use_case (UseCase): The Use Case to add
            function (Callable[[Any], Instruction]): The function to to call when running the supplied use case
        """
        self.use_cases[use_case.name] = function

    def get_instruction(self, use_case: UseCase) -> Instruction:
        """Retrieve the Instruction for a UseCase

        Args:
            use_case (UseCase): The UseCase to get the instruction for

        Returns:
            (Instruction) The Instruction fetched.
        """
        return self.use_cases[use_case.name](use_case)

    def add_error_conversion(self, incoming_error: Type[Exception], outgoing_error: Type[Exception],
                             error_parsers: List[ErrorParser] = None):
        """Add an error conversion for a given error

        Args:
            incoming_error (Exception): The error to apply conversion to
            outgoing_error (Exception): The now-converted error type
            error_parsers (List[ErrorParser]): A list of error parsers to use in the conversion
        """
        self.error_converter.add_error_conversion(incoming_error, outgoing_error, error_parsers)


class Client:
    """Class representing a client that connects to a Repository.

    Inherit, then define client specific initialization logic, and handling for action types.

    Attributes:
        action_types (Dict[ActionType, Callable]): dict of all action types and their callables for this client
    """
    action_types: Dict[ActionType, Callable]

    def __init__(self):
        """Inits Client with empty action_types"""
        self.action_types = {}

    def add_action_type(self, action_type: ActionType, payload_handler: Callable):
        """Add an ActionType to this client

        Args:
            action_type (ActionType): The action type to add
            payload_handler (Callable): A function to handle the payload for this action
        """
        self.action_types[action_type] = payload_handler

    def handle_action_type(self, action_type: ActionType, payload: Any) -> Any:
        """Handle the ActionType with the given payload

        Args:
            action_type (ActionType): The action type to handle
            payload(Any): The payload to process

        Returns:
            (Any) The result of handling the action type
        """
        return self.action_types[action_type](payload)


class Actor:
    """An actor executes defined use cases, and returns parsed values based on instances of the generic model classes.

    Attributes:
        repository (Repository): The repository this actor will interact with
        client (Client): The client used by this actor for its Repository interactions
    """
    repository: Repository
    client: Client

    def __init__(self, client: Client, repository: Repository):
        """Inits Actor with Client and Repository"""
        self.repository = repository
        self.client = client

    def run_use_case(self, use_case: UseCase) -> Any:
        """Run a UseCase for this actor

        Args:
            use_case (UseCase): The use case to run

        Returns:
            (Any) The result from running this use case
        """
        instruction = self.repository.get_instruction(use_case)
        # noinspection PyBroadException
        try:
            return instruction.parser(
                self.client.handle_action_type(instruction.action_type, instruction.payload)
            )
        except Exception as error:
            self.repository.error_converter.handle_error(error)
