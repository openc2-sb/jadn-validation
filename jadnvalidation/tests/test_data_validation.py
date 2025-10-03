from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.tests.test_utils import Utils, validate_valid_data


def test_data_validation():  
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", ["{3", "}3"], "", [
                [1, "field_value_1", "String", ["{2"], ""],
                [2, "field_value_2", "Boolean", [], ""],
                [3, "field_value_3", "Integer", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            ["test", True, 123],
        ]  
    
    invalid_data_list = [
            ["test", True] ,
            { "Root-Test": "test" },
            ["t", "test", "test", 123, "test", "test", False]
        ]        
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_data_validation_multi_root():  
    roots = ["Root-Test-1", "Root-Test-2"]
    
    j_schema = {
        "meta": {
            "package": "http://test/v1.0",
            "roots": ["Root-Test-1", "Root-Test-2"]
        },
        "types": [
            ["Root-Test-1", "Record", [], "", [
                [1, "field_value_1", "String", [], ""]
            ]],
            ["Root-Test-2", "Record", [], "", [
                [1, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list_root_1 = [
            { 'field_value_1': "test" },
            { 'field_value_1': "" },
        ]  
    
    valid_data_list_root_2 = [
            { 'field_value_2': False },
            { 'field_value_2': True },
        ]      
    
    invalid_data_list = [
            ["test", True] ,
            { "Root-Test": "test" },
            ["t", "test", "test", 123, "test", "test", False]
        ]        

    utils1 = Utils(j_schema, roots[0], valid_data_list_root_1)
    err_count = utils1.validate_test()    
    assert err_count == 0
    
    utils2 = Utils(j_schema, roots[1], valid_data_list_root_2)
    err_count = utils2.validate_test()    
    assert err_count == 0
        
    utils3 = Utils(j_schema, roots[0], invalid_data_list)        
    err_count = utils3.validate_test()
    assert err_count == len(invalid_data_list)
    
    utils4 = Utils(j_schema, roots[1], invalid_data_list)
    err_count = utils4.validate_test()
    assert err_count == len(invalid_data_list)    

def test_data_validation_multiplicity():
    root = "Root-Test"
    
    j_schema = {
        "types": [
            ["Root-Test", "Array", [], "", [
                [1, "field_value_1", "String", ["[2"], ""],
                [2, "field_value_2", "Boolean", ["[0", "]2"], ""],
                [3, "field_value_3", "Integer", ["[0", "]-1"], ""],
                [4, "field_value_4", "Number", ["[0", "]-2"], ""]
            ]]
        ]
    }
    
    valid_data_list = [
            [["test", "test2"], [True], [123]],
        ]  
    
    invalid_data_list = [
            ["test", True] ,
            { "Root-Test": "test" },
            ["t", "test", "test", 123, "test", "test", False]
        ]        
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_valid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)