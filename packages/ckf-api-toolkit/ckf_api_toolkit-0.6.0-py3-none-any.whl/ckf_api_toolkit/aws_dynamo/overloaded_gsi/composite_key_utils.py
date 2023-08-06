"""
Utility functions for composite keys and dictionaries using them
"""
from typing import List, Optional

KEY_DELIMITER = '#'


def make_composite_key(ordered_key_values: List[str], key_delimiter: str = KEY_DELIMITER, *,
                       append_delimiter: bool = False) -> str:
    f"""Create a composite key from the given ordered key values, and the given delimiter

    Args:
        ordered_key_values (List[str]): A list of ordered key values to use for creating the composite key
        key_delimiter (str, default: {KEY_DELIMITER}): Optional delimiter to use for creating the composite key
        append_delimiter (bool): Whether to append the delimiter to the key

    Returns:
        (str) The composite key created from inputs
    """
    return key_delimiter.join(ordered_key_values) if not append_delimiter \
        else key_delimiter.join(ordered_key_values) + key_delimiter


def parse_composite_key(composite_key: str, key_delimiter: str = KEY_DELIMITER) -> List[str]:
    f"""Parse a composite key into a list of parts

    Args:
        composite_key (str): The composite key to parse
        key_delimiter (str, default: {KEY_DELIMITER}): Optional delimited to use for the composite key

    Returns:
        (List[str]) The parsed parts of the given composite key
    """
    return composite_key.split(key_delimiter)


def get_dict_with_model_keys(original_dict: dict, composite_key_name: str,
                             ordered_component_key_names: List[str], key_delimiter: Optional[str] = None) -> dict:
    f"""Return a dict with the given model keys included

    Args:
        original_dict (dict): The original dict to add model keys to
        composite_key_name (str): Name of the composite key to add
        ordered_component_key_names (List[str]): A list of component key names to inject
        key_delimiter (str, default: {KEY_DELIMITER}): Optional delimiter to use for the composite key

    Returns:
        (dict) The input dict modified with entries for the model keys
    """
    if not key_delimiter:
        key_delimiter = KEY_DELIMITER
    composite_key: str = original_dict[composite_key_name]
    key_value_list = parse_composite_key(composite_key, key_delimiter)

    return {
        **{k: v for k, v in original_dict.items() if k != composite_key_name},
        **{component_key: key_value_list[index] for index, component_key in enumerate(ordered_component_key_names)}
    }


def get_dict_with_composite_key(original_dict: dict, composite_key_name: str,
                                ordered_component_key_names: List[str], key_delimiter: Optional[str] = None) -> dict:
    f"""Return a dict with the given composite key included

    Args:
        original_dict (dict): The original dict to add model keys to
        composite_key_name (str): Name of the composite key to add
        ordered_component_key_names (List[str]): A list of component key names to inject
        key_delimiter (str, default: {KEY_DELIMITER}): Optional delimiter to use for the composite key

    Returns:
        (dict) The input dict modified with entries for the composite key
    """
    if not key_delimiter:
        key_delimiter = KEY_DELIMITER
    composite_key = make_composite_key(
        [key_value for key_value in [original_dict[key_name] for key_name in ordered_component_key_names]],
        key_delimiter,
    )

    return {
        **{k: v for k, v in original_dict.items() if k not in ordered_component_key_names},
        composite_key_name: composite_key,
    }
