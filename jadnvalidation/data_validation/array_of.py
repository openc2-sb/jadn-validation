from typing import Union

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_primitive
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance
from jadnvalidation.utils.mapping_utils import get_max_length, get_min_length, get_vtype, is_optional
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "type": "check_type",
    "max_elements": "check_max_elements",
    "{": "check_min_length",
    "}": "check_max_length",    
    "fields": "check_vtype"
}

json_rules = {}
xml_rules = {}

class ArrayOf:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The array of's data only
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
        if not isinstance(self.data, list):
            raise ValueError(f"Data for type {self.j_type.type_name} must be a list. Received: {type(self.data)}")
        
    def check_max_elements(self):
        if self.data and len(self.data) > self.j_config.MaxElements:
            raise ValueError(f"Data items for type {self.j_type.type_name} exceed the maximum limit of {self.j_config.MaxElements}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Array length for type {self.j_type.type_name} must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Array length for type {self.j_type.type_name} must be less than {max_length}. Received: {len(self.data)}")
        
    def check_vtype(self):
        vtype = get_vtype(self.j_type)
        
        if self.data is None:
            if not is_optional(self.j_type):
                self.errors.append(f"Array '{self.j_type.type_name}' missing data")        
        
        for data_item in self.data:
            
            clz_kwargs = dict(
                j_schema=self.j_schema,
                data=data_item,
                data_format=self.data_format
            )            
            
            if is_primitive(vtype):
                of_jtype = Jadn_Type("of_" + self.j_type.type_name, vtype)
                
                clz_kwargs['class_name'] = vtype
                clz_kwargs['j_type'] = of_jtype
                
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()                
            else:                
                ref_type = get_reference_type(self.j_schema, vtype)
                ref_type_obj = build_j_type(ref_type)
                
                clz_kwargs['class_name'] = ref_type_obj.base_type
                clz_kwargs['j_type'] = ref_type_obj                
                
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()                
        
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