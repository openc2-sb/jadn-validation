from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML
    

def test_array_of_ints():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Integer", "{1", "}3"], ""]
        ]
    }
    
    valid_data_list = [
            [1, 2, 11111111],
            [0, 00, 0]
        ]
    
    invalid_data_list = [
            ["1", 1, 11],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_xml_array_of():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Integer", "{1", "}3"], ""]
        ]
    }
    
    valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <items>
        <item>123</item>
        <item>123</item>
        <item>123</item>
    </items>"""
    
    invalid_xml_1 = """<?xml version="1.0" encoding="UTF-8"?>
    <root>
        <item>test</item>
    </root>
    """
    
    invalid_xml_2 = """<?xml version="1.0" encoding="UTF-8"?>
    <items>
        <item>False</item>
        <item>"123"</item>
        <item>"123"</item>
    </items>""" 
    
    valid_data_list = [
            valid_xml
        ]
    
    invalid_data_list = [
            invalid_xml_1,
            invalid_xml_2
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)    
    assert err_count == len(invalid_data_list)    
    
def test_array_of_strs():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*String", "{1", "}3"], ""]
        ]
    }
    
    valid_data_list = [
            ["test", "t", "11111111"],
            ["0", "___", "##"]
        ]
    
    invalid_data_list = [
            ["1", 1, 11],
            ["1", True, False],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == 2
    
def test_array_of_booleans():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Boolean", "{2", "}3"], ""]
        ]
    }

    # Think like a computer... 'truthy' and 'falsy' items will be validated as true or false, 
    # regardless of how "non-boolean" they may appear
    valid_data_list = [
            [True, False],
            [False, False, True],
            ["False", "False"],
            [0, 1], 
            [1, "Hello World"]
        ]
    
    invalid_data_list = [
            [True],
            [],
            [10, 333]
        ]

        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_of_records():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Record-Test", "{1", "}3"], ""],
            ["Record-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""]
            ]]
        ]
    }
    
    valid_test_rec = {
        "field_value_1" : "test"
    }
    
    valid_data_list = [
            [valid_test_rec, valid_test_rec],
            [valid_test_rec, valid_test_rec, valid_test_rec]
        ]
    
    invalid_data_list = [
            [
                { "field_value_1" : 123 }, 
                { "field_value_1" : False }
            ],
            [
                { "field_value_2" : "test" }, 
                { "field_value_1" : 1.0 }
            ]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
    
def test_array_of_arrays():
    root = "Root-Test"    
    
    j_schema = { 
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Array-Name", "{1", "}3"], ""],
            ["Array-Name", "Array", ["{1"], "", [
                [1, "field_value_1", "Record-Name", [], ""]
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_test_rec = {
        "field_value_2" : "test"
    }
    
    valid_data_list = [
            [[valid_test_rec], [valid_test_rec]],
            [[valid_test_rec], [valid_test_rec], [valid_test_rec]]
        ]
    
    invalid_data_list = [
            [
                { "field_value_1" : 123 }, 
                { "field_value_1" : False }
            ],
            [
                { "field_value_2" : "test" }, 
                { "field_value_1" : 1.0 }
            ]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_array_of_arrays_2():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Sub-Array", "{1", "}3"], ""], 
            ["Sub-Array", "Array", [], "", [
                [1, "test_field_1", "Integer", ["[0"], ""],
                [2, "test_field_2", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [[1, "Hello"],[2, "World"]],
            [[1, "Hello"]],
            [[1, "Hello"],[2, "World"], [0, "yup"]]
        ]
    
    invalid_data_list = [
            ["1", 1, 11],
            ["test"],
            [[1, "Hello"],[2, "World"], [0, "yup"], [4, "This is too long"]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_array_of_choice():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Choice-List", "{1", "}3"], ""], 
            ["Choice-List", "Choice", [], "", [
                [1, "test_field_1", "Integer", [], ""],
                [2, "test_field_2", "String", [], ""],
                [3, "test_field_3", "Array-Defined", [], ""]
            ]],
            ["Array-Defined", "ArrayOf", ["*String", "{1", "}3"], ""],
        ]
    }
    
    valid_data_list = [
            [{"test_field_2": "illum repellendus nobis"}], 
            [{"test_field_3": ["illum repellendus nobis"]}] 
        ]
    
    invalid_data_list = [
            [[1, "Hello"],[2, "World"], [0, "yup"], [4, "This is too long"]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_array_of_choice_2():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Array-Defined", "{1", "}3"], ""], 

            ["Array-Defined", "Array", [], "", [
                [1, "array_field_1", "Integer", [], ""],
                [2, "array_field_2", "String", [], ""],
                [3, "array_field_3", "Choice-List", [], ""]
            ]],                     
            ["Choice-List", "Choice", [], "", [
                [1, "choice_field_1", "Integer", [], ""],
                [2, "choice_field_2", "String", [], ""],
                [3, "choice_field_3", "Tiny-Array", [], ""]
            ]],
            ["Tiny-Array", "Array", [], "", [
                [1, "tiny_field_1", "String", [], ""]]]
        ]
    }
    
    valid_data_list = [
        [[
            999, "ANY STRING", {
                "choice_field_3": ["illum repellendus nobis"]
                }
            ]]
        ]
    
    invalid_data_list = [

            [[1, "Hello"],[2, "World"], [0, "yup"], [4, "This is too long"]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_array_of_choice_3():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Array-Defined", "{1", "}3"], ""], 

            ["Array-Defined", "Array", [], "", [
                [1, "array_field_1", "Integer", [], ""],
                [2, "array_field_2", "String", [], ""],
                [3, "array_field_3", "Choice-Array-Of", [], ""]
            ]],    
            ["Choice-Array-Of", "ArrayOf", ["*Choice-List"], ""],                   
            ["Choice-List", "Choice", [], "", [
                [1, "choice_field_1", "Integer", [], ""],
                [2, "choice_field_2", "String", [], ""],
                [3, "choice_field_3", "Tiny-Array", [], ""]
            ]],
            ["Tiny-Array", "Array", [], "", [
                [1, "tiny_field_1", "String", [], ""]]]
        ]
    }
    
    valid_data_list = [
        [[
            999, "ANY STRING", [{
                "choice_field_3": ["illum repellendus nobis"]
                }]
            ]],
        [[
            999, "ANY STRING", [{
                "choice_field_3": ["illum repellendus nobis"], "choice_field_3": ["hahaha"]
                }]
            ]]
        ]
    
    invalid_data_list = [

            [[1, "Hello"],[2, "World"], [0, "yup"], [4, "This is too long"]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_array_of_choice_3_copy():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://www.test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "ArrayOf", ["*Array-Defined", "{1", "}3"], ""], 

            ["Array-Defined", "Array", [], "", [
                [1, "array_field_1", "Integer", [], ""],
                [2, "array_field_2", "String", [], ""],
                [3, "array_field_3", "Choice-Array-Of", [], ""]
            ]],    
            ["Choice-Array-Of", "ArrayOf", ["*Choice-List"], ""],                   
            ["Choice-List", "Choice", [], "", [
                [1, "choice_field_1", "Integer", [], ""],
                [2, "choice_field_2", "String", [], ""],
                [3, "choice_field_3", "Tiny-Array", [], ""]
            ]],
            ["Tiny-Array", "Array", [], "", [
                [1, "tiny_field_1", "String", [], ""]]]
        ]
    }
    
    valid_data_list = [
        [[
            999, "ANY STRING", [{
                "choice_field_3": ["illum repellendus nobis"]
                }]
            ]]
        ]
    
    invalid_data_list = [

            [[1, "Hello"],[2, "World"], [0, "yup"], [4, "This is too long"]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)