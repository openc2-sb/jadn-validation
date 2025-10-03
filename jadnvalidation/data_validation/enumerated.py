from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Base_Type, Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance
from jadnvalidation.utils.mapping_utils import get_inheritance, is_derived_enumeration, use_field_ids
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "e": "check_inheritance", 
    "value": "check_enumeration",
}

json_rules = {
    "type": "json_check_type"
}

xml_rules = {
    "type": "xml_check_type"
}

class Enumerated:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The enumeration data only
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
 
    def build_derived_enumeration(self, derived_enum_val: str = None) -> Jadn_Type:
        return_j_type = self.j_type
        
        if derived_enum_val:
            ref_type = get_reference_type(self.j_schema, derived_enum_val)
            if ref_type is None:
                raise ValueError(f"Unknown derived enumeration type {derived_enum_val} referenced in {return_j_type.type_name}.")
            ref_type_obj = build_j_type(ref_type)
            
            if ref_type_obj.base_type in [Base_Type.ENUMERATED.value, Base_Type.MAP.value, Base_Type.RECORD.value, Base_Type.CHOICE.value]:
                # TODO: May need to remove dervived enum type from j_type options
                return_j_type.fields = ref_type_obj.fields           
            else:
                raise ValueError(f"Derived enumeration type {derived_enum_val} is not a valid enumeration type for {return_j_type.type_name}.")
        else:
            raise ValueError(f"Derived enumeration type not specified for {return_j_type.type_name}.") 
        
        return return_j_type
    
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
        
    def json_check_type(self):
        if self.data is not None:
            use_ids = use_field_ids(self.j_type.type_options)
            if use_ids:
                if not isinstance(self.data, int):
                    raise ValueError(f"Data for type {self.j_type.type_name} must be an integer. Received: {type(self.data)}")
            else:
                if not isinstance(self.data, str):
                    raise ValueError(f"Data for type {self.j_type.type_name} must be a string. Received: {type(self.data)}")
            
    def xml_check_type(self):
        if self.data is not None:
            use_ids = use_field_ids(self.j_type.type_options)
            if use_ids:
                if isinstance(self.data, str):
                    try:
                        self.data = int(self.data)
                    except ValueError as e:
                        raise ValueError(f"Unable to serialize data for type {self.j_type.type_name} into an type integer. Received: {type(self.data)}")
                
                if not isinstance(self.data, int):
                    raise ValueError(f"Data for type {self.j_type.type_name} must be of type integer. Received: {type(self.data)}")
            else:
                if not isinstance(self.data, str):
                    raise ValueError(f"Data for type {self.j_type.type_name} must be a string. Received: {type(self.data)}")            
            
    def check_enumeration(self):
        derived_enum_val = is_derived_enumeration(self.j_type.type_options)
        if derived_enum_val:
            self.j_type = self.build_derived_enumeration(derived_enum_val)
                
        use_ids = use_field_ids(self.j_type.type_options)
        
        j_field_match = None
        for j_key, j_field in enumerate(self.j_type.fields):
            
            if use_ids:
                if j_field[0] == self.data:
                    j_field_match = j_field
            else:
                if j_field[1] == self.data:
                    j_field_match = j_field
                
            if j_field_match is not None:
                break
        
        if j_field_match is None:
            raise ValueError(f"Data {self.data} not valid for Enumeration type '{self.j_type.type_name}'. ")
        
        enum_base_type = Base_Type.STRING.value
        if use_ids:
            enum_base_type = Base_Type.INTEGER.value
            
        enum_jtype = Jadn_Type(self.j_type.type_name, enum_base_type)
        
        clz_kwargs = dict(
            class_name=enum_base_type,
            j_schema=self.j_schema,
            j_type=enum_jtype,
            data=self.data,
            data_format=self.data_format
        )          
        
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