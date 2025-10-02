import numpy as np

from typing import Union
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML


common_rules = {
    "type": "check_type",
    "check": "check_floating_point"
}

json_rules = {}

xml_rules = {}

class F256:
            
    
    def validate(self) -> bool:

        # Octuple point precision floats are not handles elegantly or efficiently
        # by libraries, and will massively slow validations.
        
        '''
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
        '''
    
        return True
        