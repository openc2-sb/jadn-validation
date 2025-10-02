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

class F64:
    """
    F64 class for validating and converting 64-bit floating-point numbers.
    """
    
    j_schema: dict = {}
    j_config: Jadn_Config = None    
    j_type: Jadn_Type = None
    data: any = None
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
        if self.data is not None:   
            # if not isinstance(self.data, float) and not isinstance(self.data, decimal.Decimal):
            if not isinstance(self.data, float):
                raise ValueError(f"Data must be a float/number. Received: {type(self.data)}")
                
    def check_floating_point(self):
        """Checks if a float is within the range of an f64 (approximate).
        A floating-point number that is too large for float64 is a value exceeding the maximum 
        representable value for a 64-bit floating-point number, which is approximately 1.8 * 10^308. 
        Specifically, float64 can't store numbers larger than 1.7976931348623157E+308. 
        Any value greater than this will cause an overflow, resulting in an error. 
        """
        
        if self.data is not None:   
            
            # if isinstance(self.data, float):
            if np.isinf(self.data) or np.isnan(self.data):
                raise ValueError(f"Data {self.data} for Type {self.j_type.type_name} is not a valid 64-bit float representation.")

            f128_value = 0
            restored_value = 0
            try:
                f64_value = np.float128(self.data)
                restored_value = float(f128_value)
            except ValueError as e:
                raise ValueError(f"Unable to convert data {self.data} for Type {self.j_type.type_name} to float64 and back.")                
                
            # Use np.isclose for comparison to account for potential very small differences
            # due to floating point representation
            tolerance = 1e-6  # Adjust tolerance as needed
            if np.isclose(self.data, restored_value, rtol=tolerance, atol=tolerance):
                pass
            else:
                raise ValueError(f"Data {self.data} for Type {self.j_type.type_name} is out of range for 64-bit float representation.")
    
    def validate(self) -> bool:
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
        