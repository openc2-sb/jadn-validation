from typing import Union

from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type, is_primitive, is_user_defined
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, generate_sha256, is_even
from jadnvalidation.utils.mapping_utils import get_ktype, get_max_length, get_min_length, get_vtype, is_optional
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "type": "check_type",
    "max_elements": "check_max_elements",    
    "{": "check_min_length",
    "}": "check_max_length",
    "key_value_types": "check_key_value_types",
}

json_rules = {}
xml_rules = {}

class MapOf:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The map of data only
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
        if isinstance(self.data, list) or isinstance(self.data, dict):
            return
        else:
            raise ValueError(f"Data must be a list / dict / object / record that contains an iterable structure. Received: {type(self.data)}")
        
    def check_max_elements(self):
        if self.data is not None:
            if isinstance(self.data, list):
                if len(self.data) > self.j_config.MaxElements * 2:
                    raise ValueError(f"Data items exceed the maximum limit of {self.j_config.MaxElements}")
                
            if isinstance(self.data, dict):
                if len(self.data) > self.j_config.MaxElements:
                    raise ValueError(f"Data items exceed the maximum limit of {self.j_config.MaxElements}")                
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")

    def validate_type(self, jtype: Jadn_Type, data: any):
        
        clz_kwargs = dict(
            class_name=jtype.base_type,
            j_schema=self.j_schema,
            j_type=jtype,
            data=data,
            data_format=self.data_format
        )
        
        clz_instance = create_clz_instance(**clz_kwargs)
        clz_instance.validate()
            
    def check_for_duplicate_key(self, ktype: str, keys_set: set, key: any):
        try:
            sha_key = generate_sha256(key)
            keys_set.add(sha_key)
        except KeyError:
            raise ValueError(f"{ktype} contains duplicate key: {key}")
        
    def check_key_value_types(self):
        if self.data is None:
            if not is_optional(self.j_type):
                self.errors.append(f"Map of '{self.j_type.type_name}' missing data")
                
        ktype = get_ktype(self.j_type)
        vtype = get_vtype(self.j_type)
        
        ktype_user_defined = is_user_defined(ktype)
        vtype_user_defined = is_user_defined(vtype)
        
        ktype_obj = None
        if ktype_user_defined:
            ref_ktype = get_reference_type(self.j_schema, ktype)
            ktype_obj = build_j_type(ref_ktype)
            ktype = ktype_obj.base_type
        elif is_primitive(ktype):
            ktype_obj = Jadn_Type(self.j_type.type_name.lower() + "_" + ktype.lower(), ktype)
        else:
            raise ValueError(f"Invalid MapOf ktype: {ktype}")
        
        vtype_obj = None    
        if vtype_user_defined:
            ref_vtype = get_reference_type(self.j_schema, vtype)
            vtype_obj = build_j_type(ref_vtype)
            vtype = vtype_obj.base_type
        elif is_primitive(vtype):
            vtype_obj = Jadn_Type(self.j_type.type_name.lower() + "_" + vtype.lower(), vtype)            
        else:
            raise ValueError(f"Invalid MapOf vtype: {vtype}")
        
        # Data is JSON object / dict,  if ktype is a String or User Defined type
        #  {"key1": value1, "key2": value2, ...}.
        # vtypes must be primitive or user defined types
        # ktypes must be unique
        if ktype == Base_Type.STRING.value:
        
            keys_set = set()
            for data_key, data_val in self.data.items():
                self.check_for_duplicate_key(ktype, keys_set, data_key)
                self.validate_type(ktype_obj, data_key)
                
                if is_primitive(vtype) or vtype_user_defined:
                    self.validate_type(vtype_obj, data_val)
                else: 
                    raise ValueError(f"Invalid MapOf vtype, must be primitive or user defined.  Received: {type(vtype)}")
                
        # JSON array if ktype is not a String type
        # If ktype is int, then the data is a list of key-value pairs, as follows:
        #  [key1, value1, key2, value2, ...].
        # elif ktype in [Base_Type.INTEGER.value, Base_Type.NUMBER.value, Base_Type.BOOLEAN.value]:
        elif is_primitive(ktype) or ktype_user_defined:
        
            keys_set = set()
            for i, data_item in enumerate(self.data):
                kv_type = None
                
                if is_even(i):
                    self.check_for_duplicate_key(ktype, keys_set, data_item)
                    kv_type = ktype_obj
                else:
                    kv_type = vtype_obj
                
                self.validate_type(kv_type, data_item) 
                  
        else:
            raise ValueError(f"invalid mapof ktype: {ktype}")
        
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
