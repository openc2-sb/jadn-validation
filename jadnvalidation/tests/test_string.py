from datetime import datetime

from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


def test_string_min_inclusive():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["w4"], "", []]
      ]
    }
    
    valid_data_list = ['four', 'en-US', 'multiple-small-parts', 'i-navajo', 'custom']
    invalid_data_list = ['1', '', 'one', '17']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_language():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/language"], "", []]
      ]
    }
    
    valid_data_list = ['en', 'en-US', 'multiple-small-parts', 'i-navajo', 'custom']
    invalid_data_list = ['hasmoreThan8Chars', '', 'a:colon', 'space bad']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_qname():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/QName"], "", []]
      ]
    }
    
    valid_data_list = ['w:q', 'www.example.com:Homepage']
    invalid_data_list = [':no_start', 'no_end:', 'no_colon']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_normalized_string():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/normalizedString"], "", []]
      ]
    }
    
    valid_data_list = ['letter', 'Capital', ':colon', '_underscore', 'intermed-hyphen', 'period.']
    invalid_data_list = [' start', 'end ', 'space between']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_name():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/name"], "", []]
      ]
    }
    
    valid_data_list = ['letter', 'Capital' ':colon', '_underscore', 'intermed-hyphen', 'period.']
    invalid_data_list = [' start', 'end ', '1one', '-hypnenStart', '.periodStart']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_token():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/token"], "", []]
      ]
    }
    
    valid_data_list = ['Milwaukee', 'hello world', 'one1 two2 three3']
    invalid_data_list = [' start', 'end ']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_regex():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/regex"], "", []]
      ]
    }
    
    valid_data_list = ['.*ABA.?', 'A(BB){1,4}']
    invalid_data_list = ['[', '\\']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_relative_json_pointer():
  
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/relative-json-pointer"], "", []]
      ]
    }
    
    valid_data_list = ['0/foo', '1/sin-city']
    invalid_data_list = ['/foo/0', '-1/sin-city']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_json_pointer():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/json-pointer"], "", []]
      ]
    }

    valid_data_list = ['/foo', '/foo/0', '/foo/1/sin-city']
    invalid_data_list = ['zzzz', ':///items.starfox']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_iri_ref():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/iri-reference"], "", []]
      ]
    }
    
    valid_data_list = ['mailto:info@example.com', 'file://localhost/absolute/path/to/file', 'https://www.example.珠宝/']
    invalid_data_list = ['zzzz', ':///items.starfox']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_iri():
    root = "Root-Test"  
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/iri"], "", []]
      ]
    }
    
    valid_data_list = ['http://puny£code.com', 'https://www.аррӏе.com/', 'https://www.example.珠宝/']
    invalid_data_list = ['zzzz', ':///items.starfox']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_uri_template():
    root = "Root-Test" 
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/uri-template"], "", []]
      ]
    }
    
    valid_data_list = ['https://www.example.com/api/v1/items/{/item_id}']
    invalid_data_list = ['zzzz', '/items/{}', 'https://www.example.com/api/v1/items/'] 
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_string_uri_ref():
    root = "Root-Test" 
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/uri-reference"], "", []]
      ]
    }
    
    valid_data_list = ['http://www.example.com/questions/3456/my-document', 'mailto:info@example.com', 'file://localhost/absolute/path/to/file']
    invalid_data_list = ['zzzz', '//./file_at_current_dir'] 
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_string_uri():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/uri"], "", []]
      ]
    }
    
    valid_data_list = ['http://www.example.com/questions/3456/my-document', 'mailto:info@example.com', 'foo://example.com:8042/over/there?name=ferret#nose']
    invalid_data_list = ['zzzz']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_ipv6():
    root = "Root-Test"  
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/ipv6"], "", []]
      ]
    }
    
    valid_data_list = ['2001:0db8:85a3:0000:0000:8a2e:0370:7334', '2001:db8::']
    invalid_data_list = ['zzzz2001:db8:3333:4444:5555:6666:7777:8888zzzz']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_ipv4():
    root = "Root-Test" 
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/ipv4"], "", []]
      ]
    }
    
    valid_data_list = ['127.0.0.1']
    invalid_data_list = ['zzzz127.0.0.1zzzz']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_idn_hostname():
    root = "Root-Test" 
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/idn-hostname"], "", []]
      ]
    }
    
    valid_data_list = ['xn--bcher-kva.example.com', 'ümlaut.example.com']
    invalid_data_list = ['invalid-end-.com','-invalid-start.com', 'long-hostname-that-exceeds-the-maximum-length-allowed-by-the-rfc-1034-standard-------------------------------------------------------------------------------------------------------------------------------------------------------------------.com']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)          
    
