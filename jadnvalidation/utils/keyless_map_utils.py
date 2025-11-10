"""
Utilities for handling keyless map operations in JADN validation.
"""

from jadnvalidation.models.jadn.jadn_type import Base_Type


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
