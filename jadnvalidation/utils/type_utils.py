from jadnvalidation.models.jadn.jadn_type import is_basetype
from jadnvalidation.utils.general_utils import get_item_safe_check


def get_schema_type_by_name(j_types: list, name: str):
    type_list = [j_type for j_type in j_types if j_type[0] == name]
    type = None
    
    if type_list == None or get_item_safe_check(type_list, 0) == None:
        return None
    else:
        type = get_item_safe_check(type_list, 0)
    
    return type

def get_reference_type(jschema, type_name):
    j_types = jschema.get('types')
    ref_type = get_schema_type_by_name(j_types, type_name)
    
    if not is_basetype(ref_type[1]):
        ref_type = get_reference_type(jschema, ref_type[1])  

    if not ref_type:
        raise ValueError(f"Unknown type {type_name} referenced" )
    
    return ref_type

def get_schema_types(j_types: list, base_type: str):
    return [j_type for j_type in j_types if j_type[1] == base_type]  