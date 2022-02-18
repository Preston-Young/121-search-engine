import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson

loaded_index = None
INDEX_FILEPATH = b'index_storage/partial1.json'

# Stores the JSON Binary index in loaded_index global
def load_index():
    file = simdjson.load(INDEX_FILEPATH)
    # file = file.at_pointer(file).decode()
    print(file.keys())
    return

if __name__ == '__main__':
    load_index(filepath)