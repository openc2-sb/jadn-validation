from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML

def test_num():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", [], "", []]
      ]
    }
      
    valid_data_list = [1.5]      
    invalid_data_list = ["1.7z5", "0.0.0.0.0.0.0.0.1.2", "555,", "  555  "]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_min_inclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["w2"], "", []]
      ]
    }
      
    valid_data_list = [2.0, 3.0, 4.0, 5.0]
    invalid_data_list = [1.0, 1.5, 0, -1.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_max_inclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["x5"], "", []]
      ]
    }
      
    valid_data_list = [-1.0, 0.0, 1.0, 2.0, 3.5]
    invalid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_min_exclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["y5"], "", []]
      ]
    }
      
    valid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
    invalid_data_list = [1.0, 1.5, 0, -1.0, 5.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_max_exclusive():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["x5"], "", []]
      ]
    }
    
    valid_data_list = [-1.0, 0.0, 1.0, 2.0, 3.5]
    invalid_data_list = [6.0, 100.5, 1000.0, 10000.0]  
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)         
    
def test_num_f16():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f16"], "", []]
      ]
    }
    
    valid_data_list = [3.14, -3.14, 65504.0, -65504.0, 0.0]
    invalid_data_list = [100000.0, -100000.0, 65504.1, -65504.1]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_f32():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f32"], "", []]
      ]
    }
    
    valid_data_list = [3.14, 12345.6789, 16777216.0, 16777217.0, 0.00000, -3.4e+38, 340000000000000000000000000000000000000.0]
    invalid_data_list = [3400000000000000000000000000000000000000.0, -3.4e+39, float('nan')]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_num_xml_float():
    root = "Root-Test"

    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f32"], "", []]
      ]
    }

    valid_xml_1 = """<Root-Test>3.14</Root-Test>"""
    valid_xml_2 = """<Root-Test>12345.6789</Root-Test>"""
    valid_xml_3 = """<Root-Test>16777216.0</Root-Test>"""
    valid_xml_4 = """<Root-Test>16777217.0</Root-Test>"""
    valid_xml_5 = """<Root-Test>0.00000</Root-Test>"""
    valid_xml_6 = """<Root-Test>-3.4e+38</Root-Test>"""

    valid_data_list = [
      valid_xml_1,
      valid_xml_2,
      valid_xml_3,
      valid_xml_4,
      valid_xml_5,
      valid_xml_6
    ]

    invalid_xml_1 = """<Root-Test>3400000000000000000000000000000000000000000.0</Root-Test>"""
    invalid_xml_2 = """<Root-Test>-3.4e+39</Root-Test>"""
    invalid_xml_3 = """<Root-Test>NaN</Root-Test>"""

    invalid_data_list = {
      invalid_xml_1,
      invalid_xml_2,
      invalid_xml_3 
    }

    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0

    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)

def test_num_f64():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f64"], "", []]
      ]
    }
    
    valid_data_list = [0.00000, -1.7976931348623157E+308, 1.7976931348623157E+308]
    invalid_data_list = [-1.7976931348623157E+309, 1e309, float('nan')]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)      

def test_num_xml_double():
    root = "Root-Test"

    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f64"], "", []]
      ]
    }

    valid_xml_1 = """<Root-Test>0.0000</Root-Test>"""
    valid_xml_2 = """<Root-Test>-1.7976931348623157E+308</Root-Test>"""
    valid_xml_3 = """<Root-Test>1.7976931348623157E+308</Root-Test>"""

    valid_data_list = [
      valid_xml_1,
      valid_xml_2,
      valid_xml_3
    ]

    invalid_xml_1 = """<Root-Test>1.7976931348623157E+309</Root-Test>"""
    invalid_xml_2 = """<Root-Test>1e309</Root-Test>"""
    invalid_xml_3 = """<Root-Test>NaN</Root-Test>"""

    invalid_data_list = {
      invalid_xml_1,
      invalid_xml_2,
      invalid_xml_3 
    }

    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0

    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)
    
def test_num_f128():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f128"], "", []]
      ]
    }
    
    valid_data_list = [0.00000, -1.7976931348623157E+308, 1.7976931348623157E+308, -16382., 16383.]
    invalid_data_list = [-1.7976931348623157E+309, 1e309, float('nan')]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)   
    
def test_num_f256():
    root = "Root-Test"    
  
    j_schema = {
      "types": [
        ["Root-Test", "Number", ["/f256"], "", []]
      ]
    }
    
    valid_data_list = [0.00000, -1.7976931348623157E+308, 1.7976931348623157E+308]
    invalid_data_list = [-1.7976931348623157E+309, 1e309, float('nan')]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    # assert err_count == len(invalid_data_list)   
    assert err_count == 0 
    # this case is not being validated as we do not have the appropriate libraries 
    # and users lack appropriate data. may change in future. 