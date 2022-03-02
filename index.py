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

BREAK_POINT = 20 # Document number breakpoint for debugging

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
                update_token_frequency(cur_doc_id, cur_doc_tokens)

                # Calculate weights here
                assign_importance(soup, cur_doc_id)

                #check if index needs to be cleared and stored in disk    
                if(sys.getsizeof(index) > MAX_INDEX_SIZE):
                    write_partial_index()

                cur_doc_id += 1
                doc_count += 1

        #     if doc_count == BREAK_POINT:
        #         break

        # if doc_count == BREAK_POINT:
        #     break

    

    #write remaining index to disk
    write_partial_index()

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
def update_token_frequency(doc_id, cur_doc_tokens):
    # Update token frequency of overall and of given document
    for token, freq in cur_doc_tokens.items():
        index[token]["document_frequency"] += 1
        index[token]["token_frequency"] += freq
        index[token]["doc_ids"][doc_id] = {"id": doc_id, "token_frequency": freq/sum(cur_doc_tokens.values()), "weight": 0, "tf_idf_score": 0}
        # TODO (done): normalize token_frequency

    
'''
Calculates tf-idf for every document tied to each token
'''
def calculate_tf_idf(letter_index_file):
    with open(f"index/{letter_index_file}") as f:
        loaded_json = json.load(f)

    for token in loaded_json:
        for doc_id in loaded_json[token]["doc_ids"]:
            idf = log( DOCUMENT_COUNT / (1 + loaded_json[token]["document_frequency"]), 10)
            tf = loaded_json[token]["doc_ids"][doc_id]["token_frequency"]
            loaded_json[token]["doc_ids"][doc_id]["tf_idf_score"] = tf * idf

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
            if word in index and doc_id in index[word]["doc_ids"]:
                index[word]["doc_ids"][doc_id]["weight"] += HTML_WEIGHTS.get(tag.name, 1)

'''
Writes current index to file and clears it if size exceeds MAX_INDEX_SIZE
'''
def write_partial_index():
    global index
    global partial_count

    file_name = "index_storage/partial" + str(partial_count) + ".json"

    with open(file_name, "w+") as output_file:
        json.dump(index, output_file, indent = 2)

    # TODO (done): clear
    index.clear() # once it is dumped, we can clear the index to be reused 
    partial_count += 1

'''
Loads the current index and partial index from disk, merges them in memory, and writes back to disk
'''
def merge_partial_index(partial_idx):
    partial_idx_file = f"index_storage/{partial_idx}"
    with open(partial_idx_file) as f:
        partial_index_json = json.load(f)

    index_file = "index/a.json"
    with open(index_file) as f:
        loaded_json = json.load(f)

    # Looking at terms in alphabetical order minimizes the amount of times new file needs to be opened
    for term in sorted(partial_index_json.keys()):
        char_file = f"index/{term[0]}.json"

        # Check if we need a different file for letter of next term
        if char_file != index_file:

            # Dump json from memory into old index_file and close it
            with open(index_file, "w") as f:
                json.dump(loaded_json, f, indent = 2)

            index_file = char_file
            
            # Load file for current term into memory
            with open(char_file) as f:
                loaded_json = json.load(f) # a.txt, b.txt, etc

        # Grab token dictionary for partial and loaded_json
        partial_doc_id_dict = partial_index_json[term]["doc_ids"]

        if term not in loaded_json:
            loaded_doc_id_dict = {}
            loaded_json[term] = {"token_frequency": 0, "document_frequency": 0, "doc_ids": {}}
        else:
            loaded_doc_id_dict = loaded_json[term]["doc_ids"]

        # Merge loaded_json and current term dict in partial index
        loaded_json[term]["token_frequency"] += partial_index_json[term]["token_frequency"]
        loaded_json[term]["document_frequency"] += partial_index_json[term]["document_frequency"]
        loaded_json[term]["doc_ids"] = loaded_doc_id_dict.update(partial_doc_id_dict)

    # Dump the remaining json from memory into index_file and close it
    with open(index_file, "w") as f:
        json.dump(loaded_json, f, indent = 2)

# dict_1 = { 3: {...}, 4: {...} }
# dict_2 = { 1: {...}, 2: {...} }
# full_index = loaded_json = { "hi": { 1: {...}, 2: {...}, 3: {...}, 4: {...} } }

'''
Determine if a token is valid
'''
def valid_token(token):
    return token != '' and len(token) == len(token.encode()) and token not in STOPWORDS_SET and len(token) > 2

'''
Create report from data
'''
def create_report():
    with open("report.txt", "w") as output:
        output.write(f"Number of documents: {doc_count}\n")

        output.write(f"Number of unique tokens: {len(unique_tokens)}\n")

        size_in_kb = sys.getsizeof(index) / 1000
        output.write(f"Size of index on disk: {size_in_kb}KB\n")

'''
Main function
'''
def main():
    start = time()  # start timer

    # Initialize index character json files to empty
    for ascii in range(97, 123):
        with open(f"index/{chr(ascii)}.json", "w") as output:
            json.dump(dict(), output)

    # Parsing json and writing all partial indexes
    parse_json(DATA_FOLDER)

    # Merge all partial indexes
    for partial_idx in os.listdir("index_storage"):
        if partial_idx != "url_id_map.json":
            merge_partial_index(partial_idx)

    # Calculate tf-idf for all documents for each token
    for idx in os.listdir("index"):
        if idx != "url_id_map.json":
            calculate_tf_idf(idx)

    end = time()    # end timer
    index_time = round(end-start, 2)
    print(f'Indexing time: {index_time}s')

    # create_report()
    # with open(INDEX_DUMP_PATH, 'w') as f:
    #     f.write(json.dumps(index, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
