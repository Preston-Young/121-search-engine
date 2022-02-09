# {
#   "token": {
#       "token_frequency": frequency (int),
#       "document_frequency": frequency (int),
#       "tf_idf_score": score (int),
#       "doc_ids": {
#           "page_id1": {
#               "id": page id (string?),
#               "token_frequency": frequency (int),
#               "weight": weight (int)
#           },
#           "page_id2": {
#               "id": page id (string?),
#               "token_frequency": frequency (int),
#               "weight": weight (int)
#           }
#       }
#   }
# }

import os, re, sys, json
from time import time
import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson
from bs4 import BeautifulSoup
from collections import defaultdict

from stopwords import STOPWORDS_SET 

DATA_FOLDER = 'DEV'
INDEX_DUMP_PATH = 'dump.json'

def tree(): return defaultdict(tree)
index = tree()

doc_count = 0
cur_doc_id = 0
unique_tokens = defaultdict(int)
url_id_map = {}

'''
Tokenize given html page
'''
def tokenize(soup):
    cur_doc_map = defaultdict(int)

    # get tokens
    for token in re.split("[^a-zA-Z']+", soup.get_text().lower()):
        token = token.strip()
        # check for empty token, ascii, and stopwords
        if token != '' and len(token) == len(token.encode()) and token not in STOPWORDS_SET and len(token) > 2:
            if token not in index:
                index[token] = {"token_frequency": 0, "document_frequency": 0, "doc_ids": {}}

            unique_tokens[token] += 1
            cur_doc_map[token] += 1

    return cur_doc_map

'''
Only calculates tf (for now)
'''
def update_tf_idf(doc_id, cur_doc_tokens):
    # Update token frequency of overall and of given document
    for token, freq in cur_doc_tokens.items():
        # index[token] = {
        #     'document_frequency': 0,
        #     'token_frequency': 0,
        #     'doc_ids': 0,
        # }
        index[token]["document_frequency"] += 1
        index[token]["token_frequency"] += freq
        index[token]["doc_ids"][doc_id] = {"id": doc_id, "token_frequency": freq, "weight": 0} 
        # TODO: calculate weight later

def parse_json(root_dir):
    global cur_doc_id
    global doc_count

    for subdir, _, files in os.walk(root_dir): 
        for file in files:
            if file.lower().endswith(('.json')):
                data = simdjson.load(os.path.join(subdir, file))
                data_url = data.at_pointer(b'/url').decode()
                data_content = data.at_pointer(b'/content').decode()
                
                url_id_map[cur_doc_id] = data_url
                
                print(f'{os.path.join(subdir, file)} - {data_url}')

                soup = BeautifulSoup(data_content, 'lxml')
                cur_doc_tokens = tokenize(soup)
                update_tf_idf(cur_doc_id, cur_doc_tokens)

                cur_doc_id += 1
                doc_count += 1

def create_report():
    with open("report.txt", "w") as output:
        output.write(f"Number of documents: {doc_count}\n")

        output.write(f"Number of unique tokens: {len(unique_tokens)}\n")

        size_in_kb = sys.getsizeof(index) / 1000
        output.write(f"Size of index on disk: {size_in_kb}KB\n")

if __name__ == '__main__':
    start = time()  # start timer
    
    parse_json(DATA_FOLDER)

    end = time()    # end timer

    print(f'Indexing time: {end-start} s')

    create_report()
    with open(INDEX_DUMP_PATH, 'w') as f:
        f.write(json.dumps(index, indent=4, sort_keys=True))
    