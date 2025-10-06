from jadnvalidation.tests.test_utils import validate_valid_data, validate_invalid_data
from jadnvalidation.utils.consts import XML

LIBRARY_SCHEMA = {
    "meta": {
        "title": "Music Library",
        "package": "http://fake-audio.org/music-lib",
        "version": "1.1",
        "description": "This information model defines a library of audio tracks, organized by album, with metadata regarding each track.",
        "license": "CC0-1.0",
        "roots": ["Library"],
    },
    "types": [
        [
            "Library",
            "MapOf",
            ["+Barcode", "*Album", "{1"],
            "Top level of the library is a map of CDs by barcode",
            [],
        ],
        ["Barcode", "String", ["%^\\d{12}$"], "A UPC-A barcode is 12 digits", []],
        [
            "Album",
            "Record",
            [],
            "model for the album",
            [
                [1, "album_artist", "Artist", [], "primary artist associated with this album"],
                [2, "album_title", "String", [], "publisher's title for this album"],
                [3, "pub_data", "Publication-Data", [], "metadata about the album's publication"],
                [4, "tracks", "Track", ["]0"], "individual track descriptions and content"],
                [5, "total_tracks", "Integer", ["w1"], "total track count"],
                [6, "cover_art", "Image", ["[0"], "cover art image for this album"],
            ],
        ],
        [
            "Publication-Data",
            "Record",
            [],
            "who and when of publication",
            [
                [1, "publisher", "String", [], "record label that released this album"],
                [2, "release_date", "String", ["/date"], "and when did they let this drop"],
            ],
        ],
        [
            "Image",
            "Record",
            [],
            "pretty picture for the album or track",
            [
                [1, "image_format", "Image-Format", [], "what type of image file?"],
                [2, "image_content", "Binary", [], "the image data in the identified format"],
            ],
        ],
        [
            "Image-Format",
            "Enumerated",
            [],
            "can only be one, but can extend list",
            [[1, "PNG", ""], [2, "JPG", ""], [3, "GIF", ""]],
        ],
        [
            "Artist",
            "Record",
            [],
            "interesting information about a performer",
            [
                [1, "artist_name", "String", [], "who is this person"],
                [2, "instruments", "Instrument", ["q", "]0"], "and what do they play"],
            ],
        ],
        [
            "Instrument",
            "Enumerated",
            [],
            "collection of instruments (non-exhaustive)",
            [
                [1, "vocals", ""],
                [2, "guitar", ""],
                [3, "bass", ""],
                [4, "drums", ""],
                [5, "keyboards", ""],
                [6, "percussion", ""],
                [7, "brass", ""],
                [8, "woodwinds", ""],
                [9, "harmonica", ""],
            ],
        ],
        [
            "Track",
            "Record",
            [],
            "for each track there's a file with the audio and a metadata record",
            [
                [1, "location", "File-Path", [], "path to the audio file location in local storage"],
                [2, "metadata", "Track-Info", [], "description of the track"],
            ],
        ],
        [
            "Track-Info",
            "Record",
            [],
            "information about the individual audio tracks",
            [
                [1, "track_number", "Integer", ["w1"], "track sequence number"],
                [2, "title", "String", [], "track title"],
                [3, "length", "Integer", ["w1"], "length of track in seconds"],
                [4, "audio_format", "Audio-Format", [], "format of the digital audio"],
                [5, "featured_artist", "Artist", ["q", "[0", "]0"], "notable guest performers"],
                [6, "track_art", "Image", ["[0"], "optional individual artwork"],
                [7, "genre", "Genre", [], ""],
            ],
        ],
        [
            "Audio-Format",
            "Enumerated",
            [],
            "can only be one, but can extend list",
            [[1, "MP3", ""], [2, "OGG", ""], [3, "FLAC", ""], [4, "MP4", ""], [5, "AAC", ""], [6, "WMA", ""], [7, "WAV", ""]],
        ],
        [
            "Genre",
            "Enumerated",
            [],
            "Enumeration of common genres",
            [
                [1, "rock", ""],
                [2, "jazz", ""],
                [3, "hip_hop", ""],
                [4, "electronic", ""],
                [5, "folk_country_world", ""],
                [6, "classical", ""],
                [7, "spoken_word", ""],
            ],
        ],
        ["File-Path", "String", [], "local storage location of file with directory path from root, filename, and extension"],
    ],
}

