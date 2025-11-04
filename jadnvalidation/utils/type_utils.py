from jadnvalidation.models.jadn.jadn_type import is_basetype
from jadnvalidation.utils.general_utils import get_item_safe_check


def get_schema_type_by_name(j_types: list, name: str) -> list | None:
    type_list = [j_type for j_type in j_types if j_type[0] == name]
    type = None
    
    if type_list == None or get_item_safe_check(type_list, 0) == None:
        return None
    else:
        type = get_item_safe_check(type_list, 0)
    
    return type

def get_reference_type(jschema, type_name):
    if type_name is None:
        raise ValueError("type_name cannot be None")
    
    j_types = jschema.get('types')
    ref_type = get_schema_type_by_name(j_types, type_name)
    
    if ref_type and not is_basetype(ref_type[1]):
        ref_type = get_reference_type(jschema, ref_type[1])  

    if not ref_type:
        raise ValueError(f"Unknown type {type_name} referenced" )
    
    return ref_type

def get_schema_types(j_types: list, base_type: str):
    return [j_type for j_type in j_types if j_type[1] == base_type]  


def validate_type_references(schema):
    """
    Validates that each type's referenced type (schema.types[i][1]) that's not a BaseType 
    exists in the schema.types[0] (type names).
    
    Args:
        schema: JADN schema dictionary
        
    Returns:
        list: List of validation errors, empty if all references are valid
    """
    errors = []
    types = schema.get('types', [])
    
    # Get all type names defined in the schema
    defined_type_names = {type_def[0] for type_def in types}
    
    for type_def in types:
        if len(type_def) < 2:
            continue
            
        type_name = type_def[0]
        referenced_type = type_def[1]
        
        # Check if the referenced type is not a base type and not defined in schema
        if not is_basetype(referenced_type) and referenced_type not in defined_type_names:
            errors.append(f"Type '{type_name}' references undefined type '{referenced_type}'")
    
    return errors


def validate_field_type_references(schema):
    """
    Validates that each field's type (schema.types[i][4][j][2]) that's not a BaseType 
    exists in the schema.types[0] (type names).
    
    Args:
        schema: JADN schema dictionary
        
    Returns:
        list: List of validation errors, empty if all references are valid
    """
    errors = []
    types = schema.get('types', [])
    
    # Get all type names defined in the schema
    defined_type_names = {type_def[0] for type_def in types}
    
    for type_def in types:
        if len(type_def) < 5:
            continue
            
        type_name = type_def[0]
        fields = type_def[4]
        
        if not isinstance(fields, list):
            continue
            
        for field in fields:
            if len(field) < 3:
                continue
                
            field_name = field[1] if len(field) > 1 else "unknown"
            field_type = field[2]
            
            # Skip if field_type is None or not a string
            if field_type is None or not isinstance(field_type, str):
                continue
                
            # Skip type references that start with special prefixes (like #, *, +)
            # These are option indicators, not actual type references
            if field_type.startswith(('#', '*', '+')):
                continue
                
            # Check if the field type is not a base type and not defined in schema
            if not is_basetype(field_type) and field_type not in defined_type_names:
                errors.append(f"Type '{type_name}', field '{field_name}' references undefined type '{field_type}'")
    
    return errors  