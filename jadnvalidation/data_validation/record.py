from typing import Union

from jadnvalidation.models.jadn.jadn_type import build_j_type, build_jadn_type_obj, is_field_multiplicity, is_user_defined
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_field_name, check_sys_char, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, get_data_by_name, merge_opts
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_inheritance, get_max_length, get_max_occurs, get_min_length, get_min_occurs, get_tagged_data, is_optional
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "type": "check_type",
    "e": "check_inheritance",    
    "{": "check_min_length",
    "}": "check_max_length",
    "fields": "check_fields",
    "extra_fields": "check_extra_fields"
}

json_rules = {}
xml_rules = {}


class Record:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The record data only
    data_format: str = None    
    errors = []
    
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
        if not isinstance(self.data, dict):
            raise ValueError(f"Data for type {self.j_type.type_name} must be a record / dict. Received: {type(self.data)}")
        
    def check_inheritance(self):
        inherit_from = get_inheritance(self.j_type.type_options)
        if inherit_from is not None:
            inherited_type = get_reference_type(self.j_schema, inherit_from)
            inherited_type_obj = build_j_type(inherited_type)
            
            if inherited_type is None:
                raise ValueError(f"Type {self.j_type.type_name} inherits from unknown type {inherit_from}")
            
            if self.j_type.base_type != inherited_type_obj.base_type:
                raise ValueError(f"Type {self.j_type.type_name} inherits from type {inherit_from} with different base type {inherited_type_obj.base_type}. Received: {self.j_type.base_type}")
            
            # Prepend inherited fields to current fields
            self.j_type.fields = inherited_type_obj.fields + self.j_type.fields        
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields for type {self.j_type.type_name} must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length for type {self.j_type.type_name} must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        for j_key, j_field in enumerate(self.j_type.fields):
            field_data = get_data_by_name(self.data, j_field[1])
            j_field_obj = build_jadn_type_obj(j_field)
            
            if field_data is None:
                if is_optional(j_field_obj):
                    continue
                else:
                    raise ValueError(f"Field '{j_field[1]}' is missing from data")
                
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)                
            
            if is_field_multiplicity(j_field_obj.type_options):
                j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
            
            elif is_user_defined(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                j_field_obj = ref_type_obj
                j_field_obj.type_options = merged_opts
                
            tagged_data = get_tagged_data(j_field_obj, self.data)                
                
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=field_data,
                data_format=self.data_format
            )
            if tagged_data is not None:
                clz_kwargs['tagged_data'] = tagged_data

            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()
            
    def check_extra_fields(self):
        # Check if data has any unknown fields
        if self.data is not None:
            for data_key in self.data.keys():
                is_found = False
                for j_field in self.j_type.fields:
                    if data_key == j_field[1]:
                        is_found = True
                        break
                
                if is_found == False:
                    self.errors.append(f"Unknown data {data_key}.")
                
    def validate(self):
        
        # Check data against rules
        rules = json_rules
        if self.data_format == XML:
            rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True
