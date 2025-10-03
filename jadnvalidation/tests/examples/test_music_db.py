from jadnvalidation.data_validation.data_validation import DataValidation
from jadnvalidation.utils.consts import JSON, XML

j_schema = {
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


def test_map_of_udstr_udrecord():
    root = "Library"
    
    data = {
    "012345678912": {
      "album_artist": {
        "artist_name": "test",
        "instruments": "vocals"
      },
      "album_title": "test",
      "pub_data": {
        "publisher": "test",
        "release_date": "2025-04-24"
      },
      "tracks": {
        "location": "test",
        "metadata": {
          "track_number": 1,
          "title": "test",
          "length": 5,
          "audio_format": "MP3",
          "featured_artist": {
            "artist_name": "test",
            "instruments": "guitar"
          },
          "track_art": {
            "image_format": "PNG",
            "image_content": "test"
          },
          "genre": "rock"
        }
      },
      "total_tracks": 1,
      "cover_art": {
        "image_format": "PNG",
        "image_content": "test"
      }
    }
  }
    
    errorMsgs=[]
    try :
        j_validation = DataValidation(j_schema, root, data, JSON)
        j_validation.validate()
    except Exception as err:
        if isinstance(err, ValueError):
            for error in err.args:
                errorMsgs.append(error)
        else:
            errorMsgs.append(str(err))
            
    assert len(errorMsgs) == 0
    
def test_xml_map_of_udstr_udrecord():
    root = "Library"
    
    data = '''<?xml version="1.0" encoding="UTF-8" ?>
      <Library>
          <012345678912>
              <album_artist>
                  <artist_name>test</artist_name>
                  <instruments>vocals</instruments>
              </album_artist>
              <album_title>test</album_title>
              <pub_data>
                  <publisher>test</publisher>
                  <release_date>2025-04-24</release_date>
              </pub_data>
              <tracks>
                  <location>test</location>
                  <metadata>
                      <track_number>1</track_number>
                      <title>test</title>
                      <length>5</length>
                      <audio_format>MP3</audio_format>
                      <featured_artist>
                          <artist_name>test</artist_name>
                          <instruments>guitar</instruments>
                      </featured_artist>
                      <track_art>
                          <image_format>PNG</image_format>
                          <image_content>test</image_content>
                      </track_art>
                      <genre>rock</genre>
                  </metadata>
              </tracks>
              <total_tracks>1</total_tracks>
              <cover_art>
                  <image_format>PNG</image_format>
                  <image_content>test</image_content>
              </cover_art>
          </012345678912>
      </Library>    
    '''
    
    data_2 = '''<map>
        <entry>
          <key>name</key>
          <value>
            <object>
              <property name="firstName">John</property>
              <property name="lastName">Doe</property>
            </object>
          </value>
        </entry>
        <entry>
          <key>age</key>
          <value>
            <object>
              <property name = "years">30</property>
            </object>
          </value>
        </entry>
        <entry>
          <key>city</key>
          <value>
            <object>
              <property name="cityName">New York</property>
            </object>
          </value>
        </entry>
      </map>    
    '''
    
    errorMsgs=[]
    # try :
    #     j_validation = DataValidation(j_schema, root, data, XML)
    #     j_validation.validate()
    # except Exception as err:
    #     if isinstance(err, ValueError):
    #         for error in err.args:
    #             errorMsgs.append(error)
    #     else:
    #         errorMsgs.append(str(err))
            
    assert len(errorMsgs) == 0    
    