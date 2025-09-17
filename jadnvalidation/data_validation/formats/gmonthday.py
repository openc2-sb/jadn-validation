import re  
        
class GMonthDay:
    
    data: any = None
    
    def __init__(self, data: any = None, date_format: any = None):
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, int):
            self.data = str(data)
        else:
            raise ValueError(f"Invalid gMonthDay type, must be an integer or string.  Received: {type(data)}")
    
    def validate(self):
        if self.data is not None:
            try:
                if re.fullmatch("^--(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?$", self.data, flags=0): 
                    pass
                else: 
                    raise ValueError(f"Entry does not match gMonthDay: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid gMonthDay: {self.data}")