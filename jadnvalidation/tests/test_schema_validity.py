
from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML
from jadnvalidation.utils.type_utils import validate_field_type_references, validate_type_references


def test_metadata_validity(): 
    root = "Metadata"    
  
    j_schema = {
    "meta": {
      "title": "JADN Metaschema",
      "package": "http://oasis-open.org/openc2/jadn/v2.0/schema",
      "description": "Syntax of a JSON Abstract Data Notation (JADN) package.",
      "license": "CC-BY-4.0",
      "roots": ["Metadata"],
      "config": {
        "$FieldName": "^[$A-Za-z][_A-Za-z0-9]{0,63}$"
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
        [8, "namespaces", "PrefixNs", ["[0", "]-1"], "Referenced packages"],
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

      ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],

      ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],

      ["TypeRef", "String", [], "Reference to a type, matching ($NSID ':')? $TypeName"],

      ["Type", "Array", [], "", [
        [1, "type_name", "TypeName", [], ""],
        [2, "core_type", "JADN-Type-Enum", ["#JADN-Type"]],
        [3, "type_options", "Options", ["[0"], ""],
        [4, "type_description", "Description", ["[0"]],
        [5, "fields", "ArrayOf", ["*JADN-Type"]]
      ]],

      ["JADN-Type-Enum", "Enumerated", [], "", [
        [1, "Binary"],
        [2, "Boolean"],
        [3, "Integer"],
        [4, "Number"],
        [5, "String"],
        [6, "Enumerated"],
        [7, "Choice"],
        [8, "Array"],
        [9, "ArrayOf"],
        [10, "Map"],
        [11, "MapOf"],
        [12, "Record"]
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

      ["Items", "ArrayOf", ["*Item"]],

      ["Fields", "ArrayOf", ["*Field"]],

      ["Item", "Array", [], "", [
        [1, "item_id", "FieldID"],
        [2, "item_value", "String"],
        [3, "item_description", "Description", ["[0"]]
      ]],

      ["Field", "Array", [], "", [
        [1, "field_id", "FieldID"],
        [2, "field_name", "FieldName"],
        [3, "field_type", "TypeRef"],
        [4, "field_options", "Options", ["[0"]],
        [5, "field_description", "Description", ["[0"]]
      ]],

      ["FieldID", "Integer", ["y0"]],

      ["Options", "ArrayOf", ["*Option"]],

      ["Option", "String", ["{1"]],

      ["Description", "String"]
    ]
  }
    
    valid_data_1 = {
    "package": "http://example.fake",
    "roots": ["Record-Name"]
  }
    valid_data_2 = {
    "package": "http://example.fake"
  }

    
    
    valid_data_list = [ valid_data_1, valid_data_2 ]
    #invalid_data_list = [{'SuitEnum': 10},'Aces', 1]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    #err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    #assert err_count == len(invalid_data_list) 

def test_total_validity(): 
    root = "Schema"    
  
    j_schema = {
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
            
            ["Schema", "Record", [], "", [
                [1, "info", "String", [], ""],
                [2, "types", "String", ["[1", "]-1"], ""]]]
        ]}
      
    valid_data_list = [
        {
            "info" : "package",
            "types" : ["Typename2"]       
        }]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0

