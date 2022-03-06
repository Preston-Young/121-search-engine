import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson
from time import time
import json

loaded_index = None
url_id_map = None
INDEX_FILEPATH = b'index_storage/partial1.json'
URL_MAP_FILEPATH = b'index_storage/url_id_map.json'

def load_url_map():
    global url_id_map
    url_id_map = simdjson.load(URL_MAP_FILEPATH)

def get_term_dict(term):
    # TODO (done): Handle case with term not in index

    # TODO (done): Change this later to fit letter.json
    filename = f'{term[0]}.json'

    # Load index_of_index/filename
    index_of_index_dict = simdjson.load(f"index_of_index/{filename}")

    try:
        # Load index/filename and move file pointer directly to correct position
        with open(f"index/{filename}") as index_file:
            position = index_of_index_dict.at_pointer(f'/{term}'.encode())
            index_file.seek(position)
            # Wrap in curly braces and strip off newline, tailing comma
            json_string = '{' + index_file.readline().strip(',\n') + '}'
            term_dict = json.loads(json_string)

            return_dict = term_dict[term]
    except:
        return_dict = None
            
    return return_dict

def get_url_mapping(key):
    
    if not url_id_map:
        print("url_id_map isn't loaded")
        return

    # Convert string to binary string
    json_term = f'/{key}'.encode()

    # Decode binary URL into string
    url_string = url_id_map.at_pointer(json_term).decode()

    return url_string

if __name__ == '__main__':
    # Test get_term_dict
    # stemmer = PorterStemmer()
    # load_index()    # no params for right now, fp is global
    # d = get_term_dict((stemmer.stem('machine')))
    # print(str(d[b'doc_ids']))

    # Test get_url_mapping
    load_url_map()
    d = get_url_mapping(b'45903')
    print(d)