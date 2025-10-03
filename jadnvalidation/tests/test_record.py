from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data
from jadnvalidation.utils.consts import XML

def test_forward_ref():
    root = "Root-Test"
    
    j_schema =   {  
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_a", "RecordName2", [], ""]
            ]],
            ["RecordName2", "Record", [], "", [
                [1, "field_value_aa", "RecordName3", [], ""]
            ]],
            ["RecordName3", "Record", [], "", [
                [1, "field_value_aaa", "RecordName4", [], ""]
            ]],
            ["RecordName4", "Record", [], "", [
                [1, "field_value_aaaa", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            'field_value_a': {
                'field_value_aa': {
                    'field_value_aaa': {
                        'field_value_aaaa': 'Darth Malgus'
                    }
                }
            }  
        }
    ]
    
    invalid_data_list = [
        {
            'field_value_a': {
                'field_value_aa': {
                    'field_value_aaa': {
                        'field_value_aaaa': 0
                    }
                }
            }  
        },
        {
            'field_value_a': {
                'field_value_aaa': "Dartg Nihilus"
            },
        },
        { 'true' : 'True' },
        {}
    ]
    
    # err_count = validate_valid_data(j_schema, root, valid_data_list)    
    # assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_records_min_max(): 
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{2", "}3"], "", [
                [1, "field_value_1", "String", ["{2", "}6"], ""],
                [2, "field_value_2", "String", ["{2", "}6"], ""],
                [3, "field_value_3", "String", ["[0"], ""]
            ]]
        ]
    }    
    
    valid_data_list = [
        {
            'field_value_1': 'test',
            'field_value_2': '654321'
        },
        {
            'field_value_1': '123456',
            'field_value_2': "apple",
            'field_value_3': 'Sigma'
        }        
    ]
  
    invalid_data_list_1 = [
        {
            'field_value_1': "test field",
            'field_value_2': "t",
            'field_value_3': "1234567"
        },
        {
            'field_value_1': "123456789",
            'field_value_2': "1"
        }        
    ]
    
    invalid_data_list_2 = [
        { #too few fields
            'field_value_1': "test 1"
        },
        { #incorrect typing
            'field_value_1': "test 2",
            'field_value_2': False,
            'field_value_3': "test"
        },
        { #too long field data
            'field_value_1': "test 3",
            'field_value_2': "long test string",
            'field_value_3': "test"
        },
        { #too short field data
            'field_value_1': "test 4",
            'field_value_2': "Z",
            'field_value_3': "test"
        },
        { #incorrect field in data
            'field_value_1': "test 5",
            'field_value_2': "test",
            'field_value_5': "five?"
        },
        { #too many of a field
            'field_value_1': "test 6",
            'field_value_2': "test",
            'field_value_3': "test",
            'field_value_4': "test",
        } 
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list_1)
    assert err_count == len(invalid_data_list_1)
    
    err_count = validate_invalid_data(j_schema, root, invalid_data_list_2)
    assert err_count == len(invalid_data_list_2)    

def test_record():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{2", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1a": "test field",
            "field_value_2a": "Anytown"
        },
        {
            "field_value_1a": "testing more",
            "field_value_2a": "z"
        },
        {
            "field_value_1a": "testing more 123",
            "field_value_2a": "321"
        }        
    ]
    
    invalid_data_list = [
        {
            'field_value_1a': True
        },
        {
            'field_value_1b': "test field",
            'field_value_2b': False
        }        
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_record():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{2", "}2"], "", [
                [1, "field_value_1a", "String", [], ""],
                [2, "field_value_2a", "String", [], ""]
            ]]          
        ]
    }  
    
    valid_xml_1 = """<Root-Test>
        <field_value_1a>test field</field_value_1a>
        <field_value_2a>Darth Andeddu</field_value_2a>
    </Root-Test>"""
    valid_xml_2 = """<Root-Test>
        <field_value_1a>testing more</field_value_1a>
        <field_value_2a>Darth Atrius</field_value_2a>
    </Root-Test>"""
    valid_xml_3 = """<Root-Test>
        <field_value_1a>testing more 123</field_value_1a>
        <field_value_2a>Darth Bane</field_value_2a>
    </Root-Test>"""
    
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1b>test field</field_value_1b>
        <field_value_2b>Darth Andeddu</field_value_2b>
    </Root-Test>"""
    invalid_xml_2 = """<Root-Test>
        <field_value_1a>testing more</field_value_1a>
    </Root-Test>"""
    invalid_xml_3 = """<Root-Test>
        <field_value_2a>Darth Bane</field_value_2a>
    </Root-Test>"""    
    
    valid_data_list = [
        valid_xml_1,
        valid_xml_2,
        valid_xml_3       
    ]
    
    invalid_data_list = [
        invalid_xml_1,
        invalid_xml_2,
        invalid_xml_3        
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    
    
def test_record_in_record():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Record-Test"]
        },
        "types": [
            ["Root-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1", "Record2-Test", [], ""]
            ]],
            ["Record2-Test", "Record", ["{1", "}2"], "", [
                [1, "field_value_1b", "String", ["{0", "[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": {
                "field_value_1b": "molestias,"
            }
        }       
    ]
    
    invalid_data_list = [
        {
            'field_value_1b': True
        },
        {
            'field_value_1b': 123
        }        
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    
    
def test_record_min_occurs():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1a", "String", ["[1"], ""],
                [2, "field_value_2a", "String", ["[0"], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1a": "test min occurs 1",
            "field_value_2a": "Anytown"
        },
        {
            "field_value_1a": "test min occurs 1"
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2a": "test min occurs 1",
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_record_max_occurs():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", ["{1", "}10"], "", [
                [1, "field_value_1", "String", ["]1"], ""],
                [2, "field_value_2", "String", ["[0"], ""],
                [3, "field_value_3", "String", ["]3"], ""]
            ]]          
        ]
    }  
    
    valid_data_list = [
        {
            "field_value_1": "darth mekhis",
            "field_value_2": "darth bane",
            "field_value_3": ["darth nihilus", "darth malgus", "darth revan"]
        },
        {
            "field_value_1": "darth mekhis",
            "field_value_3": ["darth nihilus", "darth malgus", "darth revan"]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": "test 3",
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

        
def test_record_complex():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "meta", "String", [], ""],
                [2, "types", "Type", ["[1", "]-1"], ""]]],
            ["Type", "Array", [], "", [
                [1, "array_field_1", "Integer", [], ""],
                [2, "array_field_2", "String", [], ""],
                [3, "array_field_3", "Choice-List", ["[0"], ""]]],
            ["Choice-List", "Choice", ["[0"], "", [
                [1, "choice_field_1", "Integer", [], ""],
                [2, "choice_field_2", "String", [], ""],
                [3, "choice_field_3", "Tiny-Array", [], ""]
            ]],
            ["Tiny-Array", "Array", [], "", [
                [1, "tiny_field_1", "String", [], ""]]]
            ]                  
    }  
    
    valid_data_list = [
        {
            "meta" : "string",
            "types" : [[999, "Array-def-Name(ANY STRING)", {"choice_field_3": ["illum repellendus nobis"]}]]
        },        
        {
            "meta" : "fake_package.url.lol",
            "types" : [[999, "Array-def-Name(ANY STRING)"]]
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "test 2",
            "field_value_3": "test 3",
        }
    ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    # err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    # assert err_count == len(invalid_data_list)