from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML
    

def test_array():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test", True, 123],
            ["", False, 0]
        ]
    
    invalid_data_list = [
            [True, "Test", 123],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_2():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [1], 
            [-1], 
            [0]
        ]
    
    invalid_data_list = [
            ["Test"], 
            [1.2], 
            ["1"],
            [0, 1, 2],
            [True],
            [False]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_field_max_occurs():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["]3"], ""]
            ]]
        ]
    }
            
    valid_data_list = [
            [["test 1", "test 2", "test 3"]],
            [["test 1", "test 2"]] 
        ]
    
    invalid_data_list = [
            [["test 1", "test 2", "test 3", "test 4", "test 5"]], 
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)       
    
def test_xml_array():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <items>
        <item>test</item>
        <item>True</item>
        <item>123</item>
    </items>"""
    
    invalid_xml = """<?xml version="1.0" encoding="UTF-8"?>
    <root>
        <item>test</item>
    </root>
    """      
    
    valid_data_list = [
            valid_xml
        ]
    
    invalid_data_list = [
            invalid_xml
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list, data_format=XML)
    assert err_count == 0
        
    # err_count = validate_invalid_data(j_schema, root, invalid_data_list, data_format=XML)
    # assert err_count == len(invalid_data_list)    


def test_array_optional_first():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["[0"], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [None, True, 123],
            ["", False, 0]
        ]
    
    invalid_data_list = [
            [True, "Test", 123],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)


def test_array_optional_last():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test", True],
            ["", False, 0]
        ]
    
    invalid_data_list = [
            [True, "Test", 123],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_min_occurs():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["[1"], ""],
                [2, "field_value_2", "Boolean", ["[2"], ""],
                [3, "field_value_3", "Integer", ["[3"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test 1", [True, False], [1, 2, 3]],
        ]
    
    invalid_data_list = [
            [True, "Test", 123],
            ["test"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_max_occurs():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "Boolean", ["]2"], ""],
                [3, "field_value_3", "Integer", ["]3"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test 1", [True, False], [1, 2, 3]],
            ["test 1", [True], [1, 2, 3]],
            ["test 1", [True, False], [1]]
        ]
    
    invalid_data_list = [
            ["test 1", [True, False, True], [1, 2, 3]],
            [["test 1", "test2"], [True, False, True], [1, 2, 3]],
            ["test 1", [True, False, True], [1, 2, 3, 4]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_array_min_max_occurs():
    root = "Root-Test"    
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["[0", "]1"], ""],
                [2, "field_value_2", "Boolean", ["[1", "]2"], ""],
                [3, "field_value_3", "Integer", ["[2", "]3"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test 1", [True, False], [1, 2, 3]],
            [None, [True, False], [1, 2, 3]],
            ["test 1", [True], [1, 2, 3]],
            ["test 1", [True, False], [1, 2]]
        ]
    
    invalid_data_list = [
            ["test 1", [True, False, True], [1, 2, 3]],
            [["test 1", "test2"], [True], [1, 2, 3]],
            [[True, False], [1, 2, 3]],
            ["test 1", [True, False, True], [1, 2, 3, 4]]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)   
    
    
def test_array_min_max_occurs_2():
    root = "Root-Test"    
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["[3", "]3"], ""]
            ]]
        ]
    }

    valid_data_list = [
            [["test 1", "test 2", "test 3"]],
            [["test a", "test b", "test c"]]
        ]

    invalid_data_list = [
            [["test 1"]],
            [["test 1", "test 2", "test 3", "test 4"]],
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
    
def test_array_min_max_occurs_3():
    root = "Root-Test"    
    
    j_schema = {
                "meta": 
                    { "package": "http://example.fake/", 
                      "roots": ["Root-Test"] 
                    }, 
                    "types": [ 
                        ["Root-Test", "Array", ["}2"], "", 
                         [ 
                          [1, "field_value_1", "String", ["[2"], ""], 
                          [2, "field_value_2", "String", ["[0"], ""], 
                          [3, "field_value_3", "String", ["[0"], ""] 
                          ]
                        ] 
                    ] 
                }

    valid_data_list = [
            [["test 1", "test 2"], "test 3"],
            [["test a", "test b"]]
        ]

    invalid_data_list = [
            [["test 1"]],
            [["test 1", "test 2", "test 3"], "test 4", "test 5"],
            [["test 1", "test 2"], "test 3", "test 4"]
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    
    
def test_forward_ref():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1a", "ArrayName2", [], ""]
            ]],
            ["ArrayName2", "Array", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [['Any String']],
            [['123']]
        ]
    
    invalid_data_list = [
            [[123, 'Any String']],
            [True]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_forward_ref_2():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1a", "ArrayName2", [], ""],
                [2, "field_value_1b", "ArrayName2", [], ""]
            ]],
            ["ArrayName2", "Array", [], "", [
                [1, "field_value_2a", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [['Any String'], ["AnyString2"]],
            [['123'], ['HelloWorld']]
        ]
    
    invalid_data_list = [
            [[123, 'Any String']],
            [True], [['Hi im one item']]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)

def test_forward_ref_toOf():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1a", "ArrayName2", [], ""],
                [2, "field_value_1b", "ArrayOf", ["*String"], ""]
            ]],
            ["ArrayName2", "ArrayOf", ["*String"], ""
            ]
        ]
    }
    
    valid_data_list = [
            [['Any String'], ["AnyString2"]],
            [['123'], ['HelloWorld']]
        ]
    
    invalid_data_list = [
            [[123, 'Any String']],
            [True], [['Hi im one item']]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_ipv4net():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["/ipv4-net", "{1", "}2"], "", [
                [1, "ipv4_addr", "Binary", ["/ipv4-addr", "{1", "[1"], "IPv4 address as defined in [[RFC0791]](#rfc0791)"],
                [2, "prefix_length", "Integer", ["{0", "}32", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
            ]]
        ]
    }
    
    valid_data_list = [
            #["127.0.0.1", 5], - array structured examples not correct JSON serialization
            #["127.0.0.1"],
            #[b"127.0.0.1", 1],
            "127.0.0.1/1"
        ]
    
    invalid_data_list = [
            [123, 'Any String'],
            [True]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)
    
def test_ipv6net():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["/ipv6-net", "{2", "}2"], "", [
                [1, "ipv6_addr", "Binary", ["/ipv6-addr", "{1", "[1"], "IPv6 address as defined in [[RFC8200]](#rfc8200)"],
                [2, "prefix_length", "Integer", ["{0", "}128", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
            ]]
        ]
    }
    
    valid_data_list = [
            #["2001:db8:3333:4444:5555:6666:1.2.3.4", 5],
            #["2001:db8:3333:4444:5555:6666:1.2.3.4"],
            #[b"2001:db8:3333:4444:5555:6666:1.2.3.4", 1],
            "2001:db8:3333:4444:5555:6666:1.2.3.4/1"
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129]
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)         
    
def test_empty_array():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["}0"], "", []
            ]]
    }
    
    valid_data_list = [
            []
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129], "",
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)         

def test_nested_array_arrayof():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["{0"], "", [
                [1, "string_name", "Integer", [], ""],
                [2, "nested_arrayOf", "ArrayOf", ["*String"], ""]
            ]]
            ]
    }
    
    valid_data_list = [
            [1, ["First"]]
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129], "",
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    


def test_nested_array_array_enum():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["}0"], "", [
                [1, "string_name", "String", [], ""],
                [2, "enum", "Enum-Ex", [], ""]
            ]],
            ["Enum-Ex", "Enumerated", [], "", [
                 [1, "First", ""],
                 [2, "Second", ""]
            ]]
            ]
    }
    
    valid_data_list = [
            ["Hello", "First"]
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129], "",
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    

def test_nested_array_complex():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", ["}0"], "", [
                [1, "enum", "Enums", [], ""],
                [2, "string_name", "String", [], ""]
            ]],
            ["Enums", "ArrayOf", ["*Enum-Ex"], "", [
                [1, "enum1", "Enum-Ex", [], ""],
                [2, "enum2", "Enum-Ex", [], ""]
            ]],
            ["Enum-Ex", "Enumerated", [], "", [
                 [1, "First", ""],
                 [2, "Second", ""]
            ]]
            ]
    }
    
    valid_data_list = [
            [["First", "First"], "AnyString"]
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129], "",
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    

def test_nested_array_complex_2():
    root = "Root-Test"
    
    j_schema =   {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Array", [], "", [
              [1, "type_name", "String", [], ""],
              [2, "core_type", "Enum-Ex", [], ""],
              [3, "type_options", "String", ["[0", "]2"], ""],
              [4, "type_description", "String", ["[0"], ""],
              [5, "fields", "ArrayOf", ["*Choice-List", "[0"], ""]
            ]],
            ["Enum-Ex", "Enumerated", [], "", [
                 [1, "First", ""],
                 [2, "Second", ""]
            ]],
            ["Choice-List", "Choice", [], "", [
                [1, "enum1", "Enum-Ex", [], ""],
                [2, "enum2", "Enum-Ex", [], ""]
            ]],
            ]
    }
    
    valid_data_list = [
            ["String", "First", ["String"], "String", [{"enum1": "First"}]]
        ]
    
    invalid_data_list = [
            ["http://www.example.com", 80],
            [b"2001:db8:3333:4444:5555:6666:1.2.3.4", 129], "",
        ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)    
    assert err_count == len(invalid_data_list)    

                