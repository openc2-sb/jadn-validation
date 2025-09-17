import re  

class YearMonthDuration:
    
    # Allow different formats?  See date.py
    date_str: str = None
    #datetime_converted: datetime = None
    
    def __init__(self, date_entry: any = None, date_format: any = None):
        if isinstance(date_entry, str):
            self.date_str = date_entry
        else:
            raise ValueError(f"Invalid date-time format: {date_entry}")
    
    def validate(self):
        """
        Validates if a string conforms to the relevant subsection of ISO 8601.
        """
        if self.date_str:
            try:
                if re.fullmatch("^-?P((([0-9]+Y)([0-9]+M)?)|([0-9]+M))$", self.date_str, flags=0): 
                    pass
                else: 
                    raise ValueError(f"Entry does not match yearMonthDuration: {self.date_str}")  
            except ValueError:
                raise ValueError(f"Invalid yearMonthDuration: {self.date_str}")        
        else: 
            raise ValueError(f"Could not parse yearMonthDuration")