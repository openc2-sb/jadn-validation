from typing import Any
from enum import Enum

from jadnvalidation.utils.general_utils import safe_get

class Primitive(Enum):  
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    
class Enumeration(Enum):
    ENUMERATED = 'Enumerated'
    
class Specialization(Enum):
    CHOICE = 'Choice'
    
class Structure(Enum):
    ARRAY = 'Array'
    MAP = 'Map'
    RECORD = 'Record'

# Core Types
class Base_Type(Enum):
    BINARY = 'Binary'
    BOOLEAN = 'Boolean'
    INTEGER = 'Integer'
    NUMBER = 'Number'
    STRING = 'String'
    ARRAY = 'Array'
    ARRAY_OF = 'ArrayOf'
    CHOICE = 'Choice'
    ENUMERATED = 'Enumerated'
    MAP = 'Map'
    MAP_OF = 'MapOf'
    RECORD = 'Record'

class Jadn_Type():
    id: str = None
    type_name: str = None
    value: str = None
    base_type: Base_Type = None
    type_options: list[str] = None
    type_description: str = None
    fields: list[Any] = None
    required: bool = False
    
    def __init__(self, type_name, base_type, id = None, type_options = [], type_description = "", fields = []):
        self.id = id # available for enums
        self.type_name = type_name
        self.base_type = base_type    
        self.type_options = type_options    
        self.type_description = type_description
        self.fields = fields

def is_array(jadn_type: Jadn_Type) -> bool:
    if jadn_type.base_type == Base_Type.ARRAY.value:
        return True
    else:
        return False  
            
def is_basetype(type: str) -> bool:
    return type in [item.value for item in Base_Type]        
    
def is_enumerated(jadn_type: list[any]):
    if len(jadn_type) == 3:
            return True
    return False
    
def is_enumeration(jadn_type: Jadn_Type) -> bool:
    return jadn_type.base_type in [item.value for item in Enumeration]
    
def is_field(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], int):
            return True
    return False

def is_field_multiplicity(opts: list) -> bool:
    """
    Checks if any option in the opts list indicates field multiplicity.
    Returns True if any option starts with '[' or ']' and the second character is a digit >= 2,
    or if it starts with ']' and the rest is '-1' or '-2'.
    """
    if opts:
        for opt in opts:
            if len(opt) >= 2:
                if (opt[0] in ['[', ']']) and opt[1].isdigit() and int(opt[1]) >= 2:
                    return True
                if opt[0] == ']' and (opt[1:] == '-1' or opt[1:] == '-2'):
                    return True
    return False

def is_primitive(type: str) -> bool:
    return type in [item.value for item in Primitive]
    
def is_non_primitive(type: str) -> bool:
    return (type in [item.value for item in Structure] or 
            type in [item.value for item in Enumeration] or 
            type in [item.value for item in Specialization])
    
def is_record_or_map(jadn_type: Jadn_Type) -> bool:
    return (jadn_type.base_type == Base_Type.RECORD.value or 
            jadn_type.base_type == Base_Type.MAP.value)
    
def is_specialization(jadn_type: Jadn_Type) -> bool:
    return jadn_type.base_type in [item.value for item in Specialization]
    
def is_structure(jadn_type: Jadn_Type) -> bool:
    return jadn_type.base_type in [item.value for item in Structure]
    
def is_type(jadn_type: list[any]):
    if len(jadn_type) > 0:
        if isinstance(jadn_type[0], str):
            return True
    return False    
    
def is_user_defined(ktype:str):
    if ktype is None:
        return False
    return not is_basetype(ktype)

def build_j_type(j_type: list) -> Jadn_Type | None:
    jadn_type_obj = None
    
    if is_type(j_type):
        jadn_type_obj = Jadn_Type(
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=safe_get(j_type, 2, []), 
                type_description=safe_get(j_type, 3, ""),
                fields=safe_get(j_type, 4, []))   
    else:
        raise ValueError("Invalid jadn type")
    
    return jadn_type_obj

def build_jadn_type_obj(j_type: list) -> Jadn_Type | None: 
    jadn_type_obj = None

    if is_field(j_type):
        # Field should have at least 4 elements: [id, name, base_type, options, ...]
        # Handle malformed fields that might be missing base_type/options
        base_type = safe_get(j_type, 2, None)
        type_options = safe_get(j_type, 3, [])
        jadn_type_obj = Jadn_Type(
                id=j_type[0],
                type_name=j_type[1], 
                base_type=base_type, 
                type_options=type_options, 
                type_description=safe_get(j_type, 4, ""))
    elif is_type(j_type):
        jadn_type_obj = Jadn_Type(
                type_name=j_type[0], 
                base_type=j_type[1], 
                type_options=j_type[2], 
                type_description=j_type[3],
                fields=safe_get(j_type, 4, []))
    elif is_enumerated(j_type):
        jadn_type_obj = Jadn_Type(
                id=j_type[0],
                type_name=j_type[1], 
                base_type=None, 
                type_options=[], 
                type_description=j_type[2])

    else:
        print("unknown jadn item")
    
    return jadn_type_obj