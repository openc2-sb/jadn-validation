import hashlib
import json
import re
import sys
import importlib

from typing import Callable, Union

def addKey(d: dict, k: str = None) -> Callable:
    """
    Decorator to append a function to a dict, referencing the function name or given key as the key in the dict
    :param d: dict to append the key/func onto
    :param k: key to use on the dict
    :return: original function
    """
    def wrapped(fun: Callable, key: str = k) -> Callable:
        d[key if key else fun.__name__] = fun
        return fun
    return wrapped

def all_unique(lst):
  return len(lst) == len(set(lst))

def create_regex(pattern_string):
  try:
    return re.compile(pattern_string)
  except re.error as e:
    raise ValueError(f"Invalid regex pattern: {e}. cannot create regex {pattern_string}")

def is_none(field_data):
    """
    Check if field_data is None or equivalent to missing/undefined values.
    Returns True if the data is None, empty list, or empty dict.
    Note: Empty string ('') is considered a valid value, not a missing value.
    """
    return field_data is None #or field_data == [] or field_data == {}
    # empty arrays are not None data in JADN
    
# (class_name, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None)
def create_clz_instance(class_name: str, *args, **kwargs):
    modules = {
        "Array" : "jadnvalidation.data_validation.array",
        "ArrayOf" : "jadnvalidation.data_validation.array_of",
        "Binary" : "jadnvalidation.data_validation.binary",
        "Boolean" : "jadnvalidation.data_validation.boolean",
        "Choice" : "jadnvalidation.data_validation.choice",
        "Enumerated" : "jadnvalidation.data_validation.enumerated",
        "Integer" : "jadnvalidation.data_validation.integer",
        "Map" : "jadnvalidation.data_validation.map",
        "MapOf" : "jadnvalidation.data_validation.map_of",
        "Number" : "jadnvalidation.data_validation.number",
        "Record" : "jadnvalidation.data_validation.record",
        "String" : "jadnvalidation.data_validation.string"
    }

    module_name = modules.get(class_name)
    if module_name is None:
        raise ValueError(f"Unknown data type: {class_name}")
    
    module = importlib.import_module(module_name)
    
    if module == None:
        raise ValueError("Unknown data type")
    
    cls = getattr(module, class_name)
    
    return cls(*args, **kwargs)

def format_class_name(class_name: str) -> str:
    """
    Formats the class name by converting it to camelCase and then to titleCase.
    Removes '_' and '-' characters in the process.
    """
    # Remove '_' and '-' and split into words
    words = class_name.replace("_", " ").replace("-", " ").split()
   
    # Title each word and concatenate them into one word
    formatted_class_name = ''.join(word[0].upper() + word[1:] for word in words)
    if formatted_class_name == 'JsonPointer':
        formatted_class_name = 'JadnJsonPointer'
    if formatted_class_name == 'Base64Binary':
        formatted_class_name = 'B64'
    if formatted_class_name == 'X':
        formatted_class_name = 'HexBinary'
    if formatted_class_name == 'Float':
        formatted_class_name = 'F32'
    if formatted_class_name == 'Double':
        formatted_class_name = 'F64'
    
    return formatted_class_name

