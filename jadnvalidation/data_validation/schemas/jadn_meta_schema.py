j_meta_roots = ["Schema"]
j_meta_schema = {
    "meta": {
        "title": "JADN Metaschema",
        "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
        "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
        "license": "CC-BY-4.0",
        "roots": ["Schema"],
        "config": {
            # "$MaxBinary": 255,
            "$MaxBinary": 500,
            # "$MaxString": 255,
            "$MaxString": 1000,
            "$MaxElements": 1000,
            "$Sys": "$",
            # "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            # "$TypeName": "^[A-Z][-$A-Za-z0-9]*(\\$[A-Za-z0-9]+)?$",  # Allow optional $suffix for types like "Party$type"
            # "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]*(\\$[A-Za-z0-9]+)?$",  # Allow both uppercase and lowercase initial
            "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]{0,63}$",
            # "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            # "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$",  # Adjusted to allow $ for system fields and uppercase first char for OSCAL
            "$FieldName": "^[A-Za-z$][-_$A-Za-z0-9]{0,63}$", 
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
        }        
    },

    "types": [
        ["Schema", "Record", [], "Definition of a JADN package", [
            [1, "meta", "Metadata", ["[0"], "Information about this package"],
            [2, "types", "Type", ["[1", "]-1"], "Types defined in this package"]
        ]],

        ["Metadata", "Map", [], "Information about this package", [
            [1, "package", "Namespace", [], "Unique name/version of this package"],
            [2, "version", "String", ["{1", "[0"], "Incrementing version within package"],
            [3, "title", "String", ["{1", "[0"], "Title"],
            [4, "description", "String", ["{1", "[0"], "Description"],
            [5, "comment", "String", ["{1", "[0"], "Comment"],
            [6, "copyright", "String", ["{1", "[0"], "Copyright notice"],
            [7, "license", "String", ["{1", "[0"], "SPDX licenseId of this package"],
            [8, "namespaces", "PrefixNS", ["[0", "]-1"], "Referenced packages"],
            [9, "roots", "TypeName", ["[0", "]-1"], "Roots of the type tree(s) in this package"],
            [10, "config", "Config", ["[0"], "Configuration variables"],
            [11, "jadn_version", "Namespace", ["[0"], "JADN Metaschema package"]
        ]],

        ["PrefixNS", "Array", [], "Prefix corresponding to a namespace IRI", [
            [1, "prefix", "NSID", [], "Namespace prefix string"],
            [2, "namespace", "Namespace", [], "Namespace IRI"]
        ]],

        ["Config", "Map", ["{1"], "Config vars override JADN defaults", [
            [1, "$MaxBinary", "Integer", ["y1", "[0"], "Package max octets, default = 255"],
            [2, "$MaxString", "Integer", ["y1", "[0"], "Package max characters, default = 255"],
            [3, "$MaxElements", "Integer", ["y1", "[0"], "Package max items/properties, default = 255"],
            [4, "$Sys", "String", ["{1", "}1", "[0"], "System character for TypeName, default = '.'"],
            [5, "$TypeName", "String", ["/regex", "[0"], "Default = ^[A-Za-z][-_$A-Za-z0-9]{0,63}$"],
            [6, "$FieldName", "String", ["/regex", "[0"], "Default = ^[A-Za-z$][-_$A-Za-z0-9]{0,63}$"],
            [7, "$NSID", "String", ["/regex", "[0"], "Default = ^([A-Za-z][A-Za-z0-9]{0,7})?$"]
        ]],

        ["Namespace", "String", ["/uri"], "Unique name of a package"],

        ["NSID", "String", ["%^([A-Za-z][A-Za-z0-9]{0,7})?$"], "Namespace prefix matching $NSID"],

        # ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],
        ["TypeName", "String", ["%^[A-Za-z][-_$A-Za-z0-9]{0,63}$"], "Name of a logical type"],

        # ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],
        ["FieldName", "String", ["%^[A-Za-z][-_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],

        ["TypeRef", "String", [], "Reference to a type, matching ($NSID ':')? $TypeName"],

        ["Type", "Array", [], "", [
            [1, "type_name", "TypeName", [], ""],
            [2, "core_type", "Enumerated", ["#JADN-Type"], ""],
            [3, "type_options", "Options", ["[0"], ""],
            [4, "type_description", "Description", ["[0"], ""],
            [5, "fields", "JADN-Type", ["[0", "&2"], ""]
        ]],

        ["JADN-Type", "Choice", [], "", [
            [1, "Binary", "Empty", [], ""],
            [2, "Boolean", "Empty", [], ""],
            [3, "Integer", "Empty", [], ""],
            [4, "Number", "Empty", [], ""],
            [5, "String", "Empty", [], ""],
            [6, "Enumerated", "Items", [], ""],
            [7, "Choice", "Fields", [], ""],
            [8, "Array", "Fields", [], ""],
            [9, "ArrayOf", "Empty", [], ""],
            [10, "Map", "Fields", [], ""],
            [11, "MapOf", "Empty", [], ""],
            [12, "Record", "Fields", [], ""]
        ]],

        ["Empty", "Array", ["}0"], "", []],

        ["Items", "ArrayOf", ["*Item"], ""],

        ["Fields", "ArrayOf", ["*Field"], ""],

        ["Item", "Array", [], "", [
            [1, "item_id", "ItemID", [], ""],
            [2, "item_value", "String", [], ""],
            [3, "item_description", "Description", ["[0"], ""]
        ]],

        ["Field", "Array", [], "", [
            [1, "field_id", "FieldID", [], ""],
            [2, "field_name", "FieldName", [], ""],
            [3, "field_type", "TypeRef", [], ""],
            [4, "field_options", "Options", ["[0"], ""],
            [5, "field_description", "Description", ["[0"], ""]
        ]],

        ["FieldID", "Integer", ["y0"], ""],

        ["ItemID", "Integer", [], ""],

        ["Options", "ArrayOf", ["*Option"], ""],

        ["Option", "String", ["{1"], ""],

        ["Description", "String", [], ""]
    ]
}
j_meta_schema_updated ={
  "meta": {
    "title": "JADN Metaschema",
    "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
    "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
    "license": "CC-BY-4.0",
    "roots": ["Schema"],
    "config": {
            # "$MaxBinary": 255,
            "$MaxBinary": 500,
            # "$MaxString": 255,
            "$MaxString": 1000,
            "$MaxElements": 1000,
            "$Sys": "$",
            # "$TypeName": "^[A-Z][-$A-Za-z0-9]{0,63}$",
            # "$TypeName": "^[A-Z][-$A-Za-z0-9]*(\\$[A-Za-z0-9]+)?$",  # Allow optional $suffix for types like "Party$type"
            # "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]*(\\$[A-Za-z0-9]+)?$",  # Allow both uppercase and lowercase initial
            "$TypeName": "^[A-Za-z][-_$A-Za-z0-9]{0,63}$",
            # "$FieldName": "^[a-z][_A-Za-z0-9]{0,63}$",
            # "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$",  # Adjusted to allow $ for system fields and uppercase first char for OSCAL
            "$FieldName": "^[A-Za-z$][-_$A-Za-z0-9]{0,63}$", 
            "$NSID": "^[A-Za-z][A-Za-z0-9]{0,7}$"
    }
  },
  "types": [
    ["Schema", "Record", [], "Definition of a JADN package", [
      [1, "meta", "Metadata", ["[0"], "Information about this package"],
      [2, "types", "Type", ["q", "]-1"], "Types defined in this package"]
    ]],
    ["Metadata", "Map", [], "Information about this package", [
      [1, "package", "Namespace", [], "Unique name/version of this package"],
      [2, "version", "String", ["{1", "[0"], "Incrementing version within package"],
      [3, "title", "String", ["{1", "[0"], "Title"],
      [4, "description", "String", ["{1", "[0"], "Description"],
      [5, "comment", "String", ["{1", "[0"], "Comment"],
      [6, "copyright", "String", ["{1", "[0"], "Copyright notice"],
      [7, "license", "String", ["{1", "[0"], "SPDX licenseId of this package"],
      [8, "namespaces", "PrefixNs", ["q", "[0", "]-1"], "Referenced packages"],
      [9, "roots", "TypeName", ["q", "[0", "]-1"], "Roots of the type tree(s) in this package"],
      [10, "config", "Config", ["[0"], "Configuration variables"],
      [11, "jadn_version", "Namespace", ["[0"], "JADN Metaschema package"]
    ]],
    ["PrefixNs", "Array", [], "Prefix corresponding to a namespace IRI", [
      [1, "prefix", "NSID", [], "Namespace prefix string"],
      [2, "namespace", "Namespace", [], "Namespace IRI"]
    ]],
    ["Config", "Map", ["{1"], "Config vars override JADN defaults", [
      [1, "$MaxBinary", "Integer", ["w1", "[0"], "Package max octets"],
      [2, "$MaxString", "Integer", ["w1", "[0"], "Package max characters"],
      [3, "$MaxElements", "Integer", ["w1", "[0"], "Package max items/properties"],
      [4, "$Sys", "String", ["{1", "}1", "[0"], "System character for TypeName"],
      [5, "$TypeName", "String", ["/regex", "[0"], ""],
      [6, "$FieldName", "String", ["/regex", "[0"], ""],
      [7, "$NSID", "String", ["/regex", "[0"], ""]
    ]],
    ["Namespace", "String", ["/uri"], "Unique name of a package"],
    ["NSID", "String", ["%^([A-Za-z][A-Za-z0-9]{0,7})?$"], "Namespace prefix matching $NSID"],
    ["TypeName", "String", ["%^[A-Za-z][-_$A-Za-z0-9]{0,63}$"], "Name of a logical type"],
    ["FieldName", "String", ["%^[A-Za-z$][-_$A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],
    ["TypeRef", "String", [], "Reference to a type, matching ($NSID ':')? $TypeName"],
    ["Type", "Array", [], "", [
      [1, "type_name", "TypeName", [], ""],
      [2, "core_type", "Enumerated", ["#JADN-Type"], ""],
      [3, "type_options", "TypeOptions", ["[0", "&2"], ""],
      [4, "type_description", "Description", ["[0"], ""],
      [5, "fields", "JADN-Type", ["[0", "&2"], ""]
    ]],
    ["JADN-Type", "Choice", [], "", [
      [1, "Binary", "Empty"],
      [2, "Boolean", "Empty"],
      [3, "Integer", "Empty"],
      [4, "Number", "Empty"],
      [5, "String", "Empty"],
      [6, "Enumerated", "Items"],
      [7, "Choice", "Fields"],
      [8, "Array", "Fields"],
      [9, "ArrayOf", "Empty"],
      [10, "Map", "Fields"],
      [11, "MapOf", "Empty"],
      [12, "Record", "Fields"]
    ]],
    ["TypeOptions", "Choice", [], "", [
      [1, "Binary", "BinaryOpts"],
      [2, "Boolean", "BooleanOpts"],
      [3, "Integer", "IntegerOpts"],
      [4, "Number", "NumberOpts"],
      [5, "String", "StringOpts"],
      [6, "Enumerated", "EnumeratedOpts"],
      [7, "Choice", "ChoiceOpts"],
      [8, "Array", "ArrayOpts"],
      [9, "ArrayOf", "ArrayOfOpts"],
      [10, "Map", "MapOpts"],
      [11, "MapOf", "MapOfOpts"],
      [12, "Record", "RecordOpts"]
    ]],
    ["Empty", "Array", ["}0"]],
    ["Items", "ArrayOf", ["*Item"]],
    ["Fields", "ArrayOf", ["*Field"]],
    ["Item", "Array", [], "", [
      [1, "item_id", "ItemID"],
      [2, "item_value", "String", ["[0"]],
      [3, "item_description", "Description", ["[0"]]
    ]],
    ["Field", "Array", [], "", [
      [1, "field_id", "FieldID"],
      [2, "field_name", "FieldName"],
      [3, "field_type", "TypeRef"],
      [4, "field_options", "FieldOpts", ["[0", "~1"]],
      [5, "field_description", "Description", ["[0"]]
    ]],
    ["FieldID", "Integer", ["y0"]],
    ["ItemID", "Integer", []],
    ["FieldOpts", "Map", ["~1"], "", [
      [91, "minOccurs", "Integer", ["w0", "[0", "Z["]],
      [93, "maxOccurs", "Integer", ["w-2", "[0", "Z]"]],
      [38, "tagId", "Integer", ["[0", "Z&"]],
      [75, "key", "Boolean", ["[0", "ZK"]],
      [76, "link", "Boolean", ["[0", "ZL"]],
      [78, "not", "Boolean", ["[0", "ZN"]],
      [123, "minLength", "Integer", ["[0", "Z{"]],
      [125, "maxLength", "Integer", ["[0", "Z}"]],
      [117, "default", "Binary", ["[0", "Zu"]],
      [118, "const", "Binary", ["[0", "Zv"]],
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [69, "scale", "Integer", ["[0", "Zundefined"]],
      [121, "minInclusive", "Integer", ["[0", "Zw"]],
      [122, "maxInclusive", "Integer", ["[0", "Zx"]],
      [119, "minExclusive", "Integer", ["[0", "Zy"]],
      [120, "maxExclusive", "Integer", ["[0", "Zz"]],
      [37, "pattern", "String", ["/regex", "[0", "Z%"]],
      [43, "keyType", "String", ["[0", "Z+"], "edited type, was TypeRef"],
      [42, "valueType", "String", ["[0", "Z*"], "edited type, was TypeRef"],
      [61, "id", "Boolean", ["[0", "Z="]],
      [35, "enum", "String", ["[0", "Z#"], "edited type, was TypeRef"],
      [62, "pointer", "String", ["[0", "Z>"], "edited type, was TypeRef"],
      [999, "keyless", "Integer", ["y0", "[0", "Z~"]],
      [67, "combine", "String", ["{1", "}1", "[0", "ZC"]],
      [113, "unique_ordered", "Boolean", ["[0", "Zq"]],
      [115, "set", "Boolean", ["[0", "Zs"]],
      [98, "unordered", "Boolean", ["[0", "Zb"]],
      [998, "alias", "String", ["[0", "ZZ"]]   
    ]],
    ["AllOpts", "Map", ["~1"], "", [
      [97, "abstract", "Boolean", ["[0", "Za"]],
      [101, "extends", "TypeRef", ["[0", "Ze"]],
      [114, "restricts", "TypeRef", ["[0", "Zr"]],
      [102, "final", "Boolean", ["[0", "Zf"]]
    ]],
    ["BinaryOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [123, "minLength", "Integer", ["[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]],
      [117, "default", "Binary", ["[0", "Zu"]],
      [118, "const", "Binary", ["[0", "Zv"]]
    ]],
    ["BooleanOpts", "Map", ["eAllOpts", "~1"], "", [
      [117, "default", "Boolean", ["[0", "Zu"]],
      [118, "const", "Boolean", ["[0", "Zv"]]
    ]],
    ["IntegerOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [69, "scale", "Integer", ["[0", "Zundefined"]],
      [121, "minInclusive", "Integer", ["[0", "Zw"]],
      [122, "maxInclusive", "Integer", ["[0", "Zx"]],
      [119, "minExclusive", "Integer", ["[0", "Zy"]],
      [120, "maxExclusive", "Integer", ["[0", "Zz"]],
      [117, "default", "Integer", ["[0", "Zu"]],
      [118, "const", "Integer", ["[0", "Zv"]]
    ]],
    ["NumberOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [121, "minInclusive", "Number", ["[0", "Zw"]],
      [122, "maxInclusive", "Number", ["[0", "Zx"]],
      [119, "minExclusive", "Number", ["[0", "Zy"]],
      [120, "maxExclusive", "Number", ["[0", "Zz"]],
      [117, "default", "Number", ["[0", "Zu"]],
      [118, "const", "Number", ["[0", "Zv"]]
    ]],
    ["StringOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [121, "minInclusive", "Number", ["[0", "Zw"]],
      [122, "maxInclusive", "Number", ["[0", "Zx"]],
      [119, "minExclusive", "Number", ["[0", "Zy"]],
      [120, "maxExclusive", "Number", ["[0", "Zz"]],
      [117, "default", "Number", ["[0", "Zu"]],
      [118, "const", "Number", ["[0", "Zv"]],
      [37, "pattern", "String", ["/regex", "[0", "Z%"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]],
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]]
    ]],
    ["EnumeratedOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "Boolean", ["[0", "Z="]],
      [35, "enum", "TypeRef", ["[0", "Z#"]],
      [62, "pointer", "TypeRef", ["[0", "Z>"]]
    ]],
    ["ChoiceOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "Boolean", ["[0", "Z="]],
      [67, "combine", "String", ["{1", "}1", "[0", "ZC"]]
    ]],
    ["ArrayOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "String", ["%^[a-zA-Z0-9-]{1,16}$", "[0", "Z/"]],
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]]
    ]],
    ["ArrayOfOpts", "Map", ["eAllOpts", "~1"], "", [
      [42, "valueType", "TypeRef", ["Z*"]],
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]],
      [113, "unique_ordered", "Boolean", ["[0", "Zq"]],
      [115, "set", "Boolean", ["[0", "Zs"]],
      [98, "unordered", "Boolean", ["[0", "Zb"]]
    ]],
    ["MapOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "Boolean", ["[0", "Z="]],
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]],
      [999, "keyless", "Integer", ["w0", "[0", "Z~"]],
      [998, "alias", "String", ["[0", "ZZ"]]   
    ]],
    ["MapOfOpts", "Map", ["eAllOpts", "~1"], "", [
      [43, "keyType", "TypeRef", ["Z+"]],
      [42, "valueType", "TypeRef", ["Z*"]],
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]]
    ]],
    ["RecordOpts", "Map", ["eAllOpts", "~1"], "", [
      [123, "minLength", "Integer", ["w0", "[0", "Z{"]],
      [125, "maxLength", "Integer", ["w0", "[0", "Z}"]]
    ]],
    ["Format", "String", ["%^[a-zA-Z0-9]{1,16$"]],
    ["Description", "String"]
  ]
}