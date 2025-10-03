from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.general_utils import sort_array_by_id


def test_order_array_by_id():
    
    j_fields_1 =  [
                [2, "item_2", "String", []],
                [1, "item_1", "String", []],
                [3, "item_3", "String", []]
            ]
    
    ordered_array =  sort_array_by_id(j_fields_1)
    
    assert ordered_array == [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []]
            ]
    
def test_order_arrays_by_id():
    
    j_fields_1 =  [
                [111, "common_1", "Integer", ["[0"]],
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]]
            ]
    
    j_fields_2 =  [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []]
            ]
    
    ordered_array =  sort_array_by_id(j_fields_1, j_fields_2)
    
    assert ordered_array == [
                [1, "item_1", "String", []],
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
                [111, "common_1", "Integer", ["[0"]],
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]]
            ]
    
def test_invalid_arrays_id():
    
    j_fields_1 =  [
                [1, "common_1", "Integer", ["[0"]],  # < == DUPLICATE
                [222, "common_2", "Integer", ["[0"]],
                [333, "common_3", "Integer", ["[0"]]
            ]
    
    j_fields_2 =  [
                [1, "item_1", "String", []], # < == DUPLICATE
                [2, "item_2", "String", []],
                [3, "item_3", "String", []],
            ]
    try:
        ordered_array =  sort_array_by_id(j_fields_1, j_fields_2)
    except ValueError as ve:
        assert str(ve) == "Duplicate IDs found in combined array: [1]"
    else:
        assert False, "Expected ValueError for duplicate IDs"

def test_array_inheritance():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Common-Items", "Array", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Array", ["eCommon-Items"], "", [
                [111, "item_1", "String", [], ""],
                [222, "item_2", "String", ["[0"], ""],
                [333, "item_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [1, 2, 3, "item_1", "item_2", "item_3"],
            [None, 2, 3, "item_1", "item_2", "item_3"],
            [1, None, 3, "item_1", "item_2", "item_3"],
            [1, 2, None, "item_1", "item_2", "item_3"],
            [1, 2, 3, "item_1", "", "item_3"],
            [1, 2, 3, "item_1", None, "item_3"],
            [1, 2, 3, "item_1", None],
            [None, None, None, "item_1"],
        ]
    
    invalid_data_list = [
            [1, 2, 3, "item_1", "item_2", "item_3", "extra"],
            [1, 2, 3, 99, "item_1", "item_2", "item_3"],
            [None, 2, 3, None, "item_2", "item_3"],
            [None, None, None, None, None, None],
            [1, 2, 3, 4, 5, 6],
            ["item_1", "item_2", "item_3", "item_4", "item_5", "item_6"],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_record_inheritance():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Common-Items", "Record", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Record", ["eCommon-Items"], "", [
                [111, "item_1", "String", [], ""],
                [222, "item_2", "String", ["[0"], ""],
                [333, "item_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                # "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                # "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                # "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                # "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                # "item_3" : "item_3 data"
            },
            {   
                # "common_1" : 1, 
                # "common_2" : 2, 
                # "common_3" : 3, 
                "item_1" : "item_1 data", 
                # "item_2" : "item_2 data", 
                # "item_3" : "item_3 data"
            },
        ]
    
    invalid_data_list = [
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data",
                "extra" : "extra data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "common_4" : 99, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                # "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
        
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : 4, 
                "item_2" : 5, 
                "item_3" : 6
            },
            {   
                "common_1" : "common_1 data", 
                "common_2" : "common_2 data", 
                "common_3" : "common_3 data", 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            }
        ]    
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_map_inheritance():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Common-Items", "Map", [], "", [
                [1, "common_1", "Integer", ["[0"]],
                [2, "common_2", "Integer", ["[0"]],
                [3, "common_3", "Integer", ["[0"]],
            ]],            
            ["Root-Test", "Map", ["eCommon-Items"], "", [
                [111, "item_1", "String", [], ""],
                [222, "item_2", "String", ["[0"], ""],
                [333, "item_3", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                # "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                # "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                # "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                # "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                # "item_3" : "item_3 data"
            },
            {   
                # "common_1" : 1, 
                # "common_2" : 2, 
                # "common_3" : 3, 
                "item_1" : "item_1 data", 
                # "item_2" : "item_2 data", 
                # "item_3" : "item_3 data"
            },
        ]
    
    invalid_data_list = [
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data",
                "extra" : "extra data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "common_4" : 99, 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                # "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            },
            {   
        
            },
            {   
                "common_1" : 1, 
                "common_2" : 2, 
                "common_3" : 3, 
                "item_1" : 4, 
                "item_2" : 5, 
                "item_3" : 6
            },
            {   
                "common_1" : "common_1 data", 
                "common_2" : "common_2 data", 
                "common_3" : "common_3 data", 
                "item_1" : "item_1 data", 
                "item_2" : "item_2 data", 
                "item_3" : "item_3 data"
            }
        ]    
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    
    
def test_enum_inheritance():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Common-Items", "Enumerated", [], "", [
                [1, "ace_of_clubs", ""],
                [2, "ace_of_diamonds", ""],
                [3, "ace_of_hearts", ""],
                [4, "ace_of_spades", ""]
            ]],            
            ["Root-Test", "Enumerated", ["eCommon-Items"], "", [
                [11, "king_of_clubs", ""],
                [22, "king_of_diamonds", ""],
                [33, "king_of_hearts", ""],
                [44, "king_of_spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [
            "ace_of_clubs",
            "king_of_clubs",
            "ace_of_spades",
            "king_of_spades"
        ]
    
    invalid_data_list = [
            "ace_of_clubs_zzzz",
            1,
            11,
            ""
        ]    
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)  
    
def test_choice_inheritance():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Common-Items", "Choice", [], "", [
                [11, "common_value_1", "String", [], ""],
                [22, "common_value_2", "String", [], ""]
            ]],            
            ["Root-Test", "Choice", ["eCommon-Items"], "", [
                [1, "value_1", "String", [], ""],
                [2, "value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "common_value_1": "revan"
        }, 
        {
            "value_1": "darth traya"
        }
    ]
    
    invalid_data_list = [
        {
            "common_value_3": "revan"
        }, 
        {
            "value_1": 1
        },
        {
            "common_value_1": "revan",
            "value_1": "darth traya"
        }          
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_choice_id_inheritance():
    root = "Root-Test"

    j_schema = {
        "info": {
            "package": "http://test.com",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Common-Items", "Choice", [], "", [
                [11, "common_value_1", "String", [], ""],
                [22, "common_value_2", "String", [], ""]
            ]],            
            ["Root-Test", "Choice", ["=", "eCommon-Items"], "", [
                [1, "value_1", "String", [], ""],
                [2, "value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            11: "revan"
        }, 
        {
            1: "darth traya"
        }
    ]
    
    invalid_data_list = [
        {
            33: "revan"
        }, 
        {
            1: 1
        },
        {
            11: "revan",
            1: "darth traya"
        }          
    ]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)     