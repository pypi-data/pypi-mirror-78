"""
Model utilities
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, List, Dict, Iterable, Optional

from ckf_api_toolkit.tools.api_response_handler import ApiResponseException, ResponseCode

"""
Parser Type
"""

Parser = Callable[[str, Any], Any]

"""
Model initialization
"""


class Model(ABC):
    """Abstract class to be implemented by your custom data models

    Attributes:
        suppress_validation (bool): Whether to suppress validation for this model
    """
    suppress_validation: bool

    def __init__(self, *, suppress_validation: bool = False, **kwargs):
        """Inits Model with kwargs"""
        self.suppress_validation = suppress_validation
        for k, v, in kwargs.items():
            setattr(self, k, v)

    @classmethod
    @abstractmethod
    def init_from_db(cls, model_dict: dict):
        """Initialize a model instance from the database

        Args:
            model_dict (dict): Dictionary containing the model data
        """
        pass

    @classmethod
    @abstractmethod
    def init_from_front_end(cls, model_dict: dict):
        """Initialize a model instance from the frontend

        Args:
            model_dict (dict): Dictionary containing the model data
        """
        pass

    @classmethod
    @abstractmethod
    def creation_init_from_front_end(cls, model_dict: dict):
        """Special initializer for object creation, e.x. for generating IDs

        Args:
            model_dict (dict): Dictionary containing the model data"""
        pass

    @abstractmethod
    def get_dict_for_front_end(self, *, private: bool = False) -> dict:
        """Return a dictionary representation of the model for the frontend

        Args:
            private (bool): Dictionary containing the model data

        Returns:
            (dict) A dictionary representation of the model for the frontend
        """
        pass

    @abstractmethod
    def get_dict_for_db(self) -> dict:
        """Return a dictionary representation of the model for the database

        Returns:
            (dict) A dictionary representation of the model for the database
        """
        pass


@dataclass(frozen=True)
class ModelAttributes(ABC):
    """Abstract class to be implemented for model attributes"""
    pass


class MissingRequiredParams(ApiResponseException):
    """Class representing an API response exception for missing params

    Attributes:
        missing_params (List[str]): The params missing from the response
    """
    missing_params: List[str]

    def __init__(self, object_name: str, missing_params: List[str]):
        """Inits MissingRequiredParams with the list of missing params, and calls the parent init() method with the
         response code and formatted error message"""
        self.missing_params = missing_params
        super().__init__(
            ResponseCode.BAD_REQUEST,
            f"Supplied {object_name} is invalid. Missing required fields: {', '.join(self.missing_params)}"
        )


# For use on @classmethod model initializers
def validate_model_required_fields(model_name: str, required_params: Iterable[str]):
    """Decorator for validating the required fields on a model

    Args:
        model_name (str): Name of the model to validate against
        required_params (Iterable[str]): The parameters on the model that are required
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            data_object: dict = args[1]
            missing_params = [param_name for param_name in required_params if
                              param_name not in data_object or not data_object[param_name]]

            if missing_params:
                raise MissingRequiredParams(model_name, missing_params)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class UnexpectedModelAttribute(ApiResponseException):
    """Class representing an API response exception for an unexpected model attribute"""
    def __init__(self, invalid_attribute: str):
        """Inits UnexpectedModelAttribute with response code and formatted error message"""
        super().__init__(ResponseCode.BAD_REQUEST, f"Unexpected attribute: '{invalid_attribute}'.")


def model_initializer(model_cls: Callable, data_object: dict, attributes: ModelAttributes,
                      parser: Optional[Parser] = None, *, suppress_validation: bool = False, **kwargs):
    """Initialize a model of the given class, optionally with an attribute parser and suppressing validation

    Args:
        model_cls (Callable): The model class to initialize
        data_object (dict): Dictionary representing the model data
        attributes (ModelAttributes): The attributes for the model
        parser (Optional[Parser]): Parser for model attributes
        suppress_validation (bool): Whether to suppress validation on this model
        **kwargs (kwargs): kwargs for the model initialization
    """
    valid_attributes = vars(attributes).values()
    if not suppress_validation:
        for supplied_attribute in data_object.keys():
            if supplied_attribute not in valid_attributes:
                raise UnexpectedModelAttribute(supplied_attribute)

    return model_cls(
        **{attribute_model_key: (
            parser(attribute_model_key, data_object[attribute_str]) if parser else data_object[attribute_str]
        ) if attribute_str in data_object else None for attribute_model_key, attribute_str in vars(attributes).items()},
        suppress_validation=suppress_validation, **kwargs
    )


"""
Model validation
"""


class InvalidModel(ApiResponseException):
    """Class representing an API response exception for an unexpected model attribute

    Attributes:
        missing_params (List[str]): The params missing for this model
    """
    missing_params: List[str]

    def __init__(self, object_name: str, missing_params: List[str], identifier: str = None):
        """Inits InvalidModel with missing_params, and calls the parent init() method with the
         response code and formatted error message"""
        self.missing_params = missing_params
        identifier_str = f": {identifier}" if identifier else ""
        super().__init__(
            ResponseCode.BAD_REQUEST,
            f"{object_name}{identifier_str} is invalid. Missing required fields: {', '.join(self.missing_params)}"
        )


# For use on instance methods of Model classes
def validate_model(model_name: str, required_attributes: ModelAttributes, identifier_attr: Optional[str] = None):
    """Decorator to validate a model instance

    Args:
        model_name (str): Name of the model to validate
        required_attributes (ModelAttributes): The required model attributes
        identifier_attr (Optional[str]): Identifier attribute for the object
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            model_object_ref: Model = args[0]

            missing_params = [
                param_name for attr_name, param_name in vars(required_attributes).items()
                if not getattr(model_object_ref, attr_name, None)
            ]

            if missing_params:
                raise InvalidModel(
                    model_name,
                    missing_params,
                    getattr(model_object_ref, identifier_attr, None) if identifier_attr else None,
                )
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


"""
Dictionary formatting
"""


def get_model_dict(model_self: Model, attributes: ModelAttributes, parser: Optional[Parser] = None) -> Dict[str, Any]:
    """Return a dictionary representation of the model

    Args:
        model_self (Model): The model to return a dictionary of
        attributes (ModelAttributes): The attributes to populate the dict with
        parser (Optional[Parser]): A Parser for the model attributes

    Returns:
        (Dict[str, Any]) The dictionary representation of the model
    """
    return {getattr(attributes, k): parser(k, v) if parser else v for k, v in
            [(model_key, getattr(model_self, model_key)) for model_key in vars(attributes).keys()]}
