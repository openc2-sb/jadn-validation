from typing import Union

from jadnvalidation.models.jadn.jadn_type import build_jadn_type_obj
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, create_fmt_clz_instance, get_item_safe_check
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_format, get_max_length, get_max_occurs, get_min_length, get_min_occurs, is_optional
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length",
    "fields": "check_fields"
}

json_rules = {}
xml_rules = {}

class Array:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The array's data only
    data_format: str = None    
    errors = []
    continue_checks = True
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format        
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        print(type(self.data))
        if isinstance(self.data, str):
            if "/ipv4-net" in self.j_type.type_options or "/ipv6-net" in self.j_type.type_options:
                pass
            else: raise ValueError(f"Data for type {self.j_type.type_name} of the wrong type. Received: {type(self.data)}")
        elif not isinstance(self.data, list):
            raise ValueError(f"Data for type {self.j_type.type_name} must be a list. Received: {type(self.data)}")
        
            '''
    def check_type(self):

        if self.data != None and not isinstance(self.data, list):
            if isinstance(self.data, str):
                if "/ipv4net" in self.j_type.type_options or "/ipv6net" in self.j_type.type_options:
                    pass
            else: raise ValueError(f"Data for type {self.j_type.type_name} of the wrong type. Received: {type(self.data)}")
        elif self.data is None:
            if "}0" in self.j_type.type_options:
                pass
            else: raise ValueError(f"Data missing for type {self.j_type.type_name}")
        else: raise ValueError(f"Data for type {self.j_type.type_name} must be a list. Received: {type(self.data)}")
        '''
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Array length for type {self.j_type.type_name} must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        
        if max_length is None or max_length == 0:
            max_length = len(self.j_type.fields)
        
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Array length for type {self.j_type.type_name} must be less than {max_length}. Received: {len(self.data)}")
        
    def check_format(self):
        if self.data is not None:
            format = get_format(self.j_type)
            if format is not None:
                fmt_clz_instance = create_fmt_clz_instance(format, self.j_schema, self.j_type, self.data, self.data_format)
                fmt_clz_instance.validate()
                self.continue_checks = False
        
    def check_fields(self):
        for j_index, j_field in enumerate(self.j_type.fields):
            j_field_obj = build_jadn_type_obj(j_field)
            field_data = get_item_safe_check(self.data, j_index)    
            
            if field_data is None:
                if is_optional(j_field_obj):
                    continue
                else:
                    raise ValueError(f"Missing required field '{j_field[1]}' for array type {self.j_type.type_name}")
        
            if not is_primitive(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                j_field_obj = ref_type_obj
                
            min_occurs = get_min_occurs(j_field_obj)
            max_occurs = get_max_occurs(j_field_obj, self.j_config)
            if min_occurs > 1 or max_occurs > 1:
                j_field_obj = flip_to_array_of(j_field_obj, min_occurs, max_occurs)
            elif max_occurs > 1:
                j_field_obj = flip_to_array_of(j_field_obj, min_occurs, max_occurs)
                
            clz_instance = create_clz_instance(j_field_obj.base_type, self.j_schema, j_field_obj, field_data, self.data_format)
            clz_instance.validate()
        
    def validate(self):
        
        # Check data against rules
        rules = json_rules
        if self.data_format == XML:
            if self.continue_checks:
                rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            if self.continue_checks:
                getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            if self.continue_checks:
                getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True