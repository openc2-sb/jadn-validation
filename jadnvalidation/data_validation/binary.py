from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_fmt_clz_instance
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length

common_rules = {
    "data": "check_data",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length"
}

json_rules = {}
xml_rules = {}

class Binary:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Union[list, Jadn_Type] = None
    data: any = None # Binary data only
    data_format: str = None  
    string_variable: str = None
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: list = [], data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format        
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_data(self):
        # Accept str (convert to bytes), or bytes only
        if self.data is not None:
            if isinstance(self.data, str):
                try:
                    self.data = self.data.encode('utf-8')
                except Exception as e:
                    self.errors.append(f"Failed to encode string to bytes: {e}")
                    return
            if not isinstance(self.data, bytes):
                self.errors.append(f"Binary data must be of type 'bytes'. Received: {type(self.data).__name__}")
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Binary length must be greater than or equal to {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if len(self.data) > max_length:
            self.errors.append(f"Binary length must be less than or equal to {max_length}. Received: {len(self.data)}")
        
    def check_format(self):
        if self.data is not None:
            format = get_format(self.j_type)
            
            if format is not None:
                
                # Note: this format breaks the normal convention since it has two designators for the same format
                if format.lower() == 'x' or format.lower() == 'X':
                    format = "hex_binary"
            
                fmt_clz_instance = create_fmt_clz_instance(format, self.data)
                fmt_clz_instance.validate()
        
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
