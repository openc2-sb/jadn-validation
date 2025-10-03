class I8:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for i8, expected an Integer.  Received: {type(self.data)}.")
        
        """
        A 1-byte signed integer (using two's complement) has a range from -128 to 127. 
        This is because 8 bits allow for 256 distinct values, and with one bit used to represent 
        the sign (positive or negative), the remaining 7 bits can represent values from -128 to 127.         
        """
        if -128 <= self.data <= 127:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for an 8-bit or 1 byte signed integer.")