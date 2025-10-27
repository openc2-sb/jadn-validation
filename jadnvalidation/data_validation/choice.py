from typing import Union

from jadnvalidation.models.jadn.jadn_type import Jadn_Type, build_j_type, build_jadn_type_obj, is_field_multiplicity, is_primitive, is_user_defined
from jadnvalidation.models.jadn.jadn_config import Jadn_Config, check_field_name, check_sys_char, check_type_name, get_j_config
from jadnvalidation.utils.general_utils import create_clz_instance, get_j_field, merge_opts
from jadnvalidation.utils.mapping_utils import flip_to_array_of, get_choice_type, get_inheritance, get_max_occurs, get_min_occurs, is_logical_not, use_field_ids
from jadnvalidation.utils.consts import JSON, XML, Choice_Consts
from jadnvalidation.utils.type_utils import get_reference_type

common_rules = {
    "e": "check_inheritance", 
    # "type": "check_type",
    # "&": "check_tagID",
    "choice": "check_choice"
}

json_rules = {}
xml_rules = {}

class Choice:
    
    j_schema: dict = {}
    j_config: Jadn_Config = None
    j_type: Union[list, Jadn_Type] = None
    data: any = None # The choice data only
    tagged_data: any = None
    data_format: str = None
    errors = []   
    
    def __init__(self, j_schema: dict = {}, j_type: Union[list, Jadn_Type] = None, data: any = None, tagged_data: any = None, data_format = JSON):
        self.j_schema = j_schema
        
        if isinstance(j_type, list):
            j_type = build_j_type(j_type)
        
        self.j_type = j_type
        self.data = data
        self.tagged_data = tagged_data
        self.data_format = data_format          
        
        self.j_config = get_j_config(self.j_schema)
        self.errors = []
        
    def check_inheritance(self):
        inherit_from = get_inheritance(self.j_type.type_options)
        if inherit_from is not None:
            inherited_type = get_reference_type(self.j_schema, inherit_from)
            inherited_type_obj = build_j_type(inherited_type)
            
            if inherited_type is None:
                raise ValueError(f"Type {self.j_type.type_name} inherits from unknown type {inherit_from}")
            
            if self.j_type.base_type != inherited_type_obj.base_type:
                raise ValueError(f"Type {self.j_type.type_name} inherits from type {inherit_from} with different base type {inherited_type_obj.base_type}. Received: {self.j_type.base_type}")
            
            # Prepend inherited fields to current fields
            self.j_type.fields = inherited_type_obj.fields + self.j_type.fields         
        
    def process_any_of(self, use_ids):
        # value must be an instance of anyOf the types, tried in field order until a match is found
        for j_index, j_field in enumerate(self.j_type.fields):
            j_field_obj = build_jadn_type_obj(j_field)
        if is_field_multiplicity(j_field_obj.type_options):
            j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
                           
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=self.data,
                data_format=self.data_format
            )                 
            
            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()

        elif is_user_defined(j_field_obj.base_type):
            ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
            ref_type_obj = build_j_type(ref_type)
            check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
            merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
            j_field_obj = ref_type_obj
            j_field_obj.type_options = merged_opts
            
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=self.data,
                data_format=self.data_format
            )                  
                
            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()

        elif is_primitive(j_field_obj.base_type): 
            
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=self.data,
                data_format=self.data_format
            )                 
            
            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()

    def process_all_of(self, use_ids):  
        # value must be an instance of allOf the types
        choice_fields = 0
        tracker = 0
        for j_index, j_field in enumerate(self.j_type.fields):
            j_field_obj = build_jadn_type_obj(j_field)
            if is_field_multiplicity(j_field_obj.type_options):
                j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
                        
                choice_fields = choice_fields+1                
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                try:
                    clz_instance.validate()
                    if is_logical_not(j_field_obj.type_options):    
                        raise Exception (f"Choice '{j_field_obj.type_name}' found, but 'not' has been specified.")
                    else: choice_fields = choice_fields+1
                except ValueError as e:
                    if is_logical_not(j_field_obj.type_options): 
                        print(f"Choice '{j_field_obj.type_name}' missing, but 'not' has been specified.")
                    else:     
                        tracker = tracker+1
                        choice_fields = choice_fields+1
                        print(f'tracker incremented')
                        print(f"not an instance of {j_field_obj.base_type}")

            elif is_user_defined(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                j_field_obj = ref_type_obj
                j_field_obj.type_options = merged_opts
                
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                  
                    
                clz_instance = create_clz_instance(**clz_kwargs)
                try:
                    clz_instance.validate()
                    if is_logical_not(j_field_obj.type_options):    
                        raise Exception (f"Choice '{j_field_obj.type_name}' found, but 'not' has been specified.")
                    else: choice_fields = choice_fields+1
                except ValueError as e:
                    if is_logical_not(j_field_obj.type_options): 
                        print(f"Choice '{j_field_obj.type_name}' missing, but 'not' has been specified.")
                    else:     
                        tracker = tracker+1
                        choice_fields = choice_fields+1
                        print(f'tracker incremented')
                        print(f"not an instance of {j_field_obj.base_type}")

            elif is_primitive(j_field_obj.base_type): 
                
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                try:
                    clz_instance.validate()
                    if is_logical_not(j_field_obj.type_options):    
                        raise Exception (f"Choice '{j_field_obj.type_name}' found, but 'not' has been specified.")
                    else: choice_fields = choice_fields+1          
                except ValueError as e:
                    if is_logical_not(j_field_obj.type_options): 
                        print(f"Choice '{j_field_obj.type_name}' missing, but 'not' has been specified.")
                    else:     
                        tracker = tracker+1
                        choice_fields = choice_fields+1
                        print(f'tracker incremented')
                        print(f"not an instance of {j_field_obj.base_type}")
        if choice_fields == 0:
            raise ValueError(f"All fields on AllOf Choice use Not option. Restrict the Choice value space.")
        if tracker != 0:
            raise ValueError(f"All fields on AllOf Choice not satisfied.")
        
    def process_one_of(self, use_ids):
        #value must be an instance of oneOf the types and no others
        if self.data is None:
            raise ValueError(f"Choice '{self.j_type.type_name}' value not found. ")
        choice_fields = 0
        tracker = 0
        for j_index, j_field in enumerate(self.j_type.fields):
            choice_fields = choice_fields+1
            j_field_obj = build_jadn_type_obj(j_field)
            if is_field_multiplicity(j_field_obj.type_options):
                j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
                                   
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()
            elif is_user_defined(j_field_obj.base_type): 
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type) 
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                j_field_obj = ref_type_obj
                j_field_obj.type_options = merged_opts
                
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                try:
                    clz_instance.validate()
                except ValueError:
                    tracker = tracker+1
                    print(f"not an instance of {j_field_obj.base_type} : {self.data}")

            elif is_primitive(j_field_obj.base_type): 
                
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                try:
                    clz_instance.validate()
                except ValueError:
                    tracker = tracker+1
                    print(f"not an instance of Basetype{j_field_obj.base_type} : {self.data}")
        print(f"tracker is at {tracker}")
        if tracker == choice_fields:
            raise ValueError(f"value matches no Choice option in {self.j_type.type_name}")
        elif tracker != choice_fields-1:
            raise ValueError(f"value matches more than one Choice option in {self.j_type.type_name}")
        else: pass

    def process_default(self, use_ids):

        # only one choice is allowed        
        if len(self.data) != 1:
            self.errors.append(f"Choice '{self.j_type.type_name}' must have exactly one choice. Received: {len(self.data)}")
        
        for key, choice_data in self.data.items():
            j_field = get_j_field(self.j_type.fields, key, use_ids)
            
            if j_field is None:
                raise ValueError(f"Choice '{self.j_type.type_name}' key {key} not found. ")
            
            j_field_obj = build_jadn_type_obj(j_field)
            check_sys_char(j_field_obj.type_name, self.j_config.Sys)
            check_field_name(j_field_obj.type_name, self.j_config.FieldName)
        
            if is_field_multiplicity(j_field_obj.type_options):
                j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
                                   
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                 
                
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()
            elif is_user_defined(j_field_obj.base_type):
                ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                ref_type_obj = build_j_type(ref_type)
                check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                j_field_obj = ref_type_obj
                j_field_obj.type_options = merged_opts
                
            clz_kwargs = dict(
                class_name=j_field_obj.base_type,
                j_schema=self.j_schema,
                j_type=j_field_obj,
                data=choice_data,
                data_format=self.data_format
            )                 
                
            clz_instance = create_clz_instance(**clz_kwargs)
            clz_instance.validate()
            
            break # Only one choice is allowed.

    def process_tag_id(self, use_ids):
        
        tagged_choice_found = False
        for j_index, j_field in enumerate(self.j_type.fields):
            j_field_obj = build_jadn_type_obj(j_field)
                
            if j_field_obj.type_name != self.tagged_data:    
                continue
            else:
                tagged_choice_found = True
                
                check_sys_char(j_field_obj.type_name, self.j_config.Sys)
                check_field_name(j_field_obj.type_name, self.j_config.FieldName)                            
        
                if is_field_multiplicity(j_field_obj.type_options):
                    j_field_obj = flip_to_array_of(j_field_obj, get_min_occurs(j_field_obj), get_max_occurs(j_field_obj, self.j_config))
                                                              
                    clz_kwargs = dict(
                        class_name=j_field_obj.base_type,
                        j_schema=self.j_schema,
                        j_type=j_field_obj,
                        data=self.data,
                        data_format=self.data_format
                    )                 
                    
                    clz_instance = create_clz_instance(**clz_kwargs)
                    clz_instance.validate()     
                elif is_user_defined(j_field_obj.base_type):
                    ref_type = get_reference_type(self.j_schema, j_field_obj.base_type)
                    ref_type_obj = build_j_type(ref_type)
                    check_type_name(ref_type_obj.type_name, self.j_config.TypeName)
                    merged_opts = merge_opts(j_field_obj.type_options, ref_type_obj.type_options)
                    j_field_obj = ref_type_obj
                    j_field_obj.type_options = merged_opts
                    
                clz_kwargs = dict(
                    class_name=j_field_obj.base_type,
                    j_schema=self.j_schema,
                    j_type=j_field_obj,
                    data=self.data,
                    data_format=self.data_format
                )                  
                    
                clz_instance = create_clz_instance(**clz_kwargs)
                clz_instance.validate()
                break
            
        if not tagged_choice_found:
            raise ValueError(f"Tagged choice '{self.tagged_data}' not found in choice type {self.j_type.type_name}.")
                        
            
    def check_choice(self):
        use_ids = use_field_ids(self.j_type.type_options)
        if self.tagged_data is not None: # seems redundant but gets mad if i remove the lower one...
            choice_type = Choice_Consts.CHOICE_TAG_ID
        else:
            choice_type = get_choice_type(self.j_type.type_options)

        if use_ids is not None:
            match choice_type:
                case Choice_Consts.CHOICE_ALL_OF:
                    self.process_all_of(use_ids)
                case Choice_Consts.CHOICE_ANY_OF:
                    self.process_any_of(use_ids)
                case Choice_Consts.CHOICE_ONE_OF:
                    self.process_one_of(use_ids)
                #case Choice_Consts.CHOICE_NOT:
                    #self.process_not(use_ids)
                case Choice_Consts.CHOICE_TAG_ID:
                    self.process_tag_id(use_ids)
                case _:
                    self.process_default(use_ids)
                                
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