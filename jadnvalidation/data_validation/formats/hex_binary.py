import re

common_rules = {
    "type": "check_type",
    "check": "check_hex_binary"
}

json_rules = {}

xml_rules = {}

class HexBinary:
    data: any = None
    errors = []      

    def __init__(self, data: any = None):
        self.data = data
        self.errors = []
        
    def check_type(self):
        if self.data is not None:
            if not isinstance(self.data, (str, bytes)):
                self.errors.append(f"Expected type 'str' or 'bytes' for hex binary data, got '{type(self.data).__name__}'")
                
    def check_hex_binary(self):
        if self.data is not None:
            if not isinstance(self.data, (bytes, str)):
                self.errors.append(f"Expected type 'bytes' or 'str' for hex binary data, got '{type(self.data).__name__}'")
                return
            # Convert bytes to string for validation
            hex_str = self.data.decode() if isinstance(self.data, bytes) else self.data

            if not re.fullmatch(r'[0-9A-Fa-f]*', hex_str):
                self.errors.append("Data is not valid hex binary (should only contain 0-9, a-f, A-F).")
            elif len(hex_str) % 2 != 0:
                self.errors.append("Hex binary data must have an even number of characters.")
    
    def validate(self) -> bool:
        # Check data against rules
        rules = json_rules
        # if self.data_format == XML:
        #     rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True
        