def test_total_validity(): 
    root = "Schema"    
  
    j_schema = {
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
        [8, "namespaces", "PrefixNs", ["[0", "]-1"], "Referenced packages"],
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

      ["TypeName", "String", ["%^[A-Z][-.A-Za-z0-9]{0,63}$"], "Name of a logical type"],

      ["FieldName", "String", ["%^[a-z][_A-Za-z0-9]{0,63}$"], "Name of a field in a structured type"],

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
        [1, "item_id", "FieldID", [], ""],
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

      ["Options", "ArrayOf", ["*Option"], ""],

      ["Option", "String", ["{1"], ""],

      ["Description", "String", [], ""]
    ]
  }
    
    
    valid_data_list = [            
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Binary", [], ""]]        
        },        
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "String", ["[0"], "", []]]        
        },             
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Integer", ["[0"], "", []]]        
        },          
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Number", ["[0"], "", []]]        
        },    
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Array", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Record", [], "", [
                [1, "thing", "String", [], ""]]
            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Map", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "ArrayOf", ["*String"], ""

            ]]        
        },      
        {
            "meta" : {"package" : "http://example.fake"},
            "types" : [["Typename", "MapOf", ["+Integer", "*String"], ""

            ]]        
        },

        {
            "meta": {
                "title": "Music Library",
                "package": "http://fake-audio.org/music-lib",
                "version": "1.1",
                "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
                "license": "CC0-1.0",
                "roots": ["Library"]
            },
  "types": [
    ["Library", "MapOf", ["+Barcode", "*Album", "{1"], "Top level of the library is a map of CDs by barcode", []],
    ["Barcode", "String", ["%^\\d{12}$"], "A UPC-A barcode is 12 digits", []],
    ["Album", "Record", [], "model for the album", [
        [1, "album_artist", "Artist", [], "primary artist associated with this album"],
        [2, "album_title", "String", [], "publisher's title for this album"],
        [3, "pub_data", "Publication-Data", [], "metadata about the album's publication"],
        [4, "tracks", "Track", ["]0"], "individual track descriptions and content"],
        [5, "total_tracks", "Integer", ["{1"], "total track count"],
        [6, "cover_art", "Image", ["[0"], "cover art image for this album"]
      ]],
    ["Publication-Data", "Record", [], "who and when of publication", [
        [1, "publisher", "String", [], "record label that released this album"],
        [2, "release_date", "String", ["/date"], "and when did they let this drop"]
      ]],
    ["Image", "Record", [], "pretty picture for the album or track", [
        [1, "image_format", "Image-Format", [], "what type of image file?"],
        [2, "image_content", "Binary", [], "the image data in the identified format"]
      ]],
    ["Image-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "PNG", ""],
        [2, "JPG", ""],
        [3, "GIF", ""]
      ]],
    ["Artist", "Record", [], "interesting information about a performer", [
        [1, "artist_name", "String", [], "who is this person"],
        [2, "instruments", "Instrument", ["q", "]0"], "and what do they play"]
      ]],
    ["Instrument", "Enumerated", [], "collection of instruments (non-exhaustive)", [
        [1, "vocals", ""],
        [2, "guitar", ""],
        [3, "bass", ""],
        [4, "drums", ""],
        [5, "keyboards", ""],
        [6, "percussion", ""],
        [7, "brass", ""],
        [8, "woodwinds", ""],
        [9, "harmonica", ""]
      ]],
    ["Track", "Record", [], "for each track there's a file with the audio and a metadata record", [
        [1, "location", "File-Path", [], "path to the audio file location in local storage"],
        [2, "metadata", "Track-Info", [], "description of the track"]
      ]],
    ["Track-Info", "Record", [], "information about the individual audio tracks", [
        [1, "track_number", "Integer", ["[1"], "track sequence number"],
        [2, "title", "String", [], "track title"],
        [3, "length", "Integer", ["{1"], "length of track in seconds; anticipated user display is mm:ss; minimum length is 1 second"],
        [4, "audio_format", "Audio-Format", [], "format of the digital audio"],
        [5, "featured_artist", "Artist", ["q", "[0", "]0"], "notable guest performers"],
        [6, "track_art", "Image", ["[0"], "each track can have optionally have individual artwork"],
        [7, "genre", "Genre", [], ""]
      ]],
    ["Audio-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "MP3", ""],
        [2, "OGG", ""],
        [3, "FLAC", ""],
        [4, "MP4", ""],
        [5, "AAC", ""],
        [6, "WMA", ""],
        [7, "WAV", ""]
      ]],
    ["Genre", "Enumerated", [], "Enumeration of common genres", [
        [1, "rock", ""],
        [2, "jazz", ""],
        [3, "hip_hop", ""],
        [4, "electronic", ""],
        [5, "folk_country_world", ""],
        [6, "classical", ""],
        [7, "spoken_word", ""]
      ]],
    ["File-Path", "String", [], "local storage location of file with directory path from root, filename, and extension"]
  ]
}

        
      
    ]
    invalid_data_list = [

         {'SuitEnum': 10},'Aces', 10
         
         ]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

