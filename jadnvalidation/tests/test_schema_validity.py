
from jadnvalidation.tests.test_utils import validate_invalid_data, validate_valid_data
from jadnvalidation.utils.consts import XML


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


def test_total_validity_with_opts(): 
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
      [1, "$MaxBinary", "Integer", ["y1", "[0", "u255"], "Package max octets"],
      [2, "$MaxString", "Integer", ["y1", "[0", "u255"], "Package max characters"],
      [3, "$MaxElements", "Integer", ["y1", "[0", "u255"], "Package max items/properties"],
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
      [1, "type_name", "TypeName"],
      [2, "core_type", "Enumerated", ["#JADN-Type"]],
      [3, "type_options", "TypeOptions", ["[0", "&2", "~1"]],
      [4, "type_description", "Description", ["[0"]],
      [5, "fields", "JADN-Type", ["[0", "&2"]]
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
      [4, "field_options", "TypeOptions", ["[0", "&3", "~1"]],
      [5, "field_description", "Description", ["[0"]]
    ]],
    ["FieldID", "Integer", ["y0"]],
    ["FieldOptions", "Map", [], "", [
      [91, "minOccurs", "Integer", ["y0", "[0", "=["]],
      [93, "maxOccurs", "Integer", ["y-2", "[0", "=]"]],
      [38, "tagId", "Integer", ["[0", "=&"]],
      [75, "key", "Boolean", ["[0", "=K"]],
      [76, "link", "Boolean", ["[0", "=L"]],
      [78, "not", "Boolean", ["[0", "=N"]]
    ]],
    ["AllOpts", "Map", [], "", [
      [48, "nillable", "Boolean", ["[0", "=K"]],
      [97, "abstract", "Boolean", ["[0", "=a"]],
      [101, "extends", "TypeRef", ["[0", "=e"]],
      [114, "restricts", "TypeRef", ["[0", "=r"]],
      [102, "final", "Boolean", ["[0", "=f"]]
    ]],
    ["BinaryOpts", "Map", [], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [123, "minLength", "Integer", ["[0", "={"]],
      [125, "maxLength", "Integer", ["[0", "=}"]],
      [117, "default", "Binary", ["[0", "=u"]],
      [118, "const", "Binary", ["[0", "=v"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["BooleanOpts", "Map", [], "", [
      [117, "default", "Boolean", ["[0", "=u"]],
      [118, "const", "Boolean", ["[0", "=K"]],
      [48, "nillable", "Boolean", ["[0", "=K"]],
      [65, "attr", "Boolean", ["[0", "=K"]]
    ]],
    ["IntegerOpts", "Map", [], "", [
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
    ["NumberOpts", "Map", [], "", [
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
    ["StringOpts", "Map", [], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [121, "minInclusive", "Number", ["[0", "=w"]],
      [122, "maxInclusive", "Number", ["[0", "=x"]],
      [119, "minExclusive", "Number", ["[0", "=y"]],
      [120, "maxExclusive", "Number", ["[0", "=z"]],
      [117, "default", "Number", ["[0", "=u"]],
      [118, "const", "Number", ["[0", "=v"]],
      [37, "pattern", "String", ["/regex", "[0", "=%"]],
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]],
      [48, "nillable", "Boolean", ["[0", "=undefined"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["EnumeratedOpts", "Map", ["eAllOpts"], "", [
      [61, "id", "Boolean", ["[0", "=="]],
      [35, "enum", "TypeRef", ["[0", "=#"]],
      [62, "pointer", "TypeRef", ["[0", "=>"]],
      [65, "attr", "Boolean", ["[0", "=undefined"]]
    ]],
    ["ChoiceOpts", "Map", ["eAllOpts"], "", [
      [61, "id", "Boolean", ["[0", "=="]],
      [67, "combine", "String", ["{1", "}1", "[0", "=C"]]
    ]],
    ["ArrayOpts", "Map", ["eAllOpts"], "", [
      [47, "format", "ArrayOf", ["*Format", "q", "[0", "=/"]],
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]]
    ]],
    ["ArrayOfOpts", "Map", ["eAllOpts"], "", [
      [42, "valueType", "TypeRef", ["=*"]],
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]],
      [113, "unique, ordered", "Boolean", ["[0", "=q"]],
      [115, "set", "Boolean", ["[0", "=s"]],
      [98, "unordered", "Boolean", ["[0", "=b"]]
    ]],
    ["MapOpts", "Map", ["eAllOpts"], "", [
      [61, "id", "Boolean", ["[0", "=="]],
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["MapOfOpts", "Map", ["eAllOpts"], "", [
      [43, "keyType", "TypeRef", ["=+"]],
      [42, "valueType", "TypeRef", ["=*"]],
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["RecordOpts", "Map", ["eAllOpts"], "", [
      [123, "minLength", "Integer", ["y0", "[0", "={"]],
      [125, "maxLength", "Integer", ["y0", "[0", "=}"]],
      [111, "sequence", "Boolean", ["[0", "=undefined"]]
    ]],
    ["Format", "String", ["%^/[a-zA-Z0-9]{1,16}+$"]],
    ["Description", "String"]
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


"""

def test_with_options():
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
            [2, "types", "Type", ["]-1"], "Types defined in this package"]
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
            [1, "type_name", "TypeName"],
            [2, "core_type", "Enumerated", ["#JADN-Type"]],
            [3, "type_options", "TypeOptions", ["[0", "&2"]],
            [4, "type_description", "Description", ["[0"]],
            [5, "fields", "JADN-Type", ["[0", "&2"]]
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
          ["FieldOptions", "Choice", [], "", [
            [1, "Binary", "BinaryFieldOpts"],
            [2, "Boolean", "BooleanFieldOpts"],
            [3, "Integer", "IntegerFieldOpts"],
            [4, "Number", "NumberFieldOpts"],
            [5, "String", "StringFieldOpts"],
            [6, "Enumerated", "EnumeratedFieldOpts"],
            [7, "Choice", "ChoiceFieldOpts"],
            [8, "Array", "ArrayFieldOpts"],
            [9, "ArrayOf", "ArrayOfFieldOpts"],
            [10, "Map", "MapFieldOpts"],
            [11, "MapOf", "MapOfFieldOpts"],
            [12, "Record", "RecordFieldOpts"]
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
            [4, "field_options", "FieldOptions", ["[0", "&3"]],
            [5, "field_description", "Description", ["[0"]]
          ]],
          ["FieldID", "Integer", ["y0"]],
          ["Format", "String", ["%^/[a-zA-Z0-9]{1,16}+$"]],
          ["Description", "String"],
          ["AllOpts", "Array", [], "", [
            [1, "nillable", "Boolean", ["[0"]],
            [2, "abstract", "Boolean", ["[0"]],
            [3, "extends", "TypeRef", ["[0"]],
            [4, "restricts", "TypeRef", ["[0"]],
            [5, "final", "Boolean", ["[0"]]
            ]],
          ["FieldOptions", "Array", ["eAllOpts"], "", [
            [1, "nillable", "Boolean", ["[0"]],
            [2, "abstract", "Boolean", ["[0"]],
            [3, "extends", "TypeRef", ["[0"]],
            [4, "restricts", "TypeRef", ["[0"]],
            [5, "final", "Boolean", ["[0"]],
            [6, "minOccurs", "Integer", ["y0", "[0"]],
            [7, "maxOccurs", "Integer", ["y-2", "[0"]],
            [8, "tagId", "Integer", ["[0"]],
            [9, "key", "Boolean", ["[0"]],
            [10, "link", "Boolean", ["[0"]],
            [11, "not", "Boolean", ["[0"]]
          ]],
          ["BinaryOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "nillable", "Boolean", ["[0"]],
            [3, "minLength", "Integer", ["[0"]],
            [4, "maxLength", "Integer", ["[0"]],
            [5, "default", "Binary", ["[0"]],
            [6, "const", "Binary", ["[0"]],
            [7, "attr", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]]
          ]],
          ["BinaryFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "nillable", "Boolean", ["[0"]],
            [3, "minLength", "Integer", ["[0"]],
            [4, "maxLength", "Integer", ["[0"]],
            [5, "default", "Binary", ["[0"]],
            [6, "const", "Binary", ["[0"]],
            [7, "attr", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]],
            [17, "minOccurs", "Integer", ["y0", "[0"]],
            [18, "maxOccurs", "Integer", ["y-2", "[0"]],
            [19, "tagId", "Integer", ["[0"]],
            [20, "key", "Boolean", ["[0"]],
            [21, "link", "Boolean", ["[0"]],
            [22, "not", "Boolean", ["[0"]]
          ]],
          ["BooleanOpts", "Array", ["eAllOpts"], "", [
            [1, "default", "Boolean", ["[0"]],
            [2, "const", "Boolean", ["[0"]],
            [3, "attr", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["BooleanFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "default", "Boolean", ["[0"]],
            [2, "const", "Boolean", ["[0"]],
            [3, "attr", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [91, "minOccurs", "Integer", ["y0", "[0"]],
            [93, "maxOccurs", "Integer", ["y-2", "[0"]],
            [38, "tagId", "Integer", ["[0"]],
            [75, "key", "Boolean", ["[0"]],
            [76, "link", "Boolean", ["[0"]],
            [78, "not", "Boolean", ["[0"]]
          ]],
          ["IntegerOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Integer", ["[0"]],
            [3, "maxInclusive", "Integer", ["[0"]],
            [4, "minExclusive", "Integer", ["[0"]],
            [5, "maxExclusive", "Integer", ["[0"]],
            [6, "default", "Integer", ["[0"]],
            [7, "const", "Integer", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]]
          ]],
          ["IntegerFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Integer", ["[0"]],
            [3, "maxInclusive", "Integer", ["[0"]],
            [4, "minExclusive", "Integer", ["[0"]],
            [5, "maxExclusive", "Integer", ["[0"]],
            [6, "default", "Integer", ["[0"]],
            [7, "const", "Integer", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]],
            [14, "minOccurs", "Integer", ["y0", "[0"]],
            [15, "maxOccurs", "Integer", ["y-2", "[0"]],
            [16, "tagId", "Integer", ["[0"]],
            [17, "key", "Boolean", ["[0"]],
            [18, "link", "Boolean", ["[0"]],
            [19, "not", "Boolean", ["[0"]]
          ]],
          ["NumberOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Number", ["[0"]],
            [3, "maxInclusive", "Number", ["[0"]],
            [4, "minExclusive", "Number", ["[0"]],
            [5, "maxExclusive", "Number", ["[0"]],
            [6, "default", "Number", ["[0"]],
            [7, "const", "Number", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]]
          ]],
          ["NumberFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "Number", ["[0"]],
            [3, "maxInclusive", "Number", ["[0"]],
            [4, "minExclusive", "Number", ["[0"]],
            [5, "maxExclusive", "Number", ["[0"]],
            [6, "default", "Number", ["[0"]],
            [7, "const", "Number", ["[0"]],
            [8, "attr", "Boolean", ["[0"]],
            [9, "nillable", "Boolean", ["[0"]],
            [10, "abstract", "Boolean", ["[0"]],
            [11, "extends", "TypeRef", ["[0"]],
            [12, "restricts", "TypeRef", ["[0"]],
            [13, "final", "Boolean", ["[0"]],
            [14, "minOccurs", "Integer", ["y0", "[0"]],
            [15, "maxOccurs", "Integer", ["y-2", "[0"]],
            [16, "tagId", "Integer", ["[0"]],
            [17, "key", "Boolean", ["[0"]],
            [18, "link", "Boolean", ["[0"]],
            [19, "not", "Boolean", ["[0"]]
          ]],
          ["StringOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "String", ["[0"]],
            [3, "maxInclusive", "String", ["[0"]],
            [4, "minExclusive", "String", ["[0"]],
            [5, "maxExclusive", "String", ["[0"]],
            [6, "pattern", "String", ["/regex", "[0"]],
            [7, "minLength", "Integer", ["y0", "[0"]],
            [8, "maxLength", "Integer", ["y0", "[0"]],
            [9, "default", "String", ["[0"]],
            [10, "const", "String", ["[0"]],
            [11, "attr", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]]
          ]],
          ["StringFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minInclusive", "String", ["[0"]],
            [3, "maxInclusive", "String", ["[0"]],
            [4, "minExclusive", "String", ["[0"]],
            [5, "maxExclusive", "String", ["[0"]],
            [6, "pattern", "String", ["/regex", "[0"]],
            [7, "minLength", "Integer", ["y0", "[0"]],
            [8, "maxLength", "Integer", ["y0", "[0"]],
            [9, "default", "String", ["[0"]],
            [10, "const", "String", ["[0"]],
            [11, "attr", "Boolean", ["[0"]],
            [12, "nillable", "Boolean", ["[0"]],
            [13, "abstract", "Boolean", ["[0"]],
            [14, "extends", "TypeRef", ["[0"]],
            [15, "restricts", "TypeRef", ["[0"]],
            [16, "final", "Boolean", ["[0"]],
            [17, "minOccurs", "Integer", ["y0", "[0"]],
            [18, "maxOccurs", "Integer", ["y-2", "[0"]],
            [19, "tagId", "Integer", ["[0"]],
            [20, "key", "Boolean", ["[0"]],
            [21, "link", "Boolean", ["[0"]],
            [22, "not", "Boolean", ["[0"]]
          ]],
          ["EnumeratedOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "enum", "TypeRef", ["[0"]],
            [3, "pointer", "TypeRef", ["[0"]],
            [4, "attr", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]]
          ]],
          ["EnumeratedFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "enum", "TypeRef", ["[0"]],
            [3, "pointer", "TypeRef", ["[0"]],
            [4, "attr", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]],
            [10, "minOccurs", "Integer", ["y0", "[0"]],
            [11, "maxOccurs", "Integer", ["y-2", "[0"]],
            [12, "tagId", "Integer", ["[0"]],
            [13, "key", "Boolean", ["[0"]],
            [14, "link", "Boolean", ["[0"]],
            [15, "not", "Boolean", ["[0"]]
          ]],
          ["ChoiceOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "combine", "String", ["{1", "}1", "[0"]],
            [3, "nillable", "Boolean", ["[0"]],
            [4, "abstract", "Boolean", ["[0"]],
            [5, "extends", "TypeRef", ["[0"]],
            [6, "restricts", "TypeRef", ["[0"]],
            [7, "final", "Boolean", ["[0"]]
          ]],
          ["ChoiceFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "combine", "String", ["{1", "}1", "[0"]],
            [3, "nillable", "Boolean", ["[0"]],
            [4, "abstract", "Boolean", ["[0"]],
            [5, "extends", "TypeRef", ["[0"]],
            [6, "restricts", "TypeRef", ["[0"]],
            [7, "final", "Boolean", ["[0"]],
            [8, "minOccurs", "Integer", ["y0", "[0"]],
            [9, "maxOccurs", "Integer", ["y-2", "[0"]],
            [10, "tagId", "Integer", ["[0"]],
            [11, "key", "Boolean", ["[0"]],
            [12, "link", "Boolean", ["[0"]],
            [13, "not", "Boolean", ["[0"]]
          ]],
          ["ArrayOpts", "Array", ["eAllOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["ArrayFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "format", "ArrayOf", ["*Format", "[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [9, "minOccurs", "Integer", ["y0", "[0"]],
            [10, "maxOccurs", "Integer", ["y-2", "[0"]],
            [11, "tagId", "Integer", ["[0"]],
            [12, "key", "Boolean", ["[0"]],
            [13, "link", "Boolean", ["[0"]],
            [14, "not", "Boolean", ["[0"]]
          ]],
          ["ArrayOfOpts", "Array", ["eAllOpts"], "", [
            [1, "vtype", "TypeRef"],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "unique", "Boolean", ["[0"]],
            [5, "set", "Boolean", ["[0"]],
            [6, "unordered", "Boolean", ["[0"]],
            [7, "nillable", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]]
          ]],
          ["ArrayOfFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "vtype", "TypeRef"],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "unique", "Boolean", ["[0"]],
            [5, "set", "Boolean", ["[0"]],
            [6, "unordered", "Boolean", ["[0"]],
            [7, "nillable", "Boolean", ["[0"]],
            [8, "abstract", "Boolean", ["[0"]],
            [9, "extends", "TypeRef", ["[0"]],
            [10, "restricts", "TypeRef", ["[0"]],
            [11, "final", "Boolean", ["[0"]],
            [12, "minOccurs", "Integer", ["y0", "[0"]],
            [13, "maxOccurs", "Integer", ["y-2", "[0"]],
            [14, "tagId", "Integer", ["[0"]],
            [15, "key", "Boolean", ["[0"]],
            [16, "link", "Boolean", ["[0"]],
            [17, "not", "Boolean", ["[0"]]
          ]],
          ["MapOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "sequence", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]]
          ]],
          ["MapFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "id", "Boolean", ["[0"]],
            [2, "minLength", "Integer", ["y0", "[0"]],
            [3, "maxLength", "Integer", ["y0", "[0"]],
            [4, "sequence", "Boolean", ["[0"]],
            [5, "nillable", "Boolean", ["[0"]],
            [6, "abstract", "Boolean", ["[0"]],
            [7, "extends", "TypeRef", ["[0"]],
            [8, "restricts", "TypeRef", ["[0"]],
            [9, "final", "Boolean", ["[0"]],
            [10, "minOccurs", "Integer", ["y0", "[0"]],
            [11, "maxOccurs", "Integer", ["y-2", "[0"]],
            [12, "tagId", "Integer", ["[0"]],
            [13, "key", "Boolean", ["[0"]],
            [14, "link", "Boolean", ["[0"]],
            [15, "not", "Boolean", ["[0"]]
          ]],
          ["MapOfOpts", "Array", ["eAllOpts"], "", [
            [1, "ktype", "TypeRef"],
            [2, "vtype", "TypeRef"],
            [3, "minLength", "Integer", ["y0", "[0"]],
            [4, "maxLength", "Integer", ["y0", "[0"]],
            [5, "sequence", "Boolean", ["[0"]],
            [6, "nillable", "Boolean", ["[0"]],
            [7, "abstract", "Boolean", ["[0"]],
            [8, "extends", "TypeRef", ["[0"]],
            [9, "restricts", "TypeRef", ["[0"]],
            [10, "final", "Boolean", ["[0"]]
          ]],
          ["MapOfFieldOpts", "Array", ["eAllOpts"], "", [
            [1, "ktype", "TypeRef"],
            [2, "vtype", "TypeRef"],
            [3, "minLength", "Integer", ["y0", "[0"]],
            [4, "maxLength", "Integer", ["y0", "[0"]],
            [5, "sequence", "Boolean", ["[0"]],
            [6, "nillable", "Boolean", ["[0"]],
            [7, "abstract", "Boolean", ["[0"]],
            [8, "extends", "TypeRef", ["[0"]],
            [9, "restricts", "TypeRef", ["[0"]],
            [10, "final", "Boolean", ["[0"]],
            [11, "minOccurs", "Integer", ["y0", "[0"]],
            [12, "maxOccurs", "Integer", ["y-2", "[0"]],
            [13, "tagId", "Integer", ["[0"]],
            [14, "key", "Boolean", ["[0"]],
            [15, "link", "Boolean", ["[0"]],
            [16, "not", "Boolean", ["[0"]]
          ]],
          ["RecordOpts", "Array", ["eAllOpts"], "", [
            [1, "minLength", "Integer", ["y0", "[0"]],
            [2, "maxLength", "Integer", ["y0", "[0"]],
            [3, "sequence", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]]
          ]],
          ["RecordFieldOpts", "Array", ["eFieldOpts"], "", [
            [1, "minLength", "Integer", ["y0", "[0"]],
            [2, "maxLength", "Integer", ["y0", "[0"]],
            [3, "sequence", "Boolean", ["[0"]],
            [4, "nillable", "Boolean", ["[0"]],
            [5, "abstract", "Boolean", ["[0"]],
            [6, "extends", "TypeRef", ["[0"]],
            [7, "restricts", "TypeRef", ["[0"]],
            [8, "final", "Boolean", ["[0"]],
            [9, "minOccurs", "Integer", ["y0", "[0"]],
            [10, "maxOccurs", "Integer", ["y-2", "[0"]],
            [11, "tagId", "Integer", ["[0"]],
            [12, "key", "Boolean", ["[0"]],
            [13, "link", "Boolean", ["[0"]],
            [14, "not", "Boolean", ["[0"]]
          ]]
        ]
      }
    


    valid_data_list = [            
            
            ["Schema", "Record", [], "", [
                [1, "meta", "String", [], ""],
                [2, "types", "String", ["[1", "]-1"], ""]]]
        ]}
      
    valid_data_list = [
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "String", ["[0"], "", []]]        
        }, 
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Binary", [], ""]]        
        },               
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Integer", ["[0"], "", []]]        
        },          
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Number", ["[0"], "", []]]        
        },    
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Enumerated", [], "", [
                [1, "thing", ""],
                [2, "two", ""]]

            ]]        
        }, 
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Array", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Record", [], "", [
                [1, "thing", "String", [], ""]]
            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "Map", [], "", [
                [1, "thing", "String", [], ""]]

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "ArrayOf", ["*String"], ""

            ]]        
        },      
        {
            "info" : {"package" : "http://example.fake"},
            "types" : [["Typename", "MapOf", ["+Integer", "*String"], ""

            ]]        
        },

        {
  "info": {
    "title": "Music Library",
    "package": "http://fake-audio.org/music-lib",
    "version": "1.1",
    "description": "This information model defines a library of audio tracks, organized by album, with associated metadata regarding each track. It is modeled on the types of library data maintained by common websites and music file tag editors.",
    "license": "CC0-1.0",
    "exports": ["Library"]
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
            "meta" : "package",
            "types" : ["Typename2"]       
        }]
    
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0
    



"""
