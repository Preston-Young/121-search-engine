import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson
from time import time
import json

loaded_index = None
url_id_map = None
INDEX_FILEPATH = b'index_storage/partial1.json'
URL_MAP_FILEPATH = b'index_storage/url_id_map.json'

# TODO: Remove this function if we don't need it due to the new way we're indexing
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

# def get_term_dict(key):
#     # if not loaded_index:
#     #     print("Index isn't loaded")
#     #     return

    # print('top of get term dict')
    # start = time()

#     # Load respective letter index json i.e. a.json, b.json, etc.
#     index_file = f"index/{key[0]}.json"
#     loaded_index = simdjson.load(index_file)

#     # Convert string to binary string
#     json_term = f'/{key}'.encode()

#     try:
#         binary_dict = loaded_index.at_pointer(json_term)

#     except:
#         binary_dict = None


#     print(f'Get term dict: {round((time() - start) * 1000, 3)} ms')

#     return binary_dict

def get_term_dict(term):
    # TODO: Handle case with term not in index

    print('top of get term dict')
    start = time()

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

    print(f'Get term dict: {round((time() - start) * 1000, 3)} ms')
            
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