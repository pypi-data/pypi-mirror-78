"""
Simple class wrapping an instance of a requests object
"""
from typing import Any, Dict


# Very basic payload generation for requests
# TODO: Implement full requests feature set
class RequestsPayload:
    """Represents an instance of a requests object

    Attributes:
        params (dict): Params for the request
        url (str): URL to send request to
        headers (dict): Headers for the request
        data (dict): Data to send with request
    """
    params: dict
    url: str
    headers: dict
    data: dict

    def __init__(self, url: str):
        """Inits RequestsPayload with empty values"""
        self.url = url
        self.headers = {}
        self.data = {}
        self.params = {}

    def add_header(self, header_name: str, header_value: Any):
        """Add a header to the request

        Args:
            header_name (str): Name of the header to add
            header_value (Any): Value of the header to add
        """
        self.headers[header_name] = header_value

    def add_data_key(self, data_key: str, data_value: Any):
        """Add a data key to the request

        Args:
            data_key (str): Key for the data to add
            data_value (Any): Value of the data to add
        """
        self.data[data_key] = data_value

    def set_data(self, data: Dict[str, Any]):
        """Set the data for the request from the given dict

        Args:
            data (Dict[str, Any]): The data to send
        """
        self.data = {**data}

    def add_param(self, param_key: str, param_value: Any):
        """Add a parameter to the request

        Args:
            param_key (str): The key of the parameter
            param_value (Any): The value of the parameter
        """
        self.params[param_key] = param_value

    def set_params(self, params: Dict[str, Any]):
        """Set the parameters for the request from the given dict

        Args:
            params (Dict[str, Any]): The parameters to add
        """
        self.params = {**params}
