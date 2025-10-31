common_rules = {}

json_rules = {}

xml_rules = {}

class Attr:
    data: any = None

    def __init__(self, data: any = None):
        self.data = data
        
    
    def validate(self) -> bool:
        # TODO: Attr is an xml format for xml attributes only.  Nothing to validate here yet.
        # Non validation logic is in the jadn-xml repo.  

        return True
        
