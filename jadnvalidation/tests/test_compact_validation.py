from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import COMPACT
from jadnvalidation.tests.examples.test_oscal_catalog import oscal_catalog_j_schema

def test_record():
    root = "Root-Test"

    j_schema = {
        "meta": {
            "package": "http://test.com",
            "roots": ["Root-Test"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", [], ""],
                [2, "field_value_2", "Boolean", [], ""]
            ]]
        ]
    }
    
    valid_data_list = [
        ["test", False], 
        ["test", True]
    ]

    invalid_data_list = [
        {
            "field_value_1": "illum repellendus nobis",
            "field_value_2": True,
            "field_value_3": "test extra field validation"
        },         
        {
            "field_value_1": "two choice incorrectly",
            "field_value_2": True
        }, 
        {
            "field_value_x": "test incorrect field name"
        },
        {
            "field_value_1": 123
        }     
    ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list, data_format=COMPACT)
    assert err_count > 0

def test_map():
    root = "Map-Name"
    jadn_schema = {
    "meta": {
        "roots": ["Map-Name"]
    },
    "types": [
        ["Map-Name", "Map", [], "", [
            [1, "field_1", "String", [], ""],
            [2, "field_2", "String", [], ""],
            [3, "field_3", "String", ["[0"], ""]
        ]]
    ]
    }

    valid_data_list = [
        {
            "field_1": "value1",
            "field_2": "value2"
        }
    ]

    invalid_data_list = [
        {
            "field_1": "value1",
            "field_2": "value2",
            "field_3": 5
        }
    ]

    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0

    err_count = validate_invalid_data(jadn_schema, root, invalid_data_list, data_format=COMPACT)
    assert err_count > 0

def test_ipv4net():
    root = "Array-IPv4"
    jadn_schema = {
    "meta": {
        "title": "IPv4/6Net Testing",
        "package": "http://JADN-Schema-Start-Up-Template-URI",
        "roots": ["Array-IPv4", "Array-IPv6"]
    },
    "types": [
        ["Array-IPv4", "Array", ["/ipv4-net", "{1", "}2"], "", [
            [1, "ipv4_addr", "Binary", ["/ipv4-addr", "{1"], "IPv4 address as defined in [[RFC0791]](#rfc0791)"],
            [2, "prefix_length", "Integer", ["{0", "}32", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
        ]],
        ["Array-IPv6", "Array", ["/ipv6-net", "{1", "}2"], "", [
            [1, "ipv6_addr", "Binary", ["/ipv6-addr", "{1"], "IPv6 address as defined in [[RFC8200]](#rfc8200)"],
            [2, "prefix_length", "Integer", ["{0", "}128", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
        ]]
    ]
    }

    valid_data_list = [
        "127.0.0.1/8",
        "192.168.0.1/32"
    ]

    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0

def test_ipv6net():
    root = "Array-IPv6"
    jadn_schema = {
    "meta": {
        "title": "IPv4/6Net Testing",
        "package": "http://JADN-Schema-Start-Up-Template-URI",
        "roots": ["Array-IPv4", "Array-IPv6"]
    },
    "types": [
        ["Array-IPv4", "Array", ["/ipv4-net", "{1", "}2"], "", [
            [1, "ipv4_addr", "Binary", ["/ipv4-addr", "{1"], "IPv4 address as defined in [[RFC0791]](#rfc0791)"],
            [2, "prefix_length", "Integer", ["{0", "}32", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
        ]],
        ["Array-IPv6", "Array", ["/ipv6-net", "{1", "}2"], "", [
            [1, "ipv6_addr", "Binary", ["/ipv6-addr", "{1"], "IPv6 address as defined in [[RFC8200]](#rfc8200)"],
            [2, "prefix_length", "Integer", ["{0", "}128", "[0"], "CIDR prefix-length. If omitted, refers to a single host address."]
        ]]
    ]
    }

    valid_data_list = [
        "2001:0db8:85a3:0000:0000:8a2e:0370:7334/64",
        "fe80::1/128"
    ]

    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0

def test_oscal_catalog():
    jadn_schema = oscal_catalog_j_schema
    root = "Root"

    valid_data_list = [
        ["abcdefg", ["f16Ed71a-aDec-5Dcf-91f3-3CF86E377805", ["abcdefg", "2441-11-30T22:38:21.1945433544702419844899708958283237972913002308048468717301575962981120384921890826170438Z", "2000-02-29T03:55:06.615663927730283605421447244-06:00", "x", "#$o1sl_/\"Or3.OK#};Hf(G, ;&T@J{[bbgqY#W+ELc+z0H2<~W~1xK7%j>-QIX:fPJ1OhJOuxwz", "abcdefg"]]]
    ]

    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0

def test_null_vals():
    root = "Map-Name"
    jadn_schema = {
        "meta": {
            "roots": ["Map-Name"]
        },
        "types": [
            ["Map-Name", "Map", [], "", [
                [1, "record_1", "Record-Name", [], ""],
                [2, "record_2", "Record-Name", [], ""],
                [3, "record_3_optional", "Record-Name", ["[0"], ""]
            ]],
            ["Record-Name", "Record", [], "", [
                [1, "str_val_optional", "String", ["[0"], ""],
                [2, "int_val", "Integer", [], ""]
            ]]
        ]
        }
    
    valid_data_list = [
        {
            "record_1": {
                "int_val": 10
            },
            "record_2": {
                "str_val_optional": None,
                "int_val": 20
            }
        }
    ]
    err_count = validate_valid_data(jadn_schema, root, valid_data_list, data_format=COMPACT)    
    assert err_count == 0