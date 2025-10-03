

class I64:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for i64, expected an Integer.  Received: {type(self.data)}.")
        
        """
        A signed integer of 8 bytes, often referred to as a long long or INT64, 
        can represent numbers within the range of -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807.      
        """
        if -9223372036854775808 <= self.data <= 9223372036854775807:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for an 64-bit or 8-byte signed integer.")