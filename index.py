# {
#   "token": {
#       "token_frequency": frequency (int),
#       "document_frequency": frequency (int),
#       "doc_ids": {
#           "page_id1": {
#               "id": page id (string?),
#               "token_frequency": frequency (int),
#               "weight": weight (int),
#               "tf_idf_score": score (int),
#           },
#           "page_id2": {
#               "id": page id (string?),
#               "token_frequency": frequency (int),
#               "weight": weight (int),
#               "tf_idf_score": score (int),
#           }
#       }
#   }
# }

import os, re, sys, json
from time import time
import libpy_simdjson as simdjson # https://github.com/gerrymanoim/libpy_simdjson
from bs4 import BeautifulSoup
from collections import defaultdict
from math import log 
from nltk.stem import PorterStemmer

from stopwords import STOPWORDS_SET 

DATA_FOLDER = 'DEV'
INDEX_DUMP_PATH = 'dump.json'
DOCUMENT_COUNT = 55393

def tree(): return defaultdict(tree)
index = tree()

doc_count = 0
cur_doc_id = 0
unique_tokens = defaultdict(int)
url_id_map = {}
stemmer = PorterStemmer()

MAX_INDEX_SIZE = 5000000 #5mb
partial_count = 1

HTML_WEIGHTS = {
    'title': 30,
    'h1': 10,
    'h2': 9,
    'h3': 8,
    'h4': 7,
    'b': 3,
    'strong': 3,
    'i': 2,
    'em': 2,
    'h5': 2,
    'h6': 2
}

'''
Load URL ID Map
'''
def load_url_id_map():
    global cur_doc_id
    global doc_count

    for subdir, _, files in os.walk(DATA_FOLDER): 
        for file in files:
            if file.lower().endswith(('.json')):
                data = simdjson.load(os.path.join(subdir, file))
                data_url = data.at_pointer(b'/url').decode()
                data_content = data.at_pointer(b'/content').decode()
                
                url_id_map[cur_doc_id] = data_url

                print(f'{os.path.join(subdir, file)} - {data_url}')

                cur_doc_id += 1
                doc_count += 1

    with open("index_storage/url_id_map.json", "w") as output_file:
        json.dump(url_id_map, output_file, indent = 2)

'''
Parse given json data
'''
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

                # Calculate weights here
                assign_importance(soup, cur_doc_id)

                #check if index needs to be cleared and stored in disk    
                # if(sys.getsizeof(index) > MAX_INDEX_SIZE):
                #     write_partial_index()

                cur_doc_id += 1
                doc_count += 1

        #     if doc_count == 50:
        #         break

        # if doc_count == 50:
        #     break

    # Calculate tf idf for every document tied to each token 
    for token in index:
        for doc_id in index[token]["doc_ids"]:
            # Set score
            idf = log( DOCUMENT_COUNT / (1 + index[token]["document_frequency"]), 10)
            tf = index[token]["doc_ids"][doc_id]["token_frequency"]
            index[token]["doc_ids"][doc_id]["tf_idf_score"] = tf * idf

    #write remaining index to disk
    #write_partial_index()

    #write url_id_map to json file
    with open("index_storage/url_id_map.json", "w") as output_file:
        json.dump(url_id_map, output_file, indent = 2)

'''
Tokenize given html page
'''
def tokenize(soup):
    cur_doc_map = defaultdict(int)

    # get tokens
    for token in re.split("[^a-zA-Z']+", soup.get_text().lower()):
        token = token.strip(" '")
        token = stemmer.stem(token)
        # check for empty token, ascii, and stopwords
        if valid_token(token):
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
        index[token]["doc_ids"][doc_id] = {"id": doc_id, "token_frequency": freq/sum(cur_doc_tokens.values()), "weight": 0, "tf_idf_score": 0}
        # TODO (done): normalize token_frequency

        # idf of a given term, is constant for a given term

        # idf = log( DOCUMENT_COUNT / (1 + index[token]["document_frequency"]), 10)
        # tf = index[token]["doc_ids"][doc_id]["token_frequency"]
        # index[token]["doc_ids"][doc_id]["tf_idf_score"] = tf * idf
        # tf-idf = tf * idf
        

'''
Determine the importance of a given input list
'''
def assign_importance(soup, doc_id):
     stemmer = PorterStemmer()
     
     # TODO: check if find_all without parameters gives all tags
     for tag in soup.find_all():
        tag_text = re.split("[^a-zA-Z']+", tag.get_text().lower())

        # TODO: Tokenize this?
        for word in tag_text:
            word = stemmer.stem(word.strip(" '"))
            if word in index:
                
                if doc_id in index[word]["doc_ids"]:
                    index[word]["doc_ids"][doc_id]["weight"] += HTML_WEIGHTS.get(tag.name, 1)

'''
writes current index to file and clears it if size exceeds 5mb
'''
def write_partial_index():
    global index
    global partial_count

    file_name = "index_storage/partial" + str(partial_count) + ".json"

    with open(file_name, "w") as output_file:
        #sort index
        sorted_index = {token: token_info for token, token_info in sorted(index.items(), key = lambda item: item[0])}
        json.dump(sorted_index, output_file, indent = 2)

    # TODO: clear
    # index.clear()
    partial_count += 1

'''
Determine if a token is valid
'''
def valid_token(token):
    return token != '' and len(token) == len(token.encode()) and token not in STOPWORDS_SET and len(token) > 2

'''
create report from data
'''
def create_report():
    with open("report.txt", "w") as output:
        output.write(f"Number of documents: {doc_count}\n")

        output.write(f"Number of unique tokens: {len(unique_tokens)}\n")

        size_in_kb = sys.getsizeof(index) / 1000
        output.write(f"Size of index on disk: {size_in_kb}KB\n")

'''
main function
'''
def main():
    start = time()  # start timer

    parse_json(DATA_FOLDER)

    end = time()    # end timer
    index_time = round(end-start, 2)
    print(f'Indexing time: {index_time}s')

    create_report()
    with open(INDEX_DUMP_PATH, 'w') as f:
        f.write(json.dumps(index, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()