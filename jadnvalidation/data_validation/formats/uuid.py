import uuid

class Uuid:
    
    data: str = None
    
    def __init__(self, data: any = None):
        self.data = data
    
    def validate(self):
        if isinstance(self.data, str):
            try:
                value = uuid.UUID(self.data)  
            except ValueError:
                raise ValueError(f"Incorrect uuid string, Received {self.data}.")
            
        elif isinstance(self.data, bytes):
            try:
                val = self.data
                string_val = val.decode('utf-8', 'strict')
                value = uuid.UUID(string_val)  
            except ValueError:
                raise ValueError(f"Incorrect Binary uuid, Received {self.data}.")
            
        else:  
            raise ValueError(f"Incorrect uuid, Received {self.data}.")