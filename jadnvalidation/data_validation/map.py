from typing import Union

from jadnvalidation.models.jadn.jadn_type import build_jadn_type_obj, is_field_multiplicity
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_field_name, check_sys_char, check_type_name, get_j_config
from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, is_user_defined, is_primitive
from jadnvalidation.utils.consts import JSON, XML
from jadnvalidation.utils.general_utils import create_clz_instance, get_data_by_id, get_data_by_name, merge_opts
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_inheritance, get_max_length, get_max_occurs, get_min_length, get_min_occurs, get_tagged_data, is_optional, use_field_ids, use_alias, use_keyless_map, to_dict_on_given_char
from jadnvalidation.utils.type_utils import get_reference_type, get_schema_type_by_name
from jadnutils.utils.jadn_utils import get_inherited_fields

common_rules = {
    "type": "check_type",
    "e": "check_inheritance",    
    "{": "check_min_length",
    "}": "check_max_length",
    "fields": "check_fields",
    "extra_fields": "check_extra_fields"
}

json_rules = {}
xml_rules = {}

class Map:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The map data only
    data_format: str = None
    use_ids: bool = False
    errors = []
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.data_format = data_format         
        
        self.use_ids = use_field_ids(self.j_type.type_options)
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_type(self):
        """
        Validates that the data type matches the expected format.
        For keyless maps in JSON format, data must be a list.
        For regular maps, data must be a dict.
        """
        keyless_map_options = use_keyless_map(self.j_type.type_options)
        is_keyless_map = keyless_map_options is not None and self.data_format == JSON
        
        if is_keyless_map:
            if not isinstance(self.data, list):
                raise ValueError(f"Data for JSON Keyless Map must be a list. Received: {type(self.data)}")
        else:
            if not isinstance(self.data, dict):
                raise ValueError(f"Data must be a map / dict. Received: {type(self.data)}")
    
    def check_inheritance(self):
        inherit_from = get_inheritance(self.j_type.type_options)
        if inherit_from is not None:
            inherited_type = get_reference_type(self.j_schema, inherit_from)
            inherited_type_obj = build_j_type(inherited_type)

            if inherited_type is None:
                raise ValueError(f"Type {self.j_type.type_name} inherits from unknown type {inherit_from}")
            
            if self.j_type.base_type != inherited_type_obj.base_type:
                raise ValueError(f"Type {self.j_type.type_name} inherits from type {inherit_from} with different base type {inherited_type_obj.base_type}. Received: {self.j_type.base_type}")
            
            schema_types = self.j_schema.get('types', [])
            self_type = get_schema_type_by_name(schema_types, self.j_type.type_name)
            self.j_type.fields = get_inherited_fields(schema_types, self_type)
        
    def check_min_length(self):
        min_length = get_min_length(self.j_type)
        if min_length is not None and len(self.data) < min_length:
            self.errors.append(f"Number of fields must be greater than {min_length}. Received: {len(self.data)}")
        
    def check_max_length(self):
        max_length = get_max_length(self.j_type, self.j_config)
        if max_length is not None and len(self.data) > max_length:
            self.errors.append(f"Number of fields length must be less than {max_length}. Received: {len(self.data)}")
        
    def check_fields(self):
        funnyArray = []
        funnyArray = use_keyless_map(self.j_type.type_options)
        temp_map = {}

        if funnyArray is not None and self.data_format == JSON:
            alias_val = ''
            for val in self.data:
                if not isinstance(val, str):
                    raise TypeError(f'inparsable item in keyless map: {val}')
                dict_val = to_dict_on_given_char(val, funnyArray[1])
                #print(f"line value changed to {dict_val}")
                #print(f"{dict_val}")
                if list(dict_val.values()) == '':
                    dict_val = {list(dict_val.keys())[0] , True} 
                    #print("updated empty to bool true")
                temp_map.update(dict_val)
                
            #print(f"{temp_map}")

            presence_tracker = False
            field_count = len(self.j_type.fields)
            missing_fields = 0
            for j_key, j_field in enumerate(self.j_type.fields):
                j_field_obj = build_jadn_type_obj(j_field)

                if is_field_multiplicity(j_field_obj.type_options):
                    j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))

                merged_opts = []
                if is_user_defined(j_field_obj.base_type):
                    ref_type = get_reference_type(self.j_schema, j_field_obj.base_type) # if it references another map with these options this may need to be revisited
                    ref_type_obj = build_j_type(ref_type)
                    check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                    merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                    print(f"options: {merged_opts}")
                    #j_field_obj = ref_type_obj     #copied hastily;examining
                    j_field_obj.type_options = merged_opts        # we don't want this because it will permanently merge them down across fields

                field_data = None
                if self.use_ids:
                    field_data = get_data_by_id(temp_map, j_field_obj.id)
                    if field_data is not None:
                        presence_tracker = True
                elif use_alias(j_field_obj.type_options): # changed this and the next line to merged_options to wipe it every type
                    alias_val = use_alias(j_field_obj.type_options)
                    #print(f"found alias {alias_val}")
                    field_data = get_data_by_name(temp_map, alias_val)
                    if field_data is not None:
                        presence_tracker = True
                else:
                    field_data = get_data_by_name(temp_map, j_field_obj.type_name) 
                    #print(f"field_data is {field_data}, presence_tracker is {presence_tracker}")
                    if field_data is not None:
                        presence_tracker = True
                    #print(f"Checking for Key {j_field_obj.type_name}, found value {field_data}")
                
                #print(f"presence_tracker is {presence_tracker}")
                if presence_tracker is False:
                    missing_fields = missing_fields+1
                    if missing_fields >= field_count:
                        raise ValueError(f"unexpected item in bagging area") # put different error msg here later
                    
                if field_data is None:
                    if is_optional(j_field_obj):
                        continue
                    else:
                        raise ValueError(f"Field '{j_field_obj.type_name}' is missing from data")
                check_sys_char(j_field_obj.type_name, self.j_config.Sys)
                check_field_name(j_field_obj.type_name, self.j_config.FieldName)    

                if is_field_multiplicity(j_field_obj.type_options):
                    j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))

                if is_user_defined(j_field_obj.base_type):
                    ref_type = get_reference_type(self.j_schema, j_field_obj.base_type) # if it references another map with these options this may need to be revisited
                    ref_type_obj = build_j_type(ref_type)
                    check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                    merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                    j_field_obj = ref_type_obj     # copied hastily; think this needs to go
                    j_field_obj.type_options = merged_opts
                    
                    #print(f"field type is : {j_field_obj.base_type}")
                    #basetype assumed String, and is starting as a split string
                    if j_field_obj.base_type=="Integer":
                        #add format checks later
                        field_data = int(field_data)
                        #print(f"field data changed to {field_data}")
                    if j_field_obj.base_type=="Number":
                        #add format checks later
                        field_data = float(field_data)
                        #print(f"field data changed to {field_data}")
                    if j_field_obj.base_type=="Boolean":
                        field_data = bool(field_data)
                        #print(f"field data changed to {field_data}")
                    # i can't see a current example on Binary we can address that if/when we have clarification

                    tagged_data = get_tagged_data(j_field_obj, self.data)
                    
                    clz_kwargs = dict(
                        class_name=j_field_obj.base_type,
                        j_schema=self.j_schema,
                        j_type=j_field_obj,
                        data=field_data,
                        data_format=self.data_format
                    )
                    if tagged_data is not None:
                        clz_kwargs['tagged_data'] = tagged_data

                    clz_instance = create_clz_instance(**clz_kwargs)
                    clz_instance.validate()

                elif is_primitive(j_field_obj.base_type):
                    
                    #print(f"field type is : {j_field_obj.base_type}")
                    #basetype assumed String, and is starting as a split string
                    if j_field_obj.base_type=="Integer":
                        #add format checks later
                        field_data = int(field_data)
                        #print(f"field data changed to {field_data}")
                    if j_field_obj.base_type=="Number":
                        #add format checks later
                        field_data = float(field_data)
                        #print(f"field data changed to {field_data}")
                    if j_field_obj.base_type=="Boolean":
                        field_data = bool(field_data)
                        #print(f"field data changed to {field_data}")
                    # i can't see a current example on Binary we can address that if/when we have clarification

                    tagged_data = get_tagged_data(j_field_obj, self.data)
                    
                    clz_kwargs = dict(
                        class_name=j_field_obj.base_type,
                        j_schema=self.j_schema,
                        j_type=j_field_obj,
                        data=field_data,
                        data_format=self.data_format
                    )
                    if tagged_data is not None:
                        clz_kwargs['tagged_data'] = tagged_data

                    #print(f"{j_field_obj.type_name}")
                    clz_instance = create_clz_instance(**clz_kwargs)
                    clz_instance.validate()


        else:
            for j_key, j_field in enumerate(self.j_type.fields):
                j_field_obj = build_jadn_type_obj(j_field)
                alias_val = ''

                if is_field_multiplicity(j_field_obj.type_options):
                    j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))

                field_data = None
                if self.use_ids:
                    field_data = get_data_by_id(self.data, j_field_obj.id)
                elif use_alias(j_field_obj.type_options):
                    alias_val = use_alias(j_field_obj.type_options)
                    field_data = get_data_by_name(self.data, alias_val)
                else:
                    field_data = get_data_by_name(self.data, j_field_obj.type_name)                
                
                if field_data is None:
                    if is_optional(j_field_obj):
                        continue
                    else:
                        raise ValueError(f"Field '{j_field_obj.type_name}' is missing from data")
                    
                check_sys_char(j_field_obj.type_name, self.j_config.Sys)
                check_field_name(j_field_obj.type_name, self.j_config.FieldName)                

                if is_field_multiplicity(j_field_obj.type_options):
                    j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))

                if is_user_defined(j_field_obj.base_type):
                    ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                    ref_type_obj = build_j_type(ref_type)
                    check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                    merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                    j_field_obj = ref_type_obj
                    j_field_obj.type_options = merged_opts
                    
                tagged_data = get_tagged_data(j_field_obj, self.data)
                    
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=field_data,
                    data_format=self.data_format
                )
                if tagged_data is not None:
                    clz_kwargs['tagged_data'] = tagged_data

                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()
                 
    def check_extra_fields(self):
        # Check if data has any unknown fields
        if self.data is not None:
            
            if len(self.data) > len(self.j_type.fields):
                raise ValueError(f"Data has more fields ({len(self.data)}) than allowed ({len(self.j_type.fields)})")
            if not use_keyless_map(self.j_type.type_options): #check to see if this needs a counter-case
                for data_key in self.data.keys():
                    is_found = False
                    print(f"{self.j_type.type_options}")
                    for j_field in self.j_type.fields:
                        print(f"{self.j_type}")
                        if self.use_ids:
                            if data_key == str(j_field[0]):
                                is_found = True

                        
                        elif len(j_field) > 2 and is_user_defined(j_field[2]):
                            
                            ref_type = get_reference_type(self.j_schema, j_field[2])
                            ref_type_obj = build_j_type(ref_type)
                            check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                            merged_opts = merge_opts(self.j_type.type_options, ref_type_obj.type_options)
                            print(f"merged options: {merged_opts}")

                            if use_alias(merged_opts):
                                alias_val = use_alias(merged_opts)
                                if data_key == alias_val:
                                    is_found = True
                            elif data_key == j_field[1]:
                                is_found = True
                        elif use_alias(self.j_type.type_options):
                            alias_val = use_alias(self.j_type.type_options)
                            print(f"alias: {alias_val}")
                            if data_key == alias_val:
                                is_found = True
                        elif data_key == j_field[1]:
                            is_found = True
                            
                    if not is_found:
                        raise ValueError(f"Data field '{data_key}' is not defined in schema")
            
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
