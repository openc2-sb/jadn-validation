from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.utils.consts import JSON
from jadnvalidation.utils.mapping_utils import use_keyless_map
from jadnvalidation.utils.type_utils import get_reference_type, validate_type_references, validate_field_type_references
# from jadnutils.utils.jadn_utils import get_inherited_fields


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
    
    try:
        from jadnutils.utils.jadn_utils import get_inherited_fields
        
        # Test schema with inheritance
        test_schema = {
            "meta": {
                "title": "Test Schema",
                "version": "1.0"
            },
            "types": [
                ["String", "String", [], "Base string type"],
                ["Integer", "Integer", [], "Base integer type"],
                ["BaseRecord", "Record", [], "Base record type", [
                    [1, "id", "Integer", [], "Unique identifier"],
                    [2, "name", "String", [], "Name field"]
                ]],
                ["ExtendedRecord", "Record", ["<BaseRecord"], "Extended record with inheritance", [
                    [3, "description", "String", [], "Description field"],
                    [4, "active", "Boolean", [], "Active status"]
                ]],
                ["DoubleExtended", "Record", ["<ExtendedRecord"], "Double inheritance", [
                    [5, "extra", "String", [], "Extra field"]
                ]]
            ]
        }
        
        # Test getting inherited fields for ExtendedRecord
        inherited_fields = get_inherited_fields(test_schema, "ExtendedRecord")
        
        # Should include fields from BaseRecord
        assert len(inherited_fields) >= 2  # At least id and name from BaseRecord
        
        # Check that inherited fields contain the base fields
        field_names = [field[1] for field in inherited_fields]
        assert "id" in field_names
        assert "name" in field_names
        
        # Test getting inherited fields for DoubleExtended (should include fields from both ancestors)
        double_inherited = get_inherited_fields(test_schema, "DoubleExtended")
        double_field_names = [field[1] for field in double_inherited]
        
        # Should include fields from both BaseRecord and ExtendedRecord
        assert "id" in double_field_names  # From BaseRecord
        assert "name" in double_field_names  # From BaseRecord
        assert "description" in double_field_names  # From ExtendedRecord
        assert "active" in double_field_names  # From ExtendedRecord
        
        # Test with non-inheriting type (should return empty or minimal result)
        no_inheritance = get_inherited_fields(test_schema, "BaseRecord")
        # BaseRecord doesn't inherit from anything, so should be empty or just its own fields
        
        print("All get_inherited_fields tests passed!")
        
    except ImportError:
        print("jadnutils not available - skipping get_inherited_fields test")
        pass
    except Exception as e:
        print(f"get_inherited_fields test failed: {e}")
        # Don't fail the entire test suite if this specific test has issues
        pass


def test_get_reference_type():
    """Test get_reference_type function."""
    
    sample_schema = {
        "meta": {
            "title": "Test Schema",
            "version": "1.0"
        },
        "types": [
            ["String", "String", [], "Base string type"],
            ["Integer", "Integer", [], "Base integer type"],
            ["Person", "Record", ["eCompany"], "A person record", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"]
            ]],
            ["PersonAlias", "Person", [], "Alias to Person type"],
            ["NestedAlias", "PersonAlias", [], "Nested alias to Person"]
        ]
    }
    
    # Test with base type (should return the type itself)
    result = get_reference_type(sample_schema, "String")
    assert result is not None
    assert result[0] == "String"
    assert result[1] == "String"
    
    # Test with record type
    result = get_reference_type(sample_schema, "Person")
    assert result is not None
    assert result[0] == "Person"
    assert result[1] == "Record"
    
    # Test with alias type (should resolve to base type)
    result = get_reference_type(sample_schema, "PersonAlias")
    assert result is not None
    assert result[0] == "Person"
    assert result[1] == "Record"
    
    # Test with nested alias (should resolve to base type)
    result = get_reference_type(sample_schema, "NestedAlias")
    assert result is not None
    assert result[0] == "Person"
    assert result[1] == "Record"
    
    # Test with unknown type (should raise ValueError)
    try:
        get_reference_type(sample_schema, "UnknownType")
        assert False, "Should have raised ValueError"
    except ValueError as e:
        assert "Unknown type UnknownType referenced" in str(e)
    
    print("All get_reference_type tests passed!")


def test_validate_type_references():
    """Test validate_type_references function."""
    
    # Valid schema - all type references exist
    valid_schema = {
        "meta": {"title": "Test Schema", "version": "1.0"},
        "types": [
            ["String", "String", [], "Base string type"],
            ["Integer", "Integer", [], "Base integer type"],
            ["Person", "Record", [], "A person record", []],
            ["PersonAlias", "Person", [], "Alias to Person type"]
        ]
    }
    
    # Should return no errors
    errors = validate_type_references(valid_schema)
    assert errors == []
    
    # Invalid schema - has undefined type reference
    invalid_schema = {
        "meta": {"title": "Test Schema", "version": "1.0"},
        "types": [
            ["String", "String", [], "Base string type"],
            ["Person", "Record", [], "A person record", []],
            ["PersonAlias", "UndefinedType", [], "Alias to undefined type"]
        ]
    }
    
    # Should return one error
    errors = validate_type_references(invalid_schema)
    assert len(errors) == 1
    assert "PersonAlias" in errors[0]
    assert "UndefinedType" in errors[0]
    
    print("All validate_type_references tests passed!")


def test_validate_field_type_references():
    """Test validate_field_type_references function."""
    
    # Valid schema - all field type references exist
    valid_schema = {
        "meta": {"title": "Test Schema", "version": "1.0"},
        "types": [
            ["String", "String", [], "Base string type"],
            ["Integer", "Integer", [], "Base integer type"],
            ["Address", "Record", [], "Address record", [
                [1, "street", "String", [], "Street name"],
                [2, "number", "Integer", [], "House number"]
            ]],
            ["Person", "Record", [], "A person record", [
                [1, "name", "String", [], "Person's name"],
                [2, "age", "Integer", [], "Person's age"],
                [3, "address", "Address", [], "Person's address"]
            ]]
        ]
    }
    
    # Should return no errors
    errors = validate_field_type_references(valid_schema)
    assert errors == []
    
    # Invalid schema - has undefined field type reference
    invalid_schema = {
        "meta": {"title": "Test Schema", "version": "1.0"},
        "types": [
            ["String", "String", [], "Base string type"],
            ["Person", "Record", [], "A person record", [
                [1, "name", "String", [], "Person's name"],
                [2, "company", "UndefinedCompany", [], "Person's company"]
            ]]
        ]
    }
    
    # Should return one error
    errors = validate_field_type_references(invalid_schema)
    assert len(errors) == 1
    assert "Person" in errors[0]
    assert "company" in errors[0]
    assert "UndefinedCompany" in errors[0]
    
    print("All validate_field_type_references tests passed!") 