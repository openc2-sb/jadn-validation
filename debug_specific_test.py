#!/usr/bin/env python3

# Test just the specific test function that's failing

import traceback

def main():
    try:
        # Import the specific test
        from jadnvalidation.tests.test_schema_validity import test_total_validity_with_opts
        
        print("Running test_total_validity_with_opts...")
        test_total_validity_with_opts()
        print("Test completed successfully!")
        
    except AttributeError as e:
        if "'NoneType' object has no attribute 'startswith'" in str(e):
            print(f"STARTSWITH ERROR: {e}")
            print("Full traceback:")
            traceback.print_exc()
        else:
            print(f"Other AttributeError: {e}")
            traceback.print_exc()
    except Exception as e:
        print(f"Other error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()