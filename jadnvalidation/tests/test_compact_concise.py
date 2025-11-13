from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import CONCISE, COMPACT


def test_record():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        ["test", False], 
        ["test", True]
    ]

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
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, data_format=COMPACT)
    assert err_count > 0

def test_map():
    root = "Map-Name"
    jadn_schema = {
    "meta": {
        "roots": ["Map-Name"]
    },
    "types": [
        ["Map-Name", "Map", [], "", [
            [1, "field_1", "String", [], ""],
            [2, "field_2", "String", [], ""],
            [3, "field_3", "String", ["[0"], ""]
        ]]
    ]
    }

    valid_data_list = [
        {
            "field_1": "value1",
            "field_2": "value2"
        }
    ]

    invalid_data_list = [
        {
            "field_1": "value1",
            "field_2": "value2",
            "field_3": 5
        }
    ]

    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0

    err_count = validate_invalid_data(jadn_schema, root, invalid_data_list, data_format=COMPACT)
    assert err_count > 0