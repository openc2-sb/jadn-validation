#!/usr/bin/env python3

# Debug script to find the startswith error

try:
    from jadnvalidation.tests.test_utils import validate_valid_data
    from jadnvalidation.utils.type_utils import validate_type_references, validate_field_type_references
    
    # Simple test case to isolate the issue
    root = "Schema"    
    j_schema = {
        "meta": {
            "title": "Test",
            "package": "http://test.com",
            "roots": ["Schema"]
        },
        "types": [
            ["Schema", "Record", [], "", [
                [1, "name", "String", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [{"name": "test"}]
    
    print("Testing validate_type_references...")
    errors = validate_type_references(j_schema)
    print(f"Type reference errors: {errors}")
    
    print("Testing validate_field_type_references...")
    errors = validate_field_type_references(j_schema)
    print(f"Field reference errors: {errors}")
    
    print("Testing validate_valid_data...")
    err_count = validate_valid_data(j_schema, root, valid_data_list)
    print(f"Validation errors: {err_count}")
    
except Exception as e:
    import traceback
    print(f"Error: {e}")
    traceback.print_exc()