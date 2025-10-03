

class I32:
    
    data: any = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for i32, expected an Integer.  Received: {type(self.data)}.")
        
        """
        A 4-byte signed integer can hold values in the range of -2,147,483,648 to 2,147,483,647. 
        This is because a 32-bit signed integer uses one bit to represent the sign (positive or negative) 
        and the remaining 31 bits to represent the magnitude.       
        """
        if -2147483648  <= self.data <= 2147483647:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for an 32-bit or 4-byte signed integer.")