from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data
from jadnvalidation.utils.consts import XML


def test_type_int():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5", True, False]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", [], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>1</Root-Test>"""
    valid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_type_int_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/duration"], "", []]
      ]
    }
      
    valid_data_list = [1, 0, -1, 1000, -1000]      
    invalid_data_list = [1.75, "one", "1.7z5"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_date():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/date"], "", []]
      ]
    }
      
    valid_data_list = [1751677200]      
    invalid_data_list = [-1.57]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_date_time():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/date-time"], "", []]
      ]
    }
      
    valid_data_list = [1751677200]      
    invalid_data_list = [-1.57]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_date_time():
    root = "Root-Test"

    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/date-time"], "", []]
      ]
    }

    valid_xml_1 = """<Root-Test>1751677200</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    invalid_xml_1 = """<Root-Test>-1.57</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]

    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)
    assert err_count == 0

    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)

def test_type_int_time():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/time"], "", []]
      ]
    }
      
    valid_data_list = [1751677200]      
    invalid_data_list = [-1.57]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_time():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/time"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>1751677200</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    invalid_xml_1 = """<Root-Test>-1.57</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_date():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/date"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>101924</Root-Test>"""
    valid_xml_2 = """<Root-Test>105</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_type_int_day_time_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/dayTimeDuration"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>P3DT4H30M15S</Root-Test>"""
    valid_xml_2 = """<Root-Test>P3DT4H30M10S</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_type_int_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/duration"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>101924</Root-Test>"""
    valid_xml_2 = """<Root-Test>105</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_type_int_year_month_duration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/yearMonthDuration"], "", []]
      ]
    }

    valid_xml_1 = """<Root-Test>P2Y6M</Root-Test>"""
    valid_xml_2 = """<Root-Test>P2Y7M</Root-Test>"""
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]

    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_type_int_min():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["{2"], "", []]
      ]
    }
      
    valid_data_list = [3, 55]      
    invalid_data_list = [1, 0, -1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_max():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["}2"], "", []]
      ]
    }
      
    valid_data_list = [1, 2]      
    invalid_data_list = [3, 5] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_type_int_i8():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i8"], "", []]
      ]
    }
    
    valid_data_list = [-128, 127, 0, 1]      
    invalid_data_list = [-129, 128, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_i8():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i8"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>1</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    valid_xml_3 = """<Root-Test>127</Root-Test>"""
    valid_xml_4 = """<Root-Test>-128</Root-Test>"""
    invalid_xml_1 = """<Root-Test>128</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-129</Root-Test>"""
    invalid_xml_3 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_4 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3, valid_xml_4]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  
    
def test_type_int_i16():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i16"], "", []]
      ]
    }
    
    valid_data_list = [-32768, 32767, 0]      
    invalid_data_list = [-32769, 32768, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i32():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i32"], "", []]
      ]
    }
    
    valid_data_list = [-2147483648, 2147483647, 0]      
    invalid_data_list = [-2147483649, 2147483648, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_type_int_i64():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/i64"], "", []]
      ]
    }
    
    valid_data_list = [-9223372036854775808, 9223372036854775807, 0]      
    invalid_data_list = [-9223372036854775809, 9223372036854775808, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)    

def test_type_int_u8():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u8"], "", []]
      ]
    }
    
    valid_data_list = [255, 0]      
    invalid_data_list = [-1, 256, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int_u8():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u8"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>255</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    invalid_xml_1 = """<Root-Test>256</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 
    