def create_fmt_clz_instance(class_name: str, *args, **kwargs):
    
    modules = {
        "Attr" : "jadnvalidation.data_validation.formats.attr",
        "Date" : "jadnvalidation.data_validation.formats.date",
        "DateTime" : "jadnvalidation.data_validation.formats.date_time",
        "Duration" : "jadnvalidation.data_validation.formats.duration",
        "DayTimeDuration" : "jadnvalidation.data_validation.formats.daytimeduration",
        "YearMonthDuration" : "jadnvalidation.data_validation.formats.yearmonthduration",
        "Time" : "jadnvalidation.data_validation.formats.time",
        "Ipv4" : "jadnvalidation.data_validation.formats.ipv4",
        "Ipv4Addr" : "jadnvalidation.data_validation.formats.ipv4",
        "Ipv4Net" : "jadnvalidation.data_validation.formats.ipv4net",
        "Ipv6" : "jadnvalidation.data_validation.formats.ipv6",
        "Ipv6Addr" : "jadnvalidation.data_validation.formats.ipv6",
        "Ipv6Net" : "jadnvalidation.data_validation.formats.ipv6net",
        "Email" : "jadnvalidation.data_validation.formats.email",
        "Hostname" : "jadnvalidation.data_validation.formats.hostname",
        "IdnEmail" : "jadnvalidation.data_validation.formats.idn_email",
        "IdnHostname" : "jadnvalidation.data_validation.formats.idn_hostname",
        "Eui" : "jadnvalidation.data_validation.formats.eui",
        "F16" : "jadnvalidation.data_validation.formats.f16",
        "F32" : "jadnvalidation.data_validation.formats.f32",
        "F64" : "jadnvalidation.data_validation.formats.f64",
        "F128" : "jadnvalidation.data_validation.formats.f128",
        "F256" : "jadnvalidation.data_validation.formats.f256",
        "NonNegativeInteger" : "jadnvalidation.data_validation.formats.non_negative_integer",
        "PositiveInteger" : "jadnvalidation.data_validation.formats.positive_integer",
        "NonPositiveInteger" : "jadnvalidation.data_validation.formats.non_positive_integer",
        "NegativeInteger" : "jadnvalidation.data_validation.formats.negative_integer",
        "Pattern" : "jadnvalidation.data_validation.formats.pattern",
        "Regex" : "jadnvalidation.data_validation.formats.regex",
        "RelativeJsonPointer" : "jadnvalidation.data_validation.formats.relative_json_pointer",
        "JadnJsonPointer" : "jadnvalidation.data_validation.formats.json_pointer",
        "Iri" : "jadnvalidation.data_validation.formats.iri",
        "IriReference" : "jadnvalidation.data_validation.formats.iri_ref",
        "Uri" : "jadnvalidation.data_validation.formats.uri",
        "UriReference" : "jadnvalidation.data_validation.formats.uri_ref",
        "UriTemplate" : "jadnvalidation.data_validation.formats.uri_template",
        "Token" : "jadnvalidation.data_validation.formats.token",
        "Name" : "jadnvalidation.data_validation.formats.name",
        "QName" : "jadnvalidation.data_validation.formats.qname",
        "NormalizedString" : "jadnvalidation.data_validation.formats.normalized_string",
        "Language" : "jadnvalidation.data_validation.formats.language",
        "GYear" : "jadnvalidation.data_validation.formats.gyear",
        "GYearMonth" : "jadnvalidation.data_validation.formats.gyearmonth",
        "GMonthDay" : "jadnvalidation.data_validation.formats.gmonthday",
        "SignedInteger" : "jadnvalidation.data_validation.formats.signed_integer",
        "UnsignedInteger" : "jadnvalidation.data_validation.formats.unsigned_integer",
        "TaggedList" : "jadnvalidation.data_validation.formats.tagged_list",
        "HexBinary" : "jadnvalidation.data_validation.formats.hex_binary",
        "B64" : "jadnvalidation.data_validation.formats.b64",
        "Uuid" : "jadnvalidation.data_validation.formats.uuid",
    }
    
    formatted_class_name = format_class_name(class_name)
    
    module = None
    try:
        module = importlib.import_module(modules.get(formatted_class_name))
    except Exception as e:
        print(f"Error importing module for format '{formatted_class_name}': {e}", file=sys.stderr)
    
    if module == None:
        raise ValueError("Unknown format type")
    
    cls = getattr(module, formatted_class_name)
    
    return cls(*args, **kwargs)

def convert_binary_to_hex(binary_string):
    """Converts a binary string to its hexadecimal representation."""

    return hex(int(binary_string, 2))[2:]  # [2:] removes the '0x' prefix

