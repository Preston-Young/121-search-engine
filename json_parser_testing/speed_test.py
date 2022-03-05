import os
from time import time
import json
import libpy_simdjson # https://github.com/gerrymanoim/libpy_simdjson
import cysimdjson # https://github.com/TeskaLabs/cysimdjson

REP_TIME = 100
DATA_PATH = 'data/grape_ics_uci_edu'
# archive_ics_uci_edu - 1281 files
# grape_ics_uci_edu - 7909 files

def timereps(reps, func):
    from time import time
    start = time()
    for _ in range(0, reps):
        func()
    end = time()
    return (end - start) / reps

def json_test(folder):
    directory = os.fsencode(folder)
    total_len = 0
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        f = open(f'{folder}/{filename}')
        doc = json.load(f)
        content_length = len(doc['content'])
        total_len += content_length
    
    print(total_len)

def simdjson_test(folder):
    directory = os.fsencode(folder)
    total_len = 0
    
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        doc = libpy_simdjson.load(f'{folder}/{filename}')
        content_length = len(doc.at_pointer(b'/content').decode())
        total_len += content_length
    
    print(total_len)

def libpy_vs_cy_multi():
    folder = '/Users/prestonyoung/yauma/UCI/JuniorYear/WinterQuarter/CS121/Projects/Assignment3/121-search-engine/index'
    directory = os.fsencode(folder)

    start = time()  # start timer
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            doc = libpy_simdjson.load(f'{folder}/{filename}')

    end = time()    # end timer
    
    print(f'libpy_simdjson - {round((end - start) * 1000, 2)}ms')

    start = time()  # start timer

    parser = cysimdjson.JSONParser()
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith('.json'):
            with open(f'{folder}/{filename}', 'rb') as fo:
                doc = parser.parse(fo.read())

    end = time()    # end timer
    
    print(f'cysimdjson - {round((end - start) * 1000, 2)}ms')

def libpy_vs_cy_single():
    key = 'announc'
    file = '/Users/prestonyoung/yauma/UCI/JuniorYear/WinterQuarter/CS121/Projects/Assignment3/121-search-engine/index/a.json'
    
    # libpy_simdjson
    libpy_start = time()  # start timer
    json_term = f'/{key}'.encode()
    doc = libpy_simdjson.load(file)
    libpy_dict = doc.at_pointer(json_term)
    libpy_end = time()    # end timer
    print(libpy_dict['doc_ids'])
    
    # cysimdjson
    cy_start = time()  # start timer
    parser = cysimdjson.JSONParser()
    with open(file, 'rb') as fo:
        json_element = parser.parse(fo.read())
        cy_dict = json_element.at_pointer(f'/{key}')

    cy_end = time()    # end timer
    print(cy_dict)

    print(f'libpy_simdjson - {round((libpy_end - libpy_start) * 1000, 5)}ms')
    print(f'cy_simdjson - {round((cy_end - cy_start) * 1000, 5)}ms')

if __name__ == '__main__':
    # json_time = timereps(REP_TIME, lambda: json_test(DATA_PATH))
    # print('=======')
    # libpy_simdjson_time = timereps(REP_TIME, lambda: simdjson_test(DATA_PATH))
    # print('=======')

    # print (f'json_time: {json_time}')
    # print (f'libpy_simdjson_time: {libpy_simdjson_time}')

    # Average time to count all characters in 7909 files (grape_ics_uci_edu)
    # Built in JSON parser: 0.7625176501274109
    # libpy_simdjson parser: 0.2980461001396179 
    # ~60% faster

    # libpy_vs_cy_multi()
    libpy_vs_cy_single()