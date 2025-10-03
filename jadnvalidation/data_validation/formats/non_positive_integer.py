class NonPositiveInteger:
    
    data: any = None
    
    def __init__(self, data: any = None, date_format: any = None):
        self.data = data
    
    def validate(self):
        
        if not isinstance(self.data, int): 
            raise ValueError(f"Invalid type for Non Positive Integer, expected an Integer.  Received: {type(self.data)}.")
        
        '''
        A non positive integer has a range of [*, 0], inclusive.
        '''
        if self.data <= 0:
            pass
        else:
            raise ValueError(f"Data {self.data} is out of range for a non positive integer.")