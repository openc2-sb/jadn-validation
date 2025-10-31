from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.utils.consts import JSON
from jadnvalidation.utils.mapping_utils import use_keyless_map
from jadnutils.utils.jadn_utils import get_inherited_fields


def validate_valid_data(j_schema: dict, root: str, data_list: list, data_format: str = JSON) -> int:
    
    err_count = 0
    for data in data_list:
        try :
            j_validation = DataValidation(j_schema, root, data, data_format)
            j_validation.validate()
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count

def validate_invalid_data(j_schema: dict, root: str, data_list: list, data_format: str = JSON) -> int:
    
    err_count = 0
    for data in data_list:
        try :
            j_validation = DataValidation(j_schema, root, data, data_format)
            j_validation.validate()
        except Exception as err:
            err_count = err_count + 1
            print(err)
    return err_count

class Utils:
    
    j_schema: dict = None
    root: str = None
    tests: list = None
    data_format: str = None
    err_count: int = 0
    
    def __init__(self, j_schema: dict = None, root: str = None, tests: list = None, data_format: str = JSON) -> int:
        self.j_schema = j_schema
        self.root = root
        self.tests = tests
        self.data_format = data_format
        self.err_count = 0
    
    def validate_test(self) -> int:
        
        err_count = 0
        for test in self.tests:
            try :
                j_validation = DataValidation(self.j_schema, self.root, test, self.data_format)
                j_validation.validate()
            except Exception as err:
                err_count = err_count + 1
                print(err)
        return err_count


def test_use_keyless_map():
    """Unit test for use_keyless_map function"""
    
    # Test with None input
    assert use_keyless_map(None) is None
    
    # Test with empty list
    assert use_keyless_map([]) is None
    
    # Test with keyless map option present
    opts_with_keyless = ["~", "other_option"]
    result = use_keyless_map(opts_with_keyless)
    assert result == ['~', True]
    
    # Test with keyless map option with value
    opts_with_value = ["~value", "other_option"]
    result = use_keyless_map(opts_with_value)
    assert result == ['~', "value"]
    
    # Test with no keyless map option
    opts_without_keyless = ["other_option", "another_option"]
    result = use_keyless_map(opts_without_keyless)
    assert result is None
    
    # Test with keyless map option in middle of list
    opts_keyless_middle = ["first_option", "~test", "last_option"]
    result = use_keyless_map(opts_keyless_middle)
    assert result == ['~', "test"]
    
    # Test with empty string after tilde
    opts_empty_value = ["~"]
    result = use_keyless_map(opts_empty_value)
    assert result == ['~', True]
    
    print("All use_keyless_map tests passed!")
    
 # tests hitting jadnutils function    
def test_get_inherited_fields():
    """Test get_inherited_fields function."""
    
    sample_schema = {
        "meta": {
            "title": "Test Schema",
            "version": "1.0"
        },
        "types": [
            ["Person", "Record", ["eCompany"], "A person", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"],
                [3, "email", "String", [], "Optional email"]
            ]],
            ["Company", "Record", [], "A company", [
                [1, "name", "String", [], "Company name"],
                [2, "employees", "Person-Array", [], "List of employees"]
            ]],
            ["Person-Array", "ArrayOf", ["*Person"], "Array of persons", []],
            ["Status", "Enumerated", [], "Status values", [
                [1, "active", "Active status"],
                [2, "inactive", "Inactive status"]
            ]]
        ]
    }
    
    types = sample_schema["types"]
    field = ["Person", "Record", ["eCompany"], "A person", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"],
                [3, "email", "String", [], "Optional email"]
            ]]
    result = get_inherited_fields(types, field)
    
    # Assert result is a list with something in it
    assert isinstance(result, list)
    assert len(result) > 0 