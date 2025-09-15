from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data


def test_binary():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", [], "", []]
      ]
    }
    
    valid_bytes_1 = b"this is a test"
    valid_bytes_2 = b'\x80\x81\x82'
    valid_bytes_3 = "this is a test"
    invalid_bytes_1 = bytearray("hello", "utf-16")
    
    valid_data_list = [valid_bytes_1, valid_bytes_2, valid_bytes_3]
    invalid_data_list = [invalid_bytes_1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_min():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["{2"], "", []]
      ]
    }
    
    bytes_valid_1 = b"this is a test"
    bytes_valid_2 = b'\x80\x81\x82'
    bytes_invalid_1 = b"x"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80'
    
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2, bytes_invalid_3]    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_min_max():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["{4","}8"], "", []]
      ]
    }
    
    bytes_valid_1 = b"test"
    bytes_valid_2 = b'\x80\x81\x82\x82'
    bytes_invalid_1 = b"zzzzzzzzzzz"
    bytes_invalid_2 = bytearray("hello", "utf-16")
    bytes_invalid_3 = b'\x80\x80\x80\x80\x80\x80\x80\x80\x80'
    
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2, bytes_invalid_3]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_eui():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/eui"], "", []]
      ]
    }
    
    bytes_valid_1 = "00:00:5e:00:53:01"
    bytes_valid_2 = "00:00:5e:00:53:02"
    bytes_invalid_1 = b"zzzzb"
    bytes_invalid_2 = "zzzzs"
    valid_data_list = [bytes_valid_1, bytes_valid_2]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_binary_uuid():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/uuid"], "", []]
      ]
    }

    bytes_valid_1 = b'00010203-0405-0607-0809-0a0b0c0d0e0f'
    bytes_valid_2 = '\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
    bytes_valid_3 = b'00010203-0405-0607-0809-0a0b0c0d0e0f'
    bytes_valid_4 = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f'
    bytes_invalid_1 = b"zzzzb"
    bytes_invalid_2 = "zzzzs"
    valid_data_list = [bytes_valid_1, bytes_valid_2, bytes_valid_3, bytes_valid_4]
    invalid_data_list = [bytes_invalid_1, bytes_invalid_2]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_ipv4_addr(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/ipv4-addr"], "", []]
      ]
    }  
    
    valid_data_list = ['127.0.0.1']
    invalid_data_list = ["zz127.0.0.1zz"]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_ipv6_addr(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/ipv6-addr"], "", []]
      ]
    }  
    
    valid_data_list = ["2001:db8:3333:4444:5555:6666:1.2.3.4"]
    invalid_data_list = ["http://www.example.com"]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_base64(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/b64"], "", []]
      ]
    }  
    
    valid_data_list = [
        b"SGVsbG8gd29ybGQ=",  # "Hello world"
        b"U29tZSBkYXRh",      # "Some data"
        b"VGVzdA==",           # "Test"
        "ABCD",
        "test",
        "testtest"
      ]
    
    invalid_data_list = [
        b"SGVsbG8gd29ybGQ",   # Missing padding
        b"SGVsbG8@d29ybGQ=",  # Invalid character '@'
        b"12345",             # Not valid base64
        "test2"
      ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_hex_binary_x(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/x"], "", []]
      ]
    }  
    
    valid_data_list = [
        "0A1B2C3D4E",         # Even length, valid hex characters
        b"deadbeef",          # Bytes, valid hex
        "ABCDEF123456",       # Uppercase, valid hex
        b"00ff",              # Lowercase, valid hex
        "abcdef",             # Lowercase, valid hex
        "1234567890abcdef"   # Mixed digits and letters, even length
      ]
    
    invalid_data_list = [
        "0A1B2C3D4",          # Odd length
        b"deadbee",           # Odd length
        "0A1B2C3D4G",         # Contains invalid character 'G'
        "xyz123",             # Contains invalid characters 'x', 'y', 'z'
        b"deadbeeg",          # Contains invalid character 'g'
        "12345",              # Odd length
        12345                # Not a string or bytes
      ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_binary_hex_binary_x(): 
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Binary", ["/X"], "", []]
      ]
    }  
    
    valid_data_list = [
        "0A1B2C3D4E",         # Even length, valid hex characters
        b"deadbeef",          # Bytes, valid hex
        "ABCDEF123456",       # Uppercase, valid hex
        b"00ff",              # Lowercase, valid hex
        "abcdef",             # Lowercase, valid hex
        "1234567890abcdef"   # Mixed digits and letters, even length
      ]
    
    invalid_data_list = [
        "0A1B2C3D4",          # Odd length
        b"deadbee",           # Odd length
        "0A1B2C3D4G",         # Contains invalid character 'G'
        "xyz123",             # Contains invalid characters 'x', 'y', 'z'
        b"deadbeeg",          # Contains invalid character 'g'
        "12345",              # Odd length
        12345                # Not a string or bytes
      ]

    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)     