from datetime import datetime
import re

from jadnvalidation.utils.consts import DURATION_FORMAT

class Duration:
    
    data: any = None
    #date_format: str = DURATION_FORMAT # RFC 3339 Duration Format
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        if isinstance(self.data,str):
            try:           
                match = re.fullmatch("^P(\d+Y)?(\d+M)?(\d+D)?(T(\d+H)?(\d+M)?(\d+S)?)?$", self.data, flags=0)
                print(str(match))
                if match:
                    pass
                else:
                    raise ValueError(f"Does not patch rfc3339 duration value: {self.data}.")
            except ValueError:
                raise ValueError(f"Invalid duration value: {self.data}. Expected a 'P' formatted periodic duration.")
        elif not isinstance(self.data, int): 
            raise ValueError(f"Invalid duration value: {self.data}. Expected an integer / number of seconds.")
        
  