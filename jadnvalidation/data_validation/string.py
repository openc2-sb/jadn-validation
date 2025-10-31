from jadnvalidation.data_validation.formats.pattern import Pattern
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_fmt_clz_instance
from jadnvalidation.utils.mapping_utils import get_format, get_max_length, get_min_length, get_pattern, get_min_inclusive, get_max_inclusive, get_min_exclusive, get_max_exclusive, get_const_val_str


common_rules = {
    "type": "check_type",
    "/": "check_format",
    "{": "check_min_length",
    "}": "check_max_length",
    "v": "check_constant",
    "w": "check_min_inclusive",
    "x": "check_max_inclusive",
    "y": "check_min_exclusive",
    "z": "check_max_exclusive",
    "%": "check_pattern"
}

json_rules = {}
xml_rules = {}

class String:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Jadn_Type = None
    data: any = None # The string's data only
    data_format: str = None    
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Jadn_Type = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format          
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_format(self):
        if self.data is not None:
            format = get_format(self.j_type)
            if format is not None:
                fmt_clz_instance = create_fmt_clz_instance(format, self.data)
                fmt_clz_instance.validate()
            
    def check_pattern(self):
        if self.data is not None:
            tmp = self.data
            try:
                if tmp and self.data_format == XML and tmp[0] == "n" and isinstance(int(tmp[1:]), int): # address issue where pattern check fails on n- prepended XML tags of digit type
                    tmp = tmp[1:]
            except:
                pass # XML tag not a number and wont have prepended "n", so no issue
            pattern = get_pattern(self.j_type)
            if pattern is not None and self.data:
                if tmp != self.data:
                    pattern_instance = Pattern(tmp, pattern)
                else:
                    pattern_instance = Pattern(self.data, pattern)
                pattern_instance.validate()        
        
    def check_type(self):
        if self.data is not None:
            if not isinstance(self.data, str):
                raise ValueError(f"Data for type {self.j_type.type_name} must be a string. Received: {type(self.data)}")
        else:  
            pass
    
    def check_constant(self):
        const_val = get_const_val_str(self.j_type)  
        if const_val is not None: 
            if self.data == const_val:
                pass
            else:
                self.errors.append(f"String for type {self.j_type.type_name} value must be exactly {const_val}. Received: {self.data}")

    def check_min_length(self):
        min_length = get_min_length(self.j_type)    
        if min_length is not None and self.data is None: 
            raise ValueError(f"A String value for type {self.j_type.type_name} is required. Received: None")
        elif min_length is not None and len(self.data) < min_length:
            self.errors.append(f"String for type {self.j_type.type_name} length must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self): 
        if self.data is not None:  
            max_length = get_max_length(self.j_type, self.j_config)
            if len(self.data) > max_length:
                self.errors.append(f"String for type {self.j_type.type_name} length must be less than {max_length}. Received: {len(self.data)}")
            
    def check_min_inclusive(self): 
        if self.data is not None:  
            min_inclusive = get_min_inclusive(self.j_type)
            if min_inclusive != None and len(str(self.data)) < (min_inclusive):
                self.errors.append(f"String for type {self.j_type.type_name} length must be at least {min_inclusive}. Received: {len(self.data)}")
    
    def check_max_inclusive(self): 
        if self.data is not None:  
            max_inclusive = get_max_inclusive(self.j_type)
            if max_inclusive != None and len(self.data) > (max_inclusive):
                self.errors.append(f"String for type {self.j_type.type_name} length cannot be more than {max_inclusive}. Received: {len(self.data)}")
    
    def check_min_exclusive(self): 
        if self.data is not None:  
            min_exclusive = get_min_exclusive(self.j_type)
            if min_exclusive != None and len(self.data) < (min_exclusive+1):
                self.errors.append(f"String for type {self.j_type.type_name} length must be more than {min_exclusive}. Received: {len(self.data)}")
    
    def check_max_exclusive(self): 
        if self.data is not None:  
            max_exclusive = get_max_exclusive(self.j_type)
            if max_exclusive != None and len(self.data) > (max_exclusive-1):
                self.errors.append(f"String for type {self.j_type.type_name} length must be less than {max_exclusive}. Received: {len(self.data)}")

                                   
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