def convert_list_to_dict(lst):
    res_dict = {}
    for i in range(0, len(lst), 2):
        res_dict[lst[i]] = lst[i + 1]
    return res_dict

def create_dynamic_union(*types):
    return Union[types]

def generate_sha256(data):
    """
    Generates a SHA256 hash of any variable type.

    Args:
        data: The variable to hash.

    Returns:
        The SHA256 hash as a hexadecimal string.
    """
    data_type = type(data)
    
    if data_type in (int, float, bool):
        data_string = str(data)
    elif data_type == str:
      data_string = data
    elif data_type in (list, dict, tuple):
        data_string = json.dumps(data, sort_keys=True)
    elif data is None:
        data_string = 'None'
    else:
        data_string = str(data)

    encoded_data = data_string.encode('utf-8')
    sha256_hash = hashlib.sha256(encoded_data).hexdigest()
    return sha256_hash

def get_data_by_id(data: dict, id: int):
    return data.get(str(id))

def get_data_by_name(data: dict, name: str):
    return data.get(name)

def get_err_msgs(err: ValueError, err_list: list = []):
    
    if isinstance(err, ValueError):
        
        if isinstance(err.args, ValueError):
            get_err_msgs(err.args[0], err_list)
            
        elif isinstance(err.args, tuple):
            for arg in err.args:
                if isinstance(arg, ValueError):
                    get_err_msgs(arg, err_list)
                else:
                    err_list.append(str(arg))
                    
        elif isinstance(err.args, list):
            for arg in err.args:
                if isinstance(arg, ValueError):
                    get_err_msgs(arg, err_list)
                else:
                    err_list.append(str(arg))
                    
        elif isinstance(err.args, dict):
            for key, value in err.args.items():
                if isinstance(value, ValueError):
                    get_err_msgs(value, err_list)
                else:
                    err_list.append(f"{key}: {value}")
                    
        elif isinstance(err.args, str):
            err_list.append(err.args)
         
        else:
            err_list.append(str(err))    
        
    elif hasattr(err, 'args') and len(err.args) > 0:
        err_list.append(err.args[0])
        
    else:
        err_list.append(err)
       
    return "\n".join(err_list)

def get_item_safe_check(my_list, index):
    if 0 <= index < len(my_list):
        return my_list[index]
    return None  # Or any other default value

def get_choice_data_content(data: dict):
    '''
    Choice Data Example:
        "Choice-Name": {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True
        }
    '''
    return_val = None
    if isinstance(data, dict):        
        first_key = next(iter(data))
        if first_key:
            data_content = data.get(first_key)
            if isinstance(data_content, dict):
                return_val = data_content
                
    return return_val

def get_j_field(j_field_list, data_key, is_using_ids):
    j_field_found = None
    
    for j_field in j_field_list:
        if is_using_ids:
            if j_field[0] == int(data_key):
                j_field_found = j_field
                break
        else:
            if j_field[1] == data_key:
                j_field_found = j_field
                break
            
    return j_field_found             
        
def get_map_of_data_content(data: dict):
    '''
    MapOf Data Example:
        {
            "Root-Test": [1, "asdf", 2, "fdsaf"]
        }
    '''
    return_val = None
    if isinstance(data, dict):        
        first_key = next(iter(data))
        if first_key:
            data_content = data.get(first_key)
            if isinstance(data_content, list):
                return_val = data_content
            elif isinstance(data_content, dict):
                return_val = data_content
                
    return return_val

def get_nested_value(data, keys, default=None):
    """
    Safely retrieves a value from a nested dictionary given a list of keys.

    Args:
        data (dict): The dictionary to search within.
        keys (list): A list of keys representing the path to the desired value.
        default: The value to return if the key path doesn't exist. Defaults to None.

    Returns:
        The value at the specified path or the default value if not found.
    """
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return default
    return current

