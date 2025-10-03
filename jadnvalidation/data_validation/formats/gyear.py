import re 
        
class GYear:
    
    data: any = None
    
    def __init__(self, data: any = None, date_format: any = None):
        if isinstance(data, str):
            self.data = data
        elif isinstance(data, int):
            self.data = str(data)
        else:
            raise ValueError(f"Invalid gYear type, must be an integer or string.  Received: {type(data)}")
        
    def validate(self):
        if self.data is not None:
            try:
                if re.fullmatch(r"-?([1-9][0-9]{3,}|0[0-9]{3})(Z|(\+|-)((0[0-9]|1[0-3]):[0-5][0-9]|14:00))?$", self.data, flags=0):
                    pass
                else: 
                    raise ValueError(f"Entry does not match gYear: {self.data}")  
            except ValueError:
                raise ValueError(f"Invalid gYear: {self.data}")