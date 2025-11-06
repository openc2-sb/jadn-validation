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

        ["PrefixNs", "Array", [], "Prefix corresponding to a namespace IRI", [
            [1, "prefix", "NSID", [], "Namespace prefix string"],
            [2, "namespace", "Namespace", [], "Namespace IRI"]
        ]],

        ["Config", "Map", ["{1"], "Config vars override JADN defaults", [
            [1, "$MaxBinary", "Integer", ["y1", "[0"], "Package max octets, default = 255"],
            [2, "$MaxString", "Integer", ["y1", "[0"], "Package max characters, default = 255"],
            [3, "$MaxElements", "Integer", ["y1", "[0"], "Package max items/properties, default = 255"],
            [4, "$Sys", "String", ["{1", "}1", "[0"], "System character for TypeName, default = '.'"],
            [5, "$TypeName", "String", ["/regex", "[0"], "Default = ^[A-Z][-.A-Za-z0-9]{0,63}$"],
            [6, "$FieldName", "String", ["/regex", "[0"], "Default = ^[a-z][_A-Za-z0-9]{0,63}$"],
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
j_meta_schema_updated = {
  "meta": {
    "title": "JADN Metaschema",
    "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
    "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
    "license": "CC-BY-4.0",
    "roots": ["Schema"],
    "config": {
      "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
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
      [1, "$MaxBinary", "Integer", ["w1", "[0", "u255"], "Package max octets"],
      [2, "$MaxString", "Integer", ["w1", "[0", "u255"], "Package max characters"],
      [3, "$MaxElements", "Integer", ["w1", "[0", "u255"], "Package max items/properties"],
      [4, "$Sys", "String", ["{1", "}1", "[0", "u."], "System character for TypeName"],
      [5, "$TypeName", "String", ["/regex", "[0", "^[A-Z][-.A-Za-z0-9]{0,63}$"], ""],
      [6, "$FieldName", "String", ["/regex", "[0", "u^[a-z][_A-Za-z0-9]{0,63}$"], ""],
      [7, "$NSID", "String", ["/regex", "[0", "u^([A-Za-z][A-Za-z0-9]{0,7})?$"], ""]
    ]],
    ["Namespace", "String", ["/uri"], "Unique name of a package"],
    ["NSID", "String", ["%^([A-Za-z][A-Za-z0-9]{0,7})?$"], "Namespace prefix matching $NSID"],
    ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],
    ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],
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
      [1, "item_id", "FieldID"],
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
    ["FieldOpts", "Map", ["~1"], "", [
      [91, "minOccurs", "Integer", ["w0", "[0", "=["]],
      [93, "maxOccurs", "Integer", ["w-2", "[0", "=]"]],
      [38, "tagId", "Integer", ["[0", "=&"]],
      [75, "key", "Boolean", ["[0", "=K"]],
      [76, "link", "Boolean", ["[0", "=L"]],
      [78, "not", "Boolean", ["[0", "=N"]],
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [123, "minLength", "Integer", ["[0", "={"]],
      [125, "maxLength", "Integer", ["[0", "=}"]],
      [117, "default", "Binary", ["[0", "=u"]],
      [118, "const", "Binary", ["[0", "=v"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]],
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [69, "scale", "Integer", ["[0", "=undefined"]],
      [121, "minInclusive", "Integer", ["[0", "=w"]],
      [122, "maxInclusive", "Integer", ["[0", "=x"]],
      [119, "minExclusive", "Integer", ["[0", "=y"]],
      [120, "maxExclusive", "Integer", ["[0", "=z"]],
      [37, "pattern", "String", ["/regex", "[0", "=%"]],
      [43, "keyType", "String", ["[0", "=+"], "edited type, was TypeRef"],
      [42, "valueType", "String", ["[0", "=*"], "edited type, was TypeRef"],
      [61, "id", "ID-Types", ["[0", "=="]],
      [35, "enum", "String", ["[0", "=#"], "edited type, was TypeRef"],
      [62, "pointer", "String", ["[0", "=>"], "edited type, was TypeRef"],
      [999, "keyless", "Integer", ["y0", "[0", "=~"]],
      [67, "combine", "String", ["{1", "}1", "[0", "=C"]],
      [113, "unique_ordered", "Boolean", ["[0", "=q"]],
      [115, "set", "Boolean", ["[0", "=s"]],
      [98, "unordered", "Boolean", ["[0", "=b"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["AllOpts", "Map", ["~1"], "", [
      [48, "nillable", "Boolean", ["[0", "=K"]],
      [97, "abstract", "Boolean", ["[0", "=a"]],
      [101, "extends", "TypeRef", ["[0", "=e"]],
      [114, "restricts", "TypeRef", ["[0", "=r"]],
      [102, "final", "Boolean", ["[0", "=f"]]
    ]],
    ["BinaryOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [123, "minLength", "Integer", ["[0", "={"]],
      [125, "maxLength", "Integer", ["[0", "=}"]],
      [117, "default", "Binary", ["[0", "=u"]],
      [118, "const", "Binary", ["[0", "=v"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["BooleanOpts", "Map", ["eAllOpts", "~1"], "", [
      [117, "default", "Boolean", ["[0", "=u"]],
      [118, "const", "Boolean", ["[0", "=K"]],
      [48, "nillable", "Boolean", ["[0", "=K"]],
      [65, "attr", "Boolean", ["[0", "=K"]]
    ]],
    ["IntegerOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [69, "scale", "Integer", ["[0", "=undefined"]],
      [121, "minInclusive", "Integer", ["[0", "=w"]],
      [122, "maxInclusive", "Integer", ["[0", "=x"]],
      [119, "minExclusive", "Integer", ["[0", "=y"]],
      [120, "maxExclusive", "Integer", ["[0", "=z"]],
      [117, "default", "Integer", ["[0", "=u"]],
      [118, "const", "Integer", ["[0", "=v"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["NumberOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [121, "minInclusive", "Number", ["[0", "=w"]],
      [122, "maxInclusive", "Number", ["[0", "=x"]],
      [119, "minExclusive", "Number", ["[0", "=y"]],
      [120, "maxExclusive", "Number", ["[0", "=z"]],
      [117, "default", "Number", ["[0", "=u"]],
      [118, "const", "Number", ["[0", "=v"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["StringOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [121, "minInclusive", "Number", ["[0", "=w"]],
      [122, "maxInclusive", "Number", ["[0", "=x"]],
      [119, "minExclusive", "Number", ["[0", "=y"]],
      [120, "maxExclusive", "Number", ["[0", "=z"]],
      [117, "default", "Number", ["[0", "=u"]],
      [118, "const", "Number", ["[0", "=v"]],
      [37, "pattern", "String", ["/regex", "[0", "=%"]],
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["EnumeratedOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "ID-Types", ["[0", "=="]],
      [35, "enum", "TypeRef", ["[0", "=#"]],
      [62, "pointer", "TypeRef", ["[0", "=>"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["ChoiceOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "ID-Types", ["[0", "=="]],
      [67, "combine", "String", ["{1", "}1", "[0", "=C"]]
    ]],
    ["ArrayOpts", "Map", ["eAllOpts", "~1"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]]
    ]],
    ["ArrayOfOpts", "Map", ["eAllOpts", "~1"], "", [
      [42, "valueType", "TypeRef", ["=*"]],
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]],
      [113, "unique_ordered", "Boolean", ["[0", "=q"]],
      [115, "set", "Boolean", ["[0", "=s"]],
      [98, "unordered", "Boolean", ["[0", "=b"]]
    ]],
    ["MapOpts", "Map", ["eAllOpts", "~1"], "", [
      [61, "id", "ID-Types", ["[0", "=="]],
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]],
      [999, "keyless", "Integer", ["w0", "[0", "=~"]]
    ]],
    ["MapOfOpts", "Map", ["eAllOpts", "~1"], "", [
      [43, "keyType", "TypeRef", ["=+"]],
      [42, "valueType", "TypeRef", ["=*"]],
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["RecordOpts", "Map", ["eAllOpts", "~1"], "", [
      [123, "minLength", "Integer", ["w0", "[0", "={"]],
      [125, "maxLength", "Integer", ["w0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["ID-Types", "Choice", ["CX"], "", [
      [1, "id_index", "Boolean", ["[0", "=="]],
      [2, "alias", "String", ["[0", "=="]]        
    ]],
    ["Format", "String", ["%^/[a-zA-Z0-9]{1,16}+$"]],
    ["Description", "String"]
  ]
}
    