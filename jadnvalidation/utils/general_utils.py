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
    raise ValueError(f"Invalid regex pattern: {e}")
    
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

    module = importlib.import_module(modules.get(class_name))
    
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
    
    return formatted_class_name

def create_fmt_clz_instance(class_name: str, *args, **kwargs):
    
    modules = {
        "Date" : "jadnvalidation.data_validation.formats.date",
        "DateTime" : "jadnvalidation.data_validation.formats.date_time",
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
        "Language" : "jadnvalidation.data_validation.formats.language"
    }
    
    formatted_class_name = format_class_name(class_name)
    module = importlib.import_module(modules.get(formatted_class_name))
    
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

def is_even(n):
    return n % 2 == 0

def is_odd(n):
    return n % 2 != 0

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

def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)
