import os

import json
import libpy_simdjson # https://github.com/gerrymanoim/libpy_simdjson

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

if __name__ == '__main__':
    json_time = timereps(REP_TIME, lambda: json_test(DATA_PATH))
    print('=======')
    libpy_simdjson_time = timereps(REP_TIME, lambda: simdjson_test(DATA_PATH))
    print('=======')

    print (f'json_time: {json_time}')
    print (f'libpy_simdjson_time: {libpy_simdjson_time}')

    # Average time to count all characters in 7909 files (grape_ics_uci_edu)
    # Built in JSON parser: 0.7625176501274109
    # libpy_simdjson parser: 0.2980461001396179 
    # ~60% faster