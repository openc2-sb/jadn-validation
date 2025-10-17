import re
from jadnvalidation.utils.general_utils import get_nested_value


ROOT_GLOBAL_CONFIG_KEY = "root_global_config"
GLOBAL_CONFIG_KEY = "global_config"
TYPE_OPTS_KEY = "type_opts"
ARRAY_TYPE_OPTS_KEY = "array_type_opts"

MAX_BINARY_KEY = "$MaxBinary"
MAX_STRING_KEY = "$MaxString"
MAX_ELEMENTS_KEY = "$MaxElements"
SYS_IND_KEY = "$Sys"
TYPE_NAME_KEY = "$TypeName"
FIELD_NAME_KEY = "$FieldName"
NSID_KEY = "$NSID"
CONFIG_KEYS = [MAX_BINARY_KEY, MAX_STRING_KEY, MAX_ELEMENTS_KEY, SYS_IND_KEY, TYPE_NAME_KEY, FIELD_NAME_KEY, NSID_KEY]

DEFAULT_MAX_BINARY = 255
DEFAULT_MAX_STRING = 255
DEFAULT_MAX_ELEMENTS = 100
DEFAULT_SYS_IND = "$"
DEFAULT_TYPE_NAME_REGEX = "^[A-Z][-$A-Za-z0-9]{0,63}$"
# DEFAULT_FIELD_NAME_REGEX = "^[a-z][_A-Za-z0-9]{0,63}$"
DEFAULT_FIELD_NAME_REGEX = "^[A-Za-z][-_A-Za-z0-9]{0,63}$"
DEFAULT_NSID_REGEX = "^[A-Za-z][A-Za-z0-9]{0,7}$"

class Jadn_Config():
    MaxBinary: int = DEFAULT_MAX_BINARY
    MaxString: int = DEFAULT_MAX_STRING
    MaxElements: int = DEFAULT_MAX_ELEMENTS
    Sys: str = DEFAULT_SYS_IND
    TypeName: str = DEFAULT_TYPE_NAME_REGEX
    FieldName: str = DEFAULT_FIELD_NAME_REGEX
    NSID: str = DEFAULT_NSID_REGEX
    
    def __init__(self, MaxBinary = DEFAULT_MAX_BINARY, MaxString = DEFAULT_MAX_STRING, MaxElements = DEFAULT_MAX_ELEMENTS, Sys = DEFAULT_SYS_IND, TypeName = DEFAULT_TYPE_NAME_REGEX, FieldName = DEFAULT_FIELD_NAME_REGEX, NSID = DEFAULT_NSID_REGEX):
        self.MaxBinary = MaxBinary
        self.MaxString = MaxString    
        self.MaxElements = MaxElements    
        self.Sys = Sys
        self.TypeName = TypeName
        self.FieldName = FieldName
        self.NSID = NSID
        
def build_jadn_config_obj(j_config_data: dict) -> Jadn_Config:
    if j_config_data == None:
        j_config_data = {}
    
    j_config_obj = Jadn_Config(
        FieldName=j_config_data.get(FIELD_NAME_KEY, DEFAULT_FIELD_NAME_REGEX),
        MaxBinary=j_config_data.get(MAX_BINARY_KEY, DEFAULT_MAX_BINARY),
        MaxElements=j_config_data.get(MAX_ELEMENTS_KEY, DEFAULT_MAX_ELEMENTS),
        MaxString=j_config_data.get(MAX_STRING_KEY, DEFAULT_MAX_STRING),
        NSID=j_config_data.get(NSID_KEY, DEFAULT_NSID_REGEX),
        Sys=j_config_data.get(SYS_IND_KEY, DEFAULT_SYS_IND)
    )
    
    return j_config_obj

def get_j_config(j_schema: dict) -> Jadn_Config:
    j_config = Jadn_Config()
    
    j_custom_config = get_nested_value(j_schema, ['meta', 'config'], None)
    if j_custom_config:
        j_config = build_jadn_config_obj(j_custom_config)
    
    return j_config

def check_sys_char(j_field_name, j_config_sys: str):
    if j_config_sys and j_config_sys in j_field_name:
        if not j_field_name in CONFIG_KEYS:
            raise ValueError(f"Field Name {j_field_name} contains System Character {j_config_sys}")

def check_type_name(j_type_name, j_config_type_name_reg: str):
    match = re.fullmatch(j_config_type_name_reg, j_type_name)
    if not match:
        raise ValueError(f"Invalid Type Name {j_type_name} per regex pattern {j_config_type_name_reg}")    
    
def check_field_name(j_field_name, j_config_field_name_reg: str):
    match = re.fullmatch(j_config_field_name_reg, j_field_name)
    if not match:
        raise ValueError(f"Invalid Field Name {j_field_name} per regex pattern {j_config_field_name_reg}")        