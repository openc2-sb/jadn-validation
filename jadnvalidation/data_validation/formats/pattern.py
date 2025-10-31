
from jadnvalidation.utils.general_utils import create_regex, search_string


class Pattern:
    
    data: str = None
    pattern_string: str = None
    
    def __init__(self, data: any = None, pattern_string: any = None):
        self.data = data
        self.pattern_string = pattern_string
    
    def validate(self):
        dynamic_regex = create_regex(self.pattern_string)
        result = search_string(dynamic_regex, self.data)

        if not result:
            raise ValueError(f"Match not found for pattern: {self.pattern_string}  Data: {self.data}")