def test_simple_metaschema_validation(): 
    root = "Schema"
  
    j_schema = {}


def test_total_validity_with_optsUPDATED(): 
    root = "Schema"    
  
    j_schema = {
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
    
    valid_data_list = [   {
  "meta": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "roots": ["Library"]
  },
  "types": [
    ["Library", "MapOf", ["+Barcode", "*Album", "{1"], "Top level of the library is a map of CDs by barcode", []],
    ["Barcode", "String", ["%^\\d{12}$"], "A UPC-A barcode is 12 digits", []],
    ["Album", "Record", [], "model for the album", [
        [1, "album_artist", "Artist", [], "primary artist associated with this album"],
        [2, "album_title", "String", [], "publisher's title for this album"],
        [3, "pub_data", "Publication-Data", [], "metadata about the album's publication"],
        [4, "tracks", "Track", ["]0"], "individual track descriptions and content"],
        [5, "total_tracks", "Integer", ["{1"], "total track count"],
        [6, "cover_art", "Image", ["[0"], "cover art image for this album"]
      ]],
    ["Publication-Data", "Record", [], "who and when of publication", [
        [1, "publisher", "String", [], "record label that released this album"],
        [2, "release_date", "String", ["/date"], "and when did they let this drop"]
      ]],
    ["Image", "Record", [], "pretty picture for the album or track", [
        [1, "image_format", "Image-Format", [], "what type of image file?"],
        [2, "image_content", "Binary", [], "the image data in the identified format"]
      ]],
    ["Image-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "PNG", ""],
        [2, "JPG", ""],
        [3, "GIF", ""]
      ]],
    ["Artist", "Record", [], "interesting information about a performer", [
        [1, "artist_name", "String", [], "who is this person"],
        [2, "instruments", "Instrument", ["q", "]0"], "and what do they play"]
      ]],
    ["Instrument", "Enumerated", [], "collection of instruments (non-exhaustive)", [
        [1, "vocals", ""],
        [2, "guitar", ""],
        [3, "bass", ""],
        [4, "drums", ""],
        [5, "keyboards", ""],
        [6, "percussion", ""],
        [7, "brass", ""],
        [8, "woodwinds", ""],
        [9, "harmonica", ""]
      ]],
    ["Track", "Record", [], "for each track there's a file with the audio and a metadata record", [
        [1, "location", "File-Path", [], "path to the audio file location in local storage"],
        [2, "metadata", "Track-Info", [], "description of the track"]
      ]],
    ["Track-Info", "Record", [], "information about the individual audio tracks", [
        [1, "track_number", "Integer", ["[1"], "track sequence number"],
        [2, "title", "String", [], "track title"],
        [3, "length", "Integer", ["{1"], "length of track in seconds; anticipated user display is mm:ss; minimum length is 1 second"],
        [4, "audio_format", "Audio-Format", [], "format of the digital audio"],
        [5, "featured_artist", "Artist", ["q", "[0", "]0"], "notable guest performers"],
        [6, "track_art", "Image", ["[0"], "each track can have optionally have individual artwork"],
        [7, "genre", "Genre", [], ""]
      ]],
    ["Audio-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "MP3", ""],
        [2, "OGG", ""],
        [3, "FLAC", ""],
        [4, "MP4", ""],
        [5, "AAC", ""],
        [6, "WMA", ""],
        [7, "WAV", ""]
      ]],
    ["Genre", "Enumerated", [], "Enumeration of common genres", [
        [1, "rock", ""],
        [2, "jazz", ""],
        [3, "hip_hop", ""],
        [4, "electronic", ""],
        [5, "folk_country_world", ""],
        [6, "classical", ""],
        [7, "spoken_word", ""]
      ]],
    ["File-Path", "String", [], "local storage location of file with directory path from root, filename, and extension"]
  ]
}   
    

    ]

    
    invalid_data_list = [
         {'SuitEnum': 10},'Aces', 10         
    ]
    
    errors = validate_type_references(j_schema)
    assert errors == []    
    
    errors = validate_field_type_references(j_schema)
    assert errors == []    
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
            
    err_count = validate_invalid_data(j_schema, root, invalid_data_list)
    assert err_count == len(invalid_data_list) 

    """
    ---
    
           
        {
  "meta": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "roots": ["Library"]
  },
  "types": [
    ["Library", "MapOf", ["+Barcode", "*Album", "{1"], "Top level of the library is a map of CDs by barcode", []],
    ["Barcode", "String", ["%^\\d{12}$"], "A UPC-A barcode is 12 digits", []],
    ["Album", "Record", [], "model for the album", [
        [1, "album_artist", "Artist", [], "primary artist associated with this album"],
        [2, "album_title", "String", [], "publisher's title for this album"],
        [3, "pub_data", "Publication-Data", [], "metadata about the album's publication"],
        [4, "tracks", "Track", ["]0"], "individual track descriptions and content"],
        [5, "total_tracks", "Integer", ["{1"], "total track count"],
        [6, "cover_art", "Image", ["[0"], "cover art image for this album"]
      ]],
    ["Publication-Data", "Record", [], "who and when of publication", [
        [1, "publisher", "String", [], "record label that released this album"],
        [2, "release_date", "String", ["/date"], "and when did they let this drop"]
      ]],
    ["Image", "Record", [], "pretty picture for the album or track", [
        [1, "image_format", "Image-Format", [], "what type of image file?"],
        [2, "image_content", "Binary", [], "the image data in the identified format"]
      ]],
    ["Image-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "PNG", ""],
        [2, "JPG", ""],
        [3, "GIF", ""]
      ]],
    ["Artist", "Record", [], "interesting information about a performer", [
        [1, "artist_name", "String", [], "who is this person"],
        [2, "instruments", "Instrument", ["q", "]0"], "and what do they play"]
      ]],
    ["Instrument", "Enumerated", [], "collection of instruments (non-exhaustive)", [
        [1, "vocals", ""],
        [2, "guitar", ""],
        [3, "bass", ""],
        [4, "drums", ""],
        [5, "keyboards", ""],
        [6, "percussion", ""],
        [7, "brass", ""],
        [8, "woodwinds", ""],
        [9, "harmonica", ""]
      ]],
    ["Track", "Record", [], "for each track there's a file with the audio and a metadata record", [
        [1, "location", "File-Path", [], "path to the audio file location in local storage"],
        [2, "metadata", "Track-Info", [], "description of the track"]
      ]],
    ["Track-Info", "Record", [], "information about the individual audio tracks", [
        [1, "track_number", "Integer", ["[1"], "track sequence number"],
        [2, "title", "String", [], "track title"],
        [3, "length", "Integer", ["{1"], "length of track in seconds; anticipated user display is mm:ss; minimum length is 1 second"],
        [4, "audio_format", "Audio-Format", [], "format of the digital audio"],
        [5, "featured_artist", "Artist", ["q", "[0", "]0"], "notable guest performers"],
        [6, "track_art", "Image", ["[0"], "each track can have optionally have individual artwork"],
        [7, "genre", "Genre", [], ""]
      ]],
    ["Audio-Format", "Enumerated", [], "can only be one, but can extend list", [
        [1, "MP3", ""],
        [2, "OGG", ""],
        [3, "FLAC", ""],
        [4, "MP4", ""],
        [5, "AAC", ""],
        [6, "WMA", ""],
        [7, "WAV", ""]
      ]],
    ["Genre", "Enumerated", [], "Enumeration of common genres", [
        [1, "rock", ""],
        [2, "jazz", ""],
        [3, "hip_hop", ""],
        [4, "electronic", ""],
        [5, "folk_country_world", ""],
        [6, "classical", ""],
        [7, "spoken_word", ""]
      ]],
    ["File-Path", "String", [], "local storage location of file with directory path from root, filename, and extension"]
  ]
}   
    
    ---
    """