def test_type_int_u16():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u16"], "", []]
      ]
    }
    
    valid_data_list = [65535, 0]      
    invalid_data_list = [65536, -1, "1"] 
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_u16():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u16"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>65535</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    invalid_xml_1 = """<Root-Test>65536</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_u32():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u32"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>429499999</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    valid_xml_3 = """<Root-Test>1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>-32769</Root-Test>"""
    invalid_xml_2 = """<Root-Test>4294967300</Root-Test>"""
    invalid_xml_3 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_4 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_u64():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/u64"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>429499999</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    valid_xml_3 = """<Root-Test>1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>-32769</Root-Test>"""
    invalid_xml_2 = """<Root-Test>429496730000000000000</Root-Test>"""
    invalid_xml_3 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_4 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_nonNegativeInteger():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/nonNegativeInteger"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>500</Root-Test>"""
    valid_xml_2 = """<Root-Test>0</Root-Test>"""
    valid_xml_3 = """<Root-Test>1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>-2</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_positiveInteger():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/positiveInteger"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>500</Root-Test>"""
    valid_xml_2 = """<Root-Test>2</Root-Test>"""
    valid_xml_3 = """<Root-Test>1</Root-Test>"""
    invalid_xml_1 = """<Root-Test>0</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_negativeInteger():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/negativeInteger"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>-5</Root-Test>"""
    valid_xml_2 = """<Root-Test>-500</Root-Test>"""
    valid_xml_3 = """<Root-Test>-123132</Root-Test>"""
    invalid_xml_1 = """<Root-Test>0</Root-Test>"""
    invalid_xml_2 = """<Root-Test>1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_xml_type_int_nonPositiveInteger():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/nonPositiveInteger"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>0</Root-Test>"""
    valid_xml_2 = """<Root-Test>-500</Root-Test>"""
    valid_xml_3 = """<Root-Test>-123132</Root-Test>"""
    invalid_xml_1 = """<Root-Test>2</Root-Test>"""
    invalid_xml_2 = """<Root-Test>1</Root-Test>"""
    invalid_xml_3 = """<Root-Test>one</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list) 

def test_type_int_gYear():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYear"], "", []]
      ]
    }
    # python is "helpful" about truncating zeroes in integers. integer-formatted 0000 0r -0010 
    # will be made unusable. we plan to have the UI give these as formatted strings, but have some tests to handle int entries.  
    valid_data_list = [1999, -1000, "1999", "0000", "-0010", "2025Z", "2024-05:00"]      
    invalid_data_list = [1.75, "one", "1.7z5", 93, 444, "90", "100"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int_gYear():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYear"], "", []]
      ]
    }
    
    valid_xml_1 = """<Root-Test>2004</Root-Test>"""  # 2004
    valid_xml_2 = """<Root-Test>2004-05:00</Root-Test>""" # 2004, US Eastern Standard Time
    valid_xml_3 = """<Root-Test>12004</Root-Test>""" # 	the year 12004
    valid_xml_4 = """<Root-Test>0922</Root-Test>""" # the year 922
    valid_xml_5 = """<Root-Test>-0045</Root-Test>""" # 45 BC
    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""
    invalid_xml_3 = """<Root-Test>1.7z5</Root-Test>"""
    invalid_xml_4 = """<Root-Test>99</Root-Test>""" # the century must not be truncated
    invalid_xml_5 = """<Root-Test>444</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3, valid_xml_4, valid_xml_5]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4, invalid_xml_5]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)      
   
