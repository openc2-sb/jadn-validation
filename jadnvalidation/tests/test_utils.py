from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.utils.consts import JSON
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
    
 # tests hitting jadnutils function    
def test_get_inherited_fields():
    """Test get_inherited_fields function."""
    
    sample_schema = {
        "meta": {
            "title": "Test Schema",
            "version": "1.0"
        },
        "types": [
            ["Person", "Record", [], "A person", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"],
                [3, "email", "String", [], "Optional email"]
            ]],
            ["Company", "Record", [], "A company", [
                [1, "name", "String", [], "Company name"],
                [2, "employees", "Person-Array", [], "List of employees"]
            ]],
            ["Person-Array", "ArrayOf", ["{*Person"], "Array of persons"],
            ["Status", "Enumerated", [], "Status values", [
                [1, "active", "Active status"],
                [2, "inactive", "Inactive status"]
            ]]
        ]
    }
    
    types = sample_schema["types"]
    field = ["Person", "Record", [], "A person"]
    result = get_inherited_fields(types, field)
    # This function returns empty list when no inheritance options are found
    assert isinstance(result, list)    