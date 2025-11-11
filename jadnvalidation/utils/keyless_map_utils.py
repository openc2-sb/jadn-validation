"""
Utilities for handling keyless map operations in JADN validation.
"""

from typing import List
from jadnvalidation.models.jadn.jadn_type import Base_Type
from jadnvalidation.utils import general_utils
from jadnvalidation.utils.mapping_utils import to_dict_on_given_char


def convert_str_data_to_true_type(j_field_obj, field_data: str, check_none=True):
    """
    Convert string field_data to the appropriate Python type based on j_field_obj.base_type.
    Specifically designed for converting string data from keyless maps to proper types.
    
    Args:
        j_field_obj: The field object containing base_type information
        field_data: The data to convert (expected to be string for conversion)
        check_none: If True, only convert if field_data is not None
        
    Returns:
        The converted field_data (string converted to appropriate type, or original if not string)
    """
    # Early return for None values when check_none is True
    if check_none and field_data is None:
        return field_data
    
    # If data is not a string, return as-is (already correct type or will be handled elsewhere)
    if not isinstance(field_data, str):
        return field_data
    
    # Type conversion mapping for string input
    type_converters = {
        Base_Type.INTEGER.value: int,
        Base_Type.NUMBER.value: float,
        Base_Type.BOOLEAN.value: bool,
        # Add Base_Type.BINARY.value: bytes when needed
    }
    
    # Apply conversion if type is supported, otherwise return original data (UserDefined types are not converted here)
    converter = type_converters.get(j_field_obj.base_type)
    return converter(field_data) if converter else field_data


def convert_field_str_data_to_true_type(j_field_obj, field_data, check_none=True):
    """
    Convert string field_data to the appropriate Python type based on j_field_obj.base_type.
    Specifically designed for converting string data from keyless maps to proper types.
    
    This is an alias for convert_str_data_to_true_type with a more descriptive name.
    
    Args:
        j_field_obj: The field object containing base_type information
        field_data: The data to convert (expected to be string for conversion)
        check_none: If True, only convert if field_data is not None
        
    Returns:
        The converted field_data (string converted to appropriate type, or original if not string)
    """
    return convert_str_data_to_true_type(j_field_obj, field_data, check_none)


def use_keyless_map(j_type_opts: List[str]) -> list:
    """
    Checks if the keyless map option ('~') is present in the type options.
    Returns [opt_key, opt_val] if found, None otherwise.
    """
    if not j_type_opts:
        return None
        
    for opt in j_type_opts:
        opt_key, opt_val = general_utils.split_on_first_char(opt)
        if opt_key == '~':
            return ['~', opt_val or True]
    
    return None


def build_keyless_map(data, separator_position):
    """
    Build a keyless map dictionary from a list of string data.
    
    Args:
        data: List of strings to process into keyless map format
        separator_position: The position/character for splitting key-value pairs (from keyless map option)
        
    Returns:
        Dictionary containing the processed keyless map data
        
    Raises:
        TypeError: If any item in data is not a string
    """
    funny_data_map = {}
    
    for val in data:
        if not isinstance(val, str):
            raise TypeError(f'inparsable item in keyless map: {val}')
        
        dict_val = to_dict_on_given_char(val, separator_position)

        if list(dict_val.values()) == '':
            dict_val = {list(dict_val.keys())[0], True} 

        funny_data_map.update(dict_val)
    
    return funny_data_map
