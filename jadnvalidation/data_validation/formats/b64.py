import base64


common_rules = {
    "type": "check_type",
    "check": "check_base64"
}

json_rules = {}

xml_rules = {}

class B64:
    data: any = None
    errors = []      

    def __init__(self, data: any = None):
        self.data = data
        self.errors = []
        
    def check_type(self):
        if self.data is not None:
            if not isinstance(self.data, bytes):
                self.errors.append(f"Expected type 'bytes' for base64 data, got '{type(self.data).__name__}'")
                
    def check_base64(self):
        if self.data is not None:
            try:
                # Try to decode the bytes as base64, then re-encode and compare
                decoded = base64.b64decode(self.data, validate=True)
                if base64.b64encode(decoded) != self.data:
                    self.errors.append("Base64 data is not properly padded or contains invalid characters.")
            except Exception as e:
                self.errors.append(f"Invalid base64 encoding: {str(e)}")
    
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
        