def test_type_int_gYearMonth():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYearMonth"], "", []]
      ]
    }
      
    valid_data_list = ["1000-12", "-1000-05", "1000-12-05:00", "-1000-05Z"]      
    invalid_data_list = ["one", "1.7z5", 99, 1.750, 1000, "1000", "01-01", "1999-99", ""]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int_gYearMonth():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gYearMonth"], "", []]
      ]
    }
      
    valid_data_list = ["1000-12", "-1000-05", "1000-12-05:00", "-1000-05Z"]      
    invalid_data_list = ["one", "1.7z5", 99, 1.750, 1000, "1000", "01-01", "1999-99", ""]

    valid_xml_1 = """<Root-Test>1000-12</Root-Test>""" 
    valid_xml_2 = """<Root-Test>-1000-05</Root-Test>""" 
    valid_xml_3 = """<Root-Test>1000-12-05:00</Root-Test>""" 
    valid_xml_4 = """<Root-Test>-1000-05Z</Root-Test>""" 

    invalid_xml_1 = """<Root-Test>one</Root-Test>"""
    invalid_xml_2 = """<Root-Test>1.7z5</Root-Test>"""
    invalid_xml_3 = """<Root-Test>99</Root-Test>"""
    invalid_xml_4 = """<Root-Test>1.750</Root-Test>""" 
    invalid_xml_5 = """<Root-Test>1000</Root-Test>"""
    invalid_xml_6 = """<Root-Test>01-01</Root-Test>"""
    invalid_xml_7 = """<Root-Test>1999-99</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3, valid_xml_4]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4, invalid_xml_5, invalid_xml_6, invalid_xml_7]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)   

def test_type_int_gMonthDay():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gMonthDay"], "", []]
      ]
    }
      
    valid_data_list = ["--04-12", "--04-12Z", "--04-12-01:00"]      
    invalid_data_list = [1.75, "one", "1.7z5", "--4-6", "04-12"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_type_int_gMonthDay():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/gMonthDay"], "", []]
      ]
    }
  
    valid_xml_1 = """<Root-Test>--04-12</Root-Test>""" 
    valid_xml_2 = """<Root-Test>--04-12Z</Root-Test>""" 
    valid_xml_3 = """<Root-Test>--04-12-01:00</Root-Test>""" 

    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""
    invalid_xml_3 = """<Root-Test>1.7z5</Root-Test>"""
    invalid_xml_4 = """<Root-Test>--4-6</Root-Test>""" 
    invalid_xml_5 = """<Root-Test>04-12</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4, invalid_xml_5]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)     
    
def test_type_int_yearMonthDuration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/yearMonthDuration"], "", []]
      ]
    }
      
    valid_data_list = ["P1Y11M", "P17M", "-P11Y"]      
    invalid_data_list = [1.75, "one", "1.7z5", "P", "P3Y6M7DT23H01M30S", "P2DT3H"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_yearMonthDuration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/yearMonthDuration"], "", []]
      ]
    }

    valid_xml_1 = """<Root-Test>P1Y11M</Root-Test>""" 
    valid_xml_2 = """<Root-Test>P17M</Root-Test>""" 
    valid_xml_3 = """<Root-Test>-P11Y</Root-Test>""" 

    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""
    invalid_xml_3 = """<Root-Test>1.7z5</Root-Test>"""
    invalid_xml_4 = """<Root-Test>P3Y6M7DT23H01M30S</Root-Test>""" 
    invalid_xml_4 = """<Root-Test>P</Root-Test>""" 
    invalid_xml_4 = """<Root-Test>P2DT3H</Root-Test>""" 

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)
    
def test_type_int_dayTimeDuration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/dayTimeDuration"], "", []]
      ]
    }
      
    valid_data_list = ["P2DT3H", "PT30M", "PT10000M"]      
    invalid_data_list = [1.75, "one", "1.7z5", "P3Y6M7DT23H01M30S"]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_xml_type_int_dayTimeDuration():
    root = "Root-Test"
    
    j_schema = {
      "types": [
        ["Root-Test", "Integer", ["/dayTimeDuration"], "", []]
      ]
    }
      
    valid_xml_1 = """<Root-Test>P2DT3H</Root-Test>""" 
    valid_xml_2 = """<Root-Test>PT30M</Root-Test>""" 
    valid_xml_3 = """<Root-Test>PT10000M</Root-Test>""" 

    invalid_xml_1 = """<Root-Test>1.75</Root-Test>"""
    invalid_xml_2 = """<Root-Test>one</Root-Test>"""
    invalid_xml_3 = """<Root-Test>1.7z5</Root-Test>"""
    invalid_xml_4 = """<Root-Test>P3Y6M7DT23H01M30S</Root-Test>""" 

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2, invalid_xml_3, invalid_xml_4]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)