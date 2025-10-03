from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data


def test_derived_from_map():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["#Colors-Map"], "", []],
            ["Colors-Map", "Map", [], "", [
                [1, "red", "String", [], ""],
                [2, "green", "String", [], ""],
                [3, "blue", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = ['red','green','blue']
    invalid_data_list = ['redd',2,'test']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_derived_from_enum():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["#Colors-Map"], "", []],
            ["Colors-Map", "Enumerated", [], "", [
                [1, "red", "String", [], ""],
                [2, "green", "String", [], ""],
                [3, "blue", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = ['red','green','blue']
    invalid_data_list = ['redd',2,'test']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_derived_from_record():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["#Colors-Map"], "", []],
            ["Colors-Map", "Record", [], "", [
                [1, "red", "String", [], ""],
                [2, "green", "String", [], ""],
                [3, "blue", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = ['red','green','blue']
    invalid_data_list = ['redd',2,'test']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_derived_from_choice():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["#Colors-Map"], "", []],
            ["Colors-Map", "Choice", [], "", [
                [1, "red", "String", [], ""],
                [2, "green", "String", [], ""],
                [3, "blue", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = ['red','green','blue']
    invalid_data_list = ['redd',2,'test']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_derived_from_arrayof():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Enumerated", ["#Colors-Map"], "", []],
            ["Colors-Map", "ArrayOf", ["*Integer", "{1", "}3"], ""]
        ]
    }
    
    invalid_data_list = [1,2,3]
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)      