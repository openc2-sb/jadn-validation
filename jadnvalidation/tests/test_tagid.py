from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_tagid_in_array():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "type_name", "String", [], ""],
                [2, "core_type", "Core-Types", [], ""],
                [3, "fields", "JADN-Type", ["&2"], ""]
            ]],    
            ["Core-Types", "Enumerated", ["#JADN-Type"], "", []],
            ["JADN-Type", "Choice", [], "", [
                [1, "string", "Array-Empty", [], ""],
                [2, "record", "Array-Fields", [], ""],
                [3, "enum", "Array-Items", [], ""]
            ]],    
            ["Array-Items", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]],
            ["Array-Fields", "Array", [], "", [
                [1, "field_value_a", "String", [], ""],
                [2, "field_value_b", "String", [], ""]
            ]],
            ["Array-Empty", "Array", [], "", []]
        ]
    }
    
    valid_data_list = [
        [
            "my name",
            "string",
            []
        ],
        [
            "Soliloquy",
            "record",
            ['row1', 'row2']
        ],
        [
            "Soliloquy",
            "enum",
            ['val1', 'val2']
        ]
    ]
    invalid_data_list = ['redd', 2 ,'test', None,
        [
            "ANY_STRING",
            "data",
            {'string': []}
        ],[
            "ANY_STRING",
            "data",
            []
        ],
        [
            "my name",
            "string",
            {'string': []}
        ],
        [
            "Soliloquy",
            "record",
            {'record': ['row1', 'row2']}
        ],
        [
            "Soliloquy",
            "record",
            {'record': ['row1', 'row2']}
        ]
                         
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_tagid_in_record():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "type_name", "String", [], ""],
                [2, "selected_type", "Selected-Type", [], ""],
                [3, "fields", "JADN-Type", ["&2"], ""]
            ]],    
            ["Selected-Type", "Enumerated", ["#JADN-Type"], "", []],
            ["JADN-Type", "Choice", [], "", [
                [1, "string", "Array-Empty", [], ""],
                [2, "record", "Array-Fields", [], ""],
                [3, "enum", "Array-Items", [], ""]
            ]],    
            ["Array-Items", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]],
            ["Array-Fields", "Array", [], "", [
                [1, "field_value_a", "String", [], ""],
                [2, "field_value_b", "String", [], ""]
            ]],
            ["Array-Empty", "Array", [], "", []]
        ]
    }
    
    valid_data_list = [
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": []
        },
        {
            "type_name": "Soliloquy",
            "selected_type": "record",
            "fields": ['row1', 'row2']
        },
        {
            "type_name": "Soliloquy",
            "selected_type": "enum",
            "fields": ['val1', 'val2']
        }
    ]
    invalid_data_list = ['redd', 2 ,'test', None,

        [   
            "my name",
            "string",
            []
        ],
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'string': []}
        },
        [
            "ANY_STRING",
            "data",
            []
        ],
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'string': []}
        },
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'record': ['row1', 'row2']}
        },
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'enum': ['item1', 'item2']}
        },
        {
            "type_name": "my name",
            "selected_type": "record",
            "fields": []
        },
                         
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_tagid_in_map():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "type_name", "String", [], ""],
                [2, "selected_type", "Selected-Type", [], ""],
                [3, "fields", "JADN-Type", ["&2"], ""]
            ]],    
            ["Selected-Type", "Enumerated", ["#JADN-Type"], "", []],
            ["JADN-Type", "Choice", [], "", [
                [1, "string", "Array-Empty", [], ""],
                [2, "record", "Array-Fields", [], ""],
                [3, "enum", "Array-Items", [], ""]
            ]],    
            ["Array-Items", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]],
            ["Array-Fields", "Array", [], "", [
                [1, "field_value_a", "String", [], ""],
                [2, "field_value_b", "String", [], ""]
            ]],
            ["Array-Empty", "Array", [], "", []]
        ]
    }
    
    valid_data_list = [
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": []
        },
        {
            "type_name": "Soliloquy",
            "selected_type": "record",
            "fields": ['row1', 'row2']
        },
        {
            "type_name": "Soliloquy",
            "selected_type": "enum",
            "fields": ['val1', 'val2']
        }
    ]
    invalid_data_list = ['redd', 2 ,'test', None,

        [   
            "my name",
            "string",
            []
        ],
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'string': []}
        },
        [
            "ANY_STRING",
            "data",
            []
        ],
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'string': []}
        },
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'record': ['row1', 'row2']}
        },
        {
            "type_name": "my name",
            "selected_type": "string",
            "fields": {'enum': ['item1', 'item2']}
        },
        {
            "type_name": "my name",
            "selected_type": "record",
            "fields": []
        },
                         
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)