def test_string_hostname():
    root = "Root-Test"  
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/hostname"], "", []]
      ]
    }

    valid_data_list = ['example.com', '192.168.123.132']
    invalid_data_list = ['http://exam_ple.com','http://example.com']
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_idn_email():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/idn-email"], "", []]
      ]
    }

    valid_data_list = ['test@ツ.life']
    invalid_data_list = ['@jarvis@stark.com']
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_email():
    root = "Root-Test"  
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/email"], "", []]
      ]
    }

    valid_data_list = ['jarvis@stark.com',
        'jarvis@stark.eng.com',
        'jarvis@stark-eng.com',
        '1jarvis@stark-eng.com']
    invalid_data_list = ['@jarvis@stark.com',
        'zzjarviszz',
        'jarvis@stark-eng.com1']
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)

def test_string_pattern():
    root = "Root-Test"  
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["%^jarvis$"], "", []]
      ]
    }

    valid_data_list = ['jarvis']
    invalid_data_list = ['JARVIS','zzjarviszz']
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_time():
    root = "Root-Test" 
      
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/time"], "", []]
      ]
    }

    current_time = datetime.now().strftime("%H:%M:%S")

    valid_data_list = [current_time]
    invalid_data_list = ['hfdkjlajfdkl', 1596542285000]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_date():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/date"], "", []]
      ]
    }

    valid_data_list = ['2024-01-01']
    invalid_data_list = ['hfdkjlajfdkl',
        'yy2024-01-01zz',
        datetime.now(),
        1596542285000]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_string_datetime():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/date-time"], "", []]
      ]
    }

    valid_data_list = [
            '2023-08-13T16:07:54Z',
            '2023-08-13T16:07:54+02:00',
            '2023-08-13T16:07:54-02:00',
            '2023-08-13T16:07:54.123Z',
            '2023-08-13T16:07:54.123+02:00',
            '2023-08-13T16:07:54'
        ]
    # current spec writing points to RFC9557 IXDTF as the time standard for JADN. 
    # it is currently best used from a Rust Crate... it validates options outside ISO 8601 and RFC 3339
    # so these libraries alone are not sufficient to validate all possible options
    invalid_data_list = [
            '2023-08-13 16:07:54X',
            '2023-08-13 t 16:07:54-02:00',
            '2023-08-13t 16:07:54-02:00'
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
        
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_string_datetime():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/date-time"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>2023-08-13T16:07:54Z</Root-Test>"""
    valid_xml_2 = """<Root-Test>2023-08-13T16:07:54+02:00</Root-Test>"""
    valid_xml_3 = """<Root-Test>2023-08-13 16:07:54Z</Root-Test>"""
    invalid_xml_1 = """<Root-Test>hfdkjlajfdkl</Root-Test>"""
    invalid_xml_2 = """<Root-Test>yy2024-01-01zz</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2, valid_xml_3]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    
  
def test_str():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["{4", "}12"], "", []]
      ]
    }

    valid_data_list = ['test string']
    invalid_data_list = [4323, 'zz', 'testing string']
  
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list)
    
def test_xml_str():
    root = "Root-Test"
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["{4", "}12"], "", []]
      ]
    }
    
    valid_xml_1 = """<Root-Test>value1</Root-Test>"""
    valid_xml_2 = """<Root-Test>value one</Root-Test>"""
    invalid_xml_1 = """<Root-Test>v1</Root-Test>"""
    invalid_xml_2 = """<Root-Test>value too long</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)    

def test_xml_string_normalizedString():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/normalizedString"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>Test</Root-Test>"""
    valid_xml_2 = """<Root-Test>String</Root-Test>"""
    invalid_xml_1 = """<Root-Test> Test    Test</Root-Test>"""
    invalid_xml_2 = """<Root-Test>  Test  Test  </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_string_token():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/token"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>token</Root-Test>"""
    valid_xml_2 = """<Root-Test>token token2</Root-Test>"""
    invalid_xml_1 = """<Root-Test> </Root-Test>"""
    invalid_xml_2 = """<Root-Test>   </Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_string_language():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/language"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>abc</Root-Test>"""
    valid_xml_2 = """<Root-Test>abc-123</Root-Test>"""
    invalid_xml_1 = """<Root-Test>123</Root-Test>"""
    invalid_xml_2 = """<Root-Test>abc-</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_string_name():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/name"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>_name</Root-Test>"""
    valid_xml_2 = """<Root-Test>test-test.xml</Root-Test>"""
    invalid_xml_1 = """<Root-Test>123</Root-Test>"""
    invalid_xml_2 = """<Root-Test>abc def</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  

def test_xml_string_qname():
    root = "Root-Test"   
  
    j_schema = {
      "types": [
        ["Root-Test", "String", ["/qName"], "", []]
      ]
    }
        
    valid_xml_1 = """<Root-Test>abc:def</Root-Test>"""
    valid_xml_2 = """<Root-Test>test-key:value.property</Root-Test>"""
    invalid_xml_1 = """<Root-Test>123:abc</Root-Test>"""
    invalid_xml_2 = """<Root-Test>abc-def</Root-Test>"""

    valid_data_list = [valid_xml_1, valid_xml_2]
    invalid_data_list = [invalid_xml_1, invalid_xml_2]
  
    err_count = validate_valid_data(j_schema, root, valid_data_list, XML)    
    assert err_count == 0
              
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, XML)
    assert err_count == len(invalid_data_list)  