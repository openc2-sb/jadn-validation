from jadnvalidation.tests.test_utils import validate_valid_data


def test_attr():
    root = "Root-Test"   
  
    j_schema = {
        "meta": {
            "title": "JADN Schema Start Up Template",
            "package": "http://JADN-Schema-Start-Up-Template-URI",
            "roots": ["Schema"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", ["/attr"], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }

    valid_data_list = [
            {
                "field_value_1": "abcdefg",
                "field_value_2": "abcdefg"
            },
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    