def give_format_constraint(format: str, option_index: int):
    # the frankenstein logic from before was a larger version of this; its moved into the formats now, 
    # but if you want one here, itll be like this

    format_designator, designated_value = split_on_first_char(format)    
    # if you need to differentiate by format designator: a holdover         
    try:
        unsigned_value = int(designated_value)
        print("uN value is 2^"+str(unsigned_value))
        unsig_min = 0
        unsig_max = pow(2,unsigned_value)
        struct = [unsig_min, unsig_max]
        return struct[option_index]
    except ValueError as e:
        print("u<n> format requires a numeric component following unsigned signifier \"u\". \n"+e)

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

def is_arg_format(format):
    if format:
        split_format = split_on_first_char(format)
        if (split_format[0] in ["i", "u"]) & ((split_format[1]).isdigit()):
            return True
    else: return False
        
def merge_opts(opts1: list, opts2: list) -> list:
    """
    Merge two lists of option strings, ensuring each item in the result has a unique first character.
    If duplicates (by first character) are found, the first occurrence is kept and the duplicate is logged and removed.

    Args:
        opts1 (list): First list of option strings.
        opts2 (list): Second list of option strings.

    Returns:
        list: Merged list with unique first characters.
    """
    merged = []
    seen = {}
    duplicates = []

    for opt in (opts1 or []) + (opts2 or []):
        if not opt:
            continue
        first_char = opt[0]
        if first_char not in seen:
            seen[first_char] = opt
            merged.append(opt)
        else:
            duplicates.append(opt)
    # hiding this popup; can be replaced later
    #if duplicates:
        #print(f"[merge_opts] Duplicate opts removed (by first char): {duplicates}")

    return merged

def safe_get(lst, index, default=None):
    """Safely get an item from a list at a given index.

    Args:
        lst: The list to access.
        index: The index to retrieve.
        default: The value to return if the index is out of range.

    Returns:
        The item at the given index, or the default value if the index is out of range.
    """
    try:
        return lst[index]
    except IndexError:
        return default
    
def search_string(regex_pattern, text):
  """Searches a string for the regex pattern and returns the result."""
  if regex_pattern:
    match = regex_pattern.search(text)
    if match:
      return match.group()
    else:
      return None
  return None    

def split_on_first_char(string):
    """Splits a string on the first character."""

    if not string:
        return []

    return [string[0], string[1:]]

def split_on_second_char(string):
    """Splits a string on the second character."""

    if not string:
        return []

    return [string[:2], string[2:]]

def split_on_given_char(string:str, pos:int) -> list:
    """Splits a string on the provided character."""

    if not string:
        return []
    first_part = string[:int(pos)]
    second_part = string[int(pos):]

    holding_list:list = [first_part, second_part]
    return holding_list

def sort_array_by_id(j_array: list, j_array2: list = None, is_allow_dups: bool = False) -> list:
    """
    Orders an array of JADN field definitions by their ID (first element of each field definition).
    If a second array is provided, combines both arrays before ordering.
    If is_allow_dups is False, raises a ValueError if duplicate IDs are found.

    Args:
        j_array (list): List of JADN field definitions, where each field is a list and the first element is the ID.
        j_array2 (list, optional): Second list of JADN field definitions to combine with the first.
        is_allow_dups (bool, optional): Whether to allow duplicate IDs. Defaults to False.

    Returns:
        list: The combined input lists ordered by the ID in ascending order.

    Raises:
        ValueError: If duplicate IDs are found and is_allow_dups is False.
    """
    combined = (j_array or []) + (j_array2 or [])
    ids = [x[0] for x in combined if isinstance(x, list) and len(x) > 0]
    if not is_allow_dups:
        seen = set()
        dups = set()
        for id_ in ids:
            if id_ in seen:
                dups.add(id_)
            else:
                seen.add(id_)
        if dups:
            raise ValueError(f"Duplicate IDs found in combined array: {sorted(dups)}")
    return sorted(combined, key=lambda x: x[0] if isinstance(x, list) and len(x) > 0 else float('inf'))

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
