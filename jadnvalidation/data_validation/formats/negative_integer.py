class NegativeInteger:
    
    data: any = None
    
    def __init__(self, data: any = None, date_format: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for Negative Integer, expected an Integer.  Received: {type(self.data)}.")
        
        '''
        A negative integer has a range of [*, 0), exclusive.
        '''
        if self.data < 0:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for a negative integer.")