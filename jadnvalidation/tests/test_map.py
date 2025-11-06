
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_map():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": "molestias, amet nobis",
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
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
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_map_with_structures():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", ["[0", "]-1"], ""],
                [2, "field_value_2", "Record-Name", [], ""],
                [3, "field_value_3", "Array-Name", ["[0", "]-1"], ""]
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]],
            ["Array-Name", "Array", [], "", [
                [1, "field_value_1", "Integer", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {   "field_value_1": ["placeat repellendus sit", "another_string"],
                "field_value_2": {"field_value_1": "molestias, sit elit. sit",
                                  "field_value_2": "molestias, sit elit. sit"},
                "field_value_3": [[1, "molestias, sit elit. sit"]]
            }, 
            {   "field_value_2": {"field_value_1": "molestias, sit elit. sit",
                                  "field_value_2": "molestias, sit elit. sit"},
                "field_value_3": [[1, "molestias, sit elit. sit"], [1, "molestias, sit elit. sit"]]
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
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
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_map_non_sequential():
    root = "Root-Test"
    
    j_schema = {
        "info": {
            "package": "http://test/v1.0",
            "exports": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", [], ""],
                [7, "non_sequential", "String", [], ""],
                [4, "unordered", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "non_sequential": "molestias, sit elit. sit",
                "unordered": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": "molestias, amet nobis",
                "unordered": "repellendus architecto",
                "non_sequential": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
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
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_xml_map():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1>test field</field_value_1>
        <field_value_2>Darth Andeddu</field_value_2>
    </Root-Test>"""
    valid_xml_2 = """<Root-Test>
        <field_value_1>testing more</field_value_1>
        <field_value_2>Darth Atrius</field_value_2>
    </Root-Test>"""
    valid_xml_3 = """<Root-Test>
        <field_value_1>testing more 123</field_value_1>
        <field_value_2>Darth Bane</field_value_2>
    </Root-Test>"""
    
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1b>test field</field_value_1b>
        <field_value_2b>Darth Andeddu</field_value_2b>
    </Root-Test>"""
    invalid_xml_2 = """<Root-Test>
        <field_value_1>testing more</field_value_1>
    </Root-Test>"""
    invalid_xml_3 = """<Root-Test>
        <field_value_2>Darth Bane</field_value_2>
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
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)     
    
def test_map_min_max():
    root = "Root-Test"
    
    j_schema = {
            "meta": {
                "package": "http://test/v1.0",
                "roots": ["Root-Test"]
            },
            "types": [
                ["Root-Test", "Map", ["{2", "}2"], "", [
                    [1, "field_value_1", "String", [], ""],
                    [2, "field_value_2", "String", [], ""]
                ]]
            ]
        }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": "molestias, amet nobis",
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit",
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
    
def test_map_id():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "1": "placeat repellendus sit",
                "2": "molestias, sit elit. sit"
            }, 
            {
                "1": "molestias, amet nobis",
                "2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": "placeat repellendus sit",
            "field_value_2": "molestias, sit elit. sit"
        }, 
        {
            "1": True,
            "2": "repellendus architecto"
        },
        {
            "1": "molestias, amet nobis"
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
'''
def test_xml_map_id():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["="], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>
        <field_value_1 key="1">test field</field_value_1>
        <field_value_2 key="2">Darth Andeddu</field_value_2>
    </Root-Test>"""
    valid_xml_2 = """<Root-Test>
        <field_value_1 id="1">testing more</field_value_1>
        <field_value_2 id="2">Darth Atrius</field_value_2>
    </Root-Test>"""
    
    invalid_xml_1 = """<Root-Test>
        <field_value_1>test field</field_value_1>
        <field_value_2>Darth Andeddu</field_value_2>
    </Root-Test>"""
    invalid_xml_2 = """<Root-Test>
        <field_value_1 key="1"></field_value_1>
        <field_value_2 key="2">Darth Andeddu</field_value_2>
    </Root-Test>"""
    invalid_xml_3 = """<Root-Test>
        <field_value_1 key="1">Darth Raine</field_value_1>
    </Root-Test>"""       
    
    valid_data_list = [
        valid_xml_1,
        valid_xml_2   
    ]
    
    invalid_data_list = [
        invalid_xml_1,
        invalid_xml_2,
        invalid_xml_3        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_valid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 
'''  
    
def test_map_ref_field():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["IntegerTest", "Integer", ["{0"], ""],
            ["StringTest", "String", ["{0"], ""],
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "IntegerTest", [], ""],
                [2, "field_value_2", "StringTest", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": 123,
                "field_value_2": "molestias, sit elit. sit"
            }, 
            {
                "field_value_1": 321,
                "field_value_2": "repellendus architecto"
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": 123,
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_1": "test incorrect field name"
        },
        {
            "field_value_1": True
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_map_ref_record():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "rec_value_1", "Record-Name", [], ""]
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "field_value_1", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "rec_value_1": {
                    "field_value_1": "test"
                }
            }
    ]
    
    invalid_data_list = [
        {
            "field_value_1": 123,
            "field_value_2": "molestias, sit elit. sit",
            "field_value_3": "test extra field validation"
        }, 
        {
            "field_value_1": "test incorrect field name"
        },
        {
            "field_value_1": True
        }        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
    
def test_map_min_occurs():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", ["[1"], ""],
                [2, "field_value_2", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            },
            {
                "field_value_1": "placeat repellendus sit"
            }            
    ]
    
    invalid_data_list = [
        {
            "field_value_2": "molestias, sit elit. sit"
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
    
    
def test_map_max_occurs():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "field_value_1", "String", ["1]"], ""],
                [2, "field_value_2", "String", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            {
                "field_value_1": "placeat repellendus sit",
                "field_value_2": "molestias, sit elit. sit"
            },
            {
                "field_value_1": "placeat repellendus sit"
            }            
    ]
    
    invalid_data_list = [
        {
            "field_value_21": "data 1",
            "field_value_11": "data 2"
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

     
def test_map_keyless_map():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["~1"], "", [
                [1, "A", "String", ["[0"], ""],
                [2, "B", "String", ["[0"], ""],
                [3, "C", "Boolean", ["[0"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            
        ["AI am any String"],["A1"],["BTwo"],["C"]
                          
    ]

    invalid_data_list = [

        ["3Two"], ["a1"], "A1",
        {"field_value_21": "data 1"}, 
        {"field_value_x": "test incorrect field name"},
        {"field_value_1": 123}        
    ]
    invalid_data_list = [

        ["3Two"], ["a1"]        
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
        
def test_map_keyless_map_2():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["~1"], "", [
                [1, "A", "String-Thing", ["[0"], ""],
                [2, "B", "Int-Thing", ["[0"], ""]
            ]],
            ["String-Thing", "String", [], "", []],
            ["Int-Thing", "Integer", [], "", []]
        ]
    }
    
    valid_data_list = [
            
        ["AI am any String"],["A1"],["B2"]
                          
    ]

    invalid_data_list = [

        ["3Two"], ["a1"], "A1", ["BHello"]       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)     

def test_map_keyless_map_inheritence():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["eIntermed-Test", "~1"], "", [
                [3, "C", "String-Thing", ["[0"], ""],
                [4, "D", "Int-Thing", ["[0"], ""]
            ]],
            ["Intermed-Test", "Map", ["eAbstract-Test", "~1"], "", [
                [2, "B", "Int-Thing", ["[0"], ""]
            ]],
            ["Abstract-Test", "Map", ["~1"], "", [
                [1, "A", "String-Thing", ["[0"], ""]
            ]],
            ["String-Thing", "String", [], "", []],
            ["Int-Thing", "Integer", [], "", []]
        ]
    }
    
    valid_data_list = [
            
        ["C1"],["D2"],["A1", "B2", "C3", "D4"],["B2", "C3", "D4"],["C3", "D4"]
                          
    ]

    invalid_data_list = [

        ["3Two"], ["a1"], "A1", ["BHello"]       
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_map_alias_fields():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", ["~1"], "", [
                [1, "A", "Pattern", ["[0"], ""],
                [2, "B", "MinOccurs", ["[0", "=["], ""]
            ]],
            ["Pattern", "String", ["=%"], "", []],
            ["MinOccurs", "Integer", [], "", []]
        ]
    }
    
    
    valid_data_list = [
            
        ["%I am any String"],["%1"],["[2"] #{"String-Thing": "I Am Any String"}, {"C", "1"}, {"[": 2}
                          
    ]

    invalid_data_list = [

        ["3Two"], ["A1"], "B1", ["BHello"]       
    ]
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

     
def test_map_alias_fields_basic():
    root = "Root-Test"
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Map", [], "", [
                [1, "A", "Pattern", ["[0"], ""],
                [2, "B", "Min-Occurs", ["[0"], ""]
            ]],
            ["Pattern", "String", ["=%"], "", []],
            ["Min-Occurs", "Integer", ["=["], "", []]
        ]
    }
    
    
    valid_data_list = [
            
        {"[": 2}, {"%": "Any String"} #["%I am any String"],["%1"],{"String-Thing": "I Am Any String"}, {"C", "1"}, {"[": 2}
                          
    ]

    invalid_data_list = [

        ["3Two"], ["A1"], "B1", ["BHello"]       
    ]
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