VALID_LIBRARY_XML = """<Library type="dict">
    <n187848720125 type="dict">
        <tracks type="dict">
            <metadata type="dict">
                <featured_artist type="dict">
                    <artist_name type="str">abcdefg</artist_name>
                    <instruments type="str">vocals</instruments>
                </featured_artist>
                <track_number type="int">1</track_number>
                <title type="str">abcdefg</title>
                <length type="int">1</length>
                <audio_format type="str">MP3</audio_format>
                <track_art type="dict">
                    <image_format type="str">PNG</image_format>
                    <image_content type="str">efg</image_content>
                </track_art>
                <genre type="str">rock</genre>
            </metadata>
            <location type="str">abcdefg</location>
        </tracks>
        <album_artist type="dict">
            <artist_name type="str">abcdefg</artist_name>
            <instruments type="str">vocals</instruments>
        </album_artist>
        <album_title type="str">abcdefg</album_title>
        <pub_data type="dict">
            <publisher type="str">abcdefg</publisher>
            <release_date type="str">2023-01-01</release_date>
        </pub_data>
        <total_tracks type="int">1</total_tracks>
        <cover_art type="dict">
            <image_format type="str">PNG</image_format>
            <image_content type="str">efg</image_content>
        </cover_art>
    </n187848720125>
</Library>"""

INVALID_LIBRARY_XML = """<Library type="dict">
    <n1878487201256 type="dict">
        <tracks type="dict">
            <metadata type="dict">
                <featured_artist type="dict">
                    <artist_name type="str">abcdefg</artist_name>
                    <instruments type="str">vocals</instruments>
                </featured_artist>
                <track_number type="int">1</track_number>
                <title type="str">abcdefg</title>
                <length type="int">1</length>
                <audio_format type="str">MP3</audio_format>
                <track_art type="dict">
                    <image_format type="str">PNG</image_format>
                    <image_content type="str">efg</image_content>
                </track_art>
                <genre type="str">rock</genre>
            </metadata>
            <location type="str">abcdefg</location>
        </tracks>
        <album_artist type="dict">
            <artist_name type="str">abcdefg</artist_name>
            <instruments type="str">vocals</instruments>
        </album_artist>
        <album_title type="str">abcdefg</album_title>
        <pub_data type="dict">
            <publisher type="str">abcdefg</publisher>
            <release_date type="str">2023-01-01</release_date>
        </pub_data>
        <total_tracks type="int">1</total_tracks>
        <cover_art type="dict">
            <image_format type="str">PNG</image_format>
            <image_content type="str">efg</image_content>
        </cover_art>
    </n1878487201256>
</Library>"""

def test_attr():
    root = "Root-Test"   
  
    j_schema = {
        "meta": {
            "title": "JADN Schema Start Up Template",
            "package": "http://JADN-Schema-Start-Up-Template-URI",
            "roots": ["Schema"]
        },
        "types": [
            ["Root-Test", "Record", [], "", [
                [1, "field_value_1", "String", ["/attr"], ""],
                [2, "field_value_2", "String", [], ""]
            ]]
        ]
    }

    valid_data_list = [
            {
                "field_value_1": "abcdefg",
                "field_value_2": "abcdefg"
            },
        ]
        
    err_count = validate_valid_data(j_schema, root, valid_data_list)    
    assert err_count == 0

def test_xml_pattern_digit():
    root = "Library"
    err_count = validate_valid_data(LIBRARY_SCHEMA, root, [VALID_LIBRARY_XML], XML)
    assert err_count == 0
    err_count = validate_invalid_data(LIBRARY_SCHEMA, root, [INVALID_LIBRARY_XML], XML)
    assert err_count == 1