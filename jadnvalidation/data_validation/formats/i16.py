class I16:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for i16, expected an Integer.  Received: {type(self.data)}.")
        
        """
        A 2-byte signed integer (16-bit) has a range of -32,768 to 32,767. 
        This is because one bit is used to represent the sign (positive or negative), 
        leaving 15 bits to represent the magnitude of the number.         
        """
        if -32768 <= self.data <= 32767:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for an 16-bit or 2-byte signed integer.")