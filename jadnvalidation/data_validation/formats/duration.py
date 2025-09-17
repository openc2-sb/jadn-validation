from datetime import datetime
from jadnvalidation.utils.consts import JSON, XML
import re

from jadnvalidation.utils.consts import DURATION_FORMAT

class Duration:
    
    data: any = None
    data_format: any = None
    
    def __init__(self, data: any = None, data_format: any = None):
        self.data = data
        self.data_format = data_format
    
    def validate(self):

        if isinstance(self.data, int):
                print(f"json int duration")
                return
        elif self.data_format == XML:
            try:
                temp = int(self.data)
                return
            except ValueError:
                raise ValueError(f"Invalid XML duration value: {self.data}")
        elif isinstance(self.data, str):
            try:           
                match = re.fullmatch("^P(\d+Y)?(\d+M)?(\d+D)?(T(\d+H)?(\d+M)?(\d+S)?)?$", self.data, flags=0)
                print(str(match))
                if match:
                    pass
                else:
                    raise ValueError(f"Does not patch rfc3339 duration value: {self.data}.")
            except ValueError:
                raise ValueError(f"Invalid duration value: {self.data}. Expected a 'P' formatted periodic duration.")
        else: 
            raise ValueError(f"Invalid duration value: {self.data}.")
        
  