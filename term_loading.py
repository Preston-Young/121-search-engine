import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson
import json
from time import time
from nltk.stem import PorterStemmer

loaded_index = None
url_id_map = None
INDEX_FILEPATH = b'index_storage/partial1.json'
URL_MAP_FILEPATH = b'index_storage/url_id_map.json'

# Stores the JSON Binary index in loaded_index global
def load_index():
    global loaded_index
    
    print('Starting index load')
    
    start = time()  # start timer
    loaded_index = simdjson.load(INDEX_FILEPATH)
    end = time()    # end timer
    
    print(f'Index load done - {round((end - start) * 1000, 2)}ms')

def load_url_map():
    global url_id_map
    
    print('Starting url id map load')
    
    start = time()  # start timer
    url_id_map = simdjson.load(URL_MAP_FILEPATH)
    end = time()    # end timer
    
    print(f'url id map load done - {round((end - start) * 1000, 2)}ms')

def get_term_dict(key):
    if not loaded_index:
        print("Index isn't loaded")
        return

    # Convert string to binary string
    json_term = f'/{key}'.encode()

    print(f'json_term: {json_term}')

    binary_dict = loaded_index.at_pointer(json_term)

    return binary_dict

def get_url_mapping(key):
    
    if not url_id_map:
        print("url_id_map isn't loaded")
        return

    # Convert string to binary string
    json_term = f'/{key}'.encode()

    binary_dict = url_id_map.at_pointer(json_term).as_dict()

    return binary_dict

if __name__ == '__main__':
    stemmer = PorterStemmer()
    load_index()    # no params for right now, fp is global
    d = get_term_dict((stemmer.stem('machine')))
    print(str(d[b'doc_ids']))