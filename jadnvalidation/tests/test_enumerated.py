
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_enum(): 
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", [], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = ['clubs','spades']
    invalid_data_list = [{'SuitEnum': 'asdfghjklasdfghjkl'}, {'SuitEnum': 'Aces'}, {'SuitEnum': 10},'asdfghjklasdfghjkl', 'Aces', 10]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_enum_multiple(): 
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "suit", "Enum-Test", ["[2", "]2"], ""]
            ]],
            ["Enum-Test", "Enumerated", [], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [{'suit': ['clubs', 'spades']}, {'suit': ['hearts', 'diamonds']}]
    invalid_data_list = [{'suit': 'clubs'}, {'suit': 'asdfghjklasdfghjkl'}, {'suit': 'Aces'}, {'SuitEnum': 10},'asdfghjklasdfghjkl', 'Aces', 10]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 
    
def test_xml_enum(): 
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", [], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>clubs</Root-Test>"""
    valid_xml_2 = """<Root-Test>diamonds</Root-Test>"""
    invalid_xml_1 = """<Root-Test>club</Root-Test>"""
    invalid_xml_2 = """<Root-Test>test</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)     
    
def test_enum_ids():
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["="], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_data_list = [10, 40]
    invalid_data_list = ['asdfghjklasdfghjkl', 'Aces', '10']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_enum_ids():
    root = "Root-Test"    
  
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["="], "", [
                [10, "clubs", ""],
                [20, "diamonds", ""],
                [30, "hearts", ""],
                [40, "spades", ""]
            ]]
        ]
    }
    
    valid_xml_1 = """<Root-Test>10</Root-Test>"""
    valid_xml_2 = """<Root-Test>40</Root-Test>"""
    invalid_xml_1 = """<Root-Test>clubs</Root-Test>"""
    invalid_xml_2 = """<Root-Test>hearts</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)       