from jadnvalidation.models.jadn.jadn_config import Jadn_Config, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance
from jadnvalidation.utils.mapping_utils import is_optional
        
        
common_rules = {
    "type": "check_type",
    "length": "check_length",
    "fields": "check_data"
}

json_rules = {}
xml_rules = {}        
        
class Ipv6Net:
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Jadn_Type = None
    data: any = None
    data_format: str = None    
    errors = []     
    
    def __init__(self, j_schema: dict = {}, j_type: Jadn_Type = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format          
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def build_j_type_ipv6_addr(self) -> Jadn_Type:
        jadn_type_obj = Jadn_Type(
                type_name="ipv6_addr", 
                base_type="Binary", 
                type_options=["/ipv6-addr", "{1", "[1"], 
                type_description="IPv6 address as defined in [[RFC8200]](#rfc8200)",
                fields=[])
        
        return jadn_type_obj
    
    def build_j_type_prefix_length(self) -> Jadn_Type:
        jadn_type_obj = Jadn_Type(
                type_name="prefix_length", 
                base_type="Integer", 
                type_options=["{0", "}128", "[0"], 
                type_description="CIDR prefix-length. If omitted, refers to a single host address.",
                fields=[])
        
        return jadn_type_obj   
    
    def check_type(self):
        if self.data_format == JSON:
            if not isinstance(self.data, str):
                raise ValueError(f"Data for type {self.j_type.type_name} must be JSON String. Received: {type(self.data)}")
            else: 
                self.data = self.data.split("/") 
                self.data[0] = (self.data[0]) 
                self.data[1] = (int(self.data[1])) 
                print(self.data) 
                try:
                    if self.data[2]: 
                        raise ValueError(f"incorrectly formatted network. Received: {(self.data)}") 
                    else: 
                        pass
                except IndexError as e:
                    print('correctly formatted ip-net')
                
                    
        elif not isinstance(self.data, list):
            raise ValueError(f"Data for type {self.j_type.type_name} not a list. Received: {type(self.data)}")                
           
    def check_length(self):
        if self.data is None:
            if not is_optional(self.j_type):
                raise ValueError(f"Missing required data for type {self.j_type.type_name}")
        else:            
            list_length = len(self.data)
            if list_length < 1: 
                raise ValueError(f"Data for type {self.j_type.type_name} must have at least 1 element (ipv6_addr). Received: {list_length}")
            
            if list_length > 2: 
                raise ValueError(f"Data for type {self.j_type.type_name} must be no larger than 2 elements (ipv6_addr & prefix length). Received: {list_length}")          
            
            
    def check_data(self):
        j_type_ipv6_addr = self.build_j_type_ipv6_addr()
        j_type_prefix_length = self.build_j_type_prefix_length()
        
        for j_index, field_data in enumerate(self.data):  
                
            clz_kwargs = dict(
                j_schema=self.j_schema,
                data=field_data,
                data_format=self.data_format
            )                 
                
            if j_index == 0:
                
                clz_kwargs['class_name'] = j_type_ipv6_addr.base_type
                clz_kwargs['j_type'] = j_type_ipv6_addr                   
                
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()
                
            elif j_index == 1:
                
                if field_data is not None:
                    
                    clz_kwargs['class_name'] = j_type_prefix_length.base_type
                    clz_kwargs['j_type'] = j_type_prefix_length                    
                    
                    clz_instance = create_clz_instance(**clz_kwargs)
                    clz_instance.validate()             
    
    def validate(self):
      # Check data against rules
        rules = json_rules
        if self.data_format == XML:
            rules = xml_rules
       
       # Data format specific rules
        for key, function_name in rules.items():
            getattr(self, function_name)()
            
        # Common rules across all data formats
        for key, function_name in common_rules.items():
            getattr(self, function_name)()            
            
        if len(self.errors) > 0:
            raise ValueError(self.errors)  
        
        return True    