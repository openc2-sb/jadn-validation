#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, '/home/matt/workspace/jadn-validation')

import traceback

try:
    from jadnvalidation.tests.test_schema_validity import test_total_validity_with_opts
    
    print("Running test_total_validity_with_opts with detailed debugging...")
    
    # Monkey patch the array.py check_fields method to add debugging
    from jadnvalidation.data_validation import array
    from jadnvalidation.models.jadn.jadn_type import build_jadn_type_obj
    
    original_check_fields = array.Array.check_fields
    
    def debug_check_fields(self):
        print(f"DEBUG: Array check_fields called with {len(self.j_type.fields)} fields")
        for j_index, j_field in enumerate(self.j_type.fields):
            print(f"DEBUG: Field {j_index}: {j_field}")
            j_field_obj = build_jadn_type_obj(j_field)
            print(f"DEBUG: Built field obj - type_name: {j_field_obj.type_name}, base_type: {j_field_obj.base_type}")
            if j_field_obj.base_type is None:
                print(f"DEBUG: Found None base_type! Field details: {j_field}")
                print(f"DEBUG: j_field_obj details: id={getattr(j_field_obj, 'id', 'N/A')}, type_name={j_field_obj.type_name}, base_type={j_field_obj.base_type}, type_options={j_field_obj.type_options}")
                break
        return original_check_fields(self)
    
    array.Array.check_fields = debug_check_fields
    
    test_total_validity_with_opts()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()

print("Script finished.")