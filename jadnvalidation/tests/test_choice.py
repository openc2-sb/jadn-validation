
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_choice():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis"
        }, 
        {
            "field_value_2": False
        }
    ]

    invalid_data_list = []
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        },         
        {
            "field_value_1": "two choice incorrectly",
            "field_value_2": True
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }     
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_xml_choice():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1>illum repellendus nobis</field_value_1>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2>False</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1>illum repellendus nobis</field_value_1>
        <field_value_2>True</field_value_2>
        <field_value_3>test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x>test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1>i have 2 values</field_value_1>
        <field_value_2>False</field_value_2>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)
    
def test_choice_id():
    root = "Root-Test"
        
    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        {
            "1": "illum repellendus nobis",
        }, 
        {
            "2": False
        }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "1": "illum repellendus nobis",
            "2": True
        },
        {
            "field_value_x": "test incorrect field name"
        }       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_choice_id():
    root = "Root-Test"
        
    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1 key="1">illum repellendus nobis</field_value_1>
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        <field_value_2 id="2">False</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  
    
def test_choice_oneOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CX"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", ["%^a$"], ""]
            ]]
        ]
    }
    
    valid_data_list = ["illum repellendus nobis"]

    invalid_data_list = [123, "a", ["illum repellendus nobis", 456],
        {
            "field_value_1": "illum repellendus nobis"
        }  
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)   
    
def test_xml_choice_oneOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CX"], "", [
                [1, "field_value_1", "Number", [], ""],
                [2, "field_value_2", "String", ["/date-time"], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        333.0
    </Root-Test>"""
    valid_xml_2 = """<Root-Test>2023-08-13T16:07:54Z</Root-Test>"""
    valid_xml_3 = """<?xml version="1.0" encoding="UTF-8"?>
        <items>
            <item>one</item>
            <item>two</item>
            <item>three</item>
        </items>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_4>test extra field validation</field_value_4>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x>test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1>a</field_value_1>
        <field_value_2>false</field_value_2>
    </Root-Test>"""

    invalid_xml_4 = """<Root-Test>
        <field_value_1>a</field_value_1>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]    
     
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)

def test_choice_anyOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CO"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        "illum repellendus nobis", False      
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    
        
    
def test_xml_choice_anyOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CO"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        illum repellendus nobis
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        False
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1 key="1">123</field_value_x>
    </Root-Test>"""

    invalid_xml_4 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

    
def test_choice_allOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", ["%^[a-z]*$"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        "false", "illumrepellendusnobis"            
    ]
    
    invalid_data_list = [ "numeric1", False, 123, ["False", "illum repellendus nobis"],
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_xml_choice_allOf():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", ["%^[a-z]*$"], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        illumrepellendusnobis
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        banana       
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
        <field_value_2 id="2">True</field_value_2>
        <field_value_3 id="3">test extra field validation</field_value_3>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        <field_value_x key="11">test incorrect field name</field_value_x>
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>
        <field_value_1 key="1">123</field_value_x>
    </Root-Test>"""

    invalid_xml_4 = """<Root-Test>
        illum repellendus nobis with spaces
    </Root-Test>"""

    invalid_xml_5 = """<Root-Test>
        illum repellendus nobis with CAPS
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4, invalid_xml_5]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  
    
    
def test_choice_allOf_with_not():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", ["N", "%^a$"], ""]
            ]]
        ]
    }
    
    valid_data_list = ["illum repellendus nobis", "b"]
    
    invalid_data_list = ["a", 123,
        {
            "field_value_1": "illum repellendus nobis"
        },      
    ]
    invalid_data_list = ["a"]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_choice_allOf_with_not():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Choice", ["CA"], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", ["N", "%^a$"], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        illum repellendus nobis
    </Root-Test>"""
    
    valid_xml_2 = """<Root-Test>
        b  
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1 id="1">illum repellendus nobis</field_value_1>
    </Root-Test>"""
    
    invalid_xml_2 = """<Root-Test>
        a
    </Root-Test>"""

    invalid_xml_3 = """<Root-Test>  # currently not invalid; needs more team discussion
        illum repellendus nobis
        multiline?
        or are all strings
        outside a block
        together??
    </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    

def test_choice_as_field():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Choice-Test", [], ""]
            ]],
            ["Choice-Test", "Choice", [], "", [
                [1, "choice_value_1", "Integer", [], ""],
                [2, "choice_value_2", "Boolean", [], ""]
            ]]
        ]
    }

    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": {"choice_value_1": 1}
        }
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)  
        

def test_choice_as_field_multiple():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Choice-Test", ["]-1"], ""]
            ]],
            ["Choice-Test", "Choice", [], "", [
                [1, "choice_value_1", "Integer", [], ""],
                [2, "choice_value_2", "Boolean", [], ""]
            ]]
        ]
    }

    valid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": [{"choice_value_1": 1}, {"choice_value_2": True}]
        }
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_choice_spec_example():
    root = "PhoneType"
    
    j_schema = {
        "meta": {
            "title": "JADN Schema Start Up Template",
            "package": "http://JADN-Schema-Start-Up-Template-URI",
            "roots": ["PhoneType"]
        },
        "types": [
            ["PhoneType", "Choice", ["CO"], "", [
                [1, "predefined", "PhoneNumberTypes", [], ""],
                [2, "custom", "String", ["{3", "}10"], ""]
            ]],
            ["PhoneNumberTypes", "Enumerated", [], "", [
                [1, "Home", ""],
                [2, "Cell", ""],
                [3, "Work", ""]
            ]]
        ]
    }

    valid_data_list = [
            "Home"
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)       
    
def test_choice_spec_example_xml():
    root = "PhoneType"
    
    j_schema = {
        "meta": {
            "title": "JADN Schema Start Up Template",
            "package": "http://JADN-Schema-Start-Up-Template-URI",
            "roots": ["PhoneType"]
        },
        "types": [
            ["PhoneType", "Choice", ["CO"], "", [
                [1, "predefined", "PhoneNumberTypes", [], ""],
                [2, "custom", "String", ["{3", "}10"], ""]
            ]],
            ["PhoneNumberTypes", "Enumerated", [], "", [
                [1, "Home", ""],
                [2, "Cell", ""],
                [3, "Work", ""]
            ]]
        ]
    }
    
    valid_xml_1 = """
        <PhoneType>Home</PhoneType>
    """

    valid_data_list = [
        valid_xml_1
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_x": "test incorrect field name"
        }
    ]

    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)       
        