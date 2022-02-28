import re
#import mmap
#from index import main, index, url_id_map, valid_token
from index import url_id_map, valid_token
from time import time
from collections import defaultdict
from nltk.stem import PorterStemmer

from stopwords import STOPWORDS_SET 
from term_loading import load_index, load_url_map, get_term_dict, get_url_mapping

from cython_helpers import get_top_results as c_top_results

TOP_RESULT_COUNT = 5
EXIT_COMMAND = '/end'

def handle_query(query: str) -> None:
    query_terms = re.sub("[^\s0-9a-zA-Z']+", "", query)
    query_terms = query_terms.split()

    # Filter out invalid tokens
    query_terms = list(filter(valid_token, query_terms))

    if len(query_terms) == 0:
        return []

    # print(f"Query Terms: {query_terms}")
    
    # Assuming that stopwards are not yet filtered:
    # with open('stopwards.py') as file:
    #     search = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    #     for word in query_terms:
    #         if re.search(br'(?i){word}', search):
    #             query_terms.replace(word, '') 

    # TODO: Change this intersection logic to work for 1 and >2

    stemmer = PorterStemmer()
    query_terms = list(map(lambda term: stemmer.stem(term), query_terms))

    term1 = query_terms[0]

    # return dict for term1 
    #common_doc_ids = list(sorted(index[term1]["doc_ids"].keys()))
    term1_dict = get_term_dict(term1)
    if not term1_dict: return []
    common_doc_ids = list(sorted(term1_dict[b'doc_ids'].keys()))

    # print(f'split query: {query_terms}')
    # print(f'after stemming: {term1}')
    # print(f'term info: {dict(index[term1])}')
    # print(f"Common doc ids: {common_doc_ids}")
    
    # Loop starts here for intersection
    start = time()
    
    for term2 in query_terms[1:]:
        #term2_doc_ids = list(sorted(index[term2]["doc_ids"].keys()))
        term2_dict = get_term_dict(term2)
        if not term2_dict: return []
        term2_doc_ids = list(sorted(term2_dict[b'doc_ids'].keys()))
        
        ptr1 = ptr2 = 0

        # print(f"Common doc ids: {common_doc_ids}")
        common_doc_ids_copy = common_doc_ids[:]
        common_doc_ids = []
        
        while ptr1 < len(common_doc_ids_copy) and ptr2 < len(term2_doc_ids):
            term1_doc_id = common_doc_ids_copy[ptr1]
            term2_doc_id = term2_doc_ids[ptr2]

            if term1_doc_id == term2_doc_id:
                common_doc_ids.append(term1_doc_id)
                ptr1 += 1
                ptr2 += 1

            elif term1_doc_id < term2_doc_id:
                ptr1 += 1

            else:
                ptr2 += 1
    
    end = time()    # end timer
    intersection_time = round((end - start) * 1000, 2)
    print(f'Common doc id count: {len(common_doc_ids)}')
    print(f'Common doc id calculation runtime: {intersection_time}ms')

    # Build doc_id:score dict
    # {doc_id: score}
    # {1: 10, 4: 50}
    start = time()
    
    top_urls = c_top_results(query_terms, common_doc_ids, 5)

    top_urls = list(map(lambda url: get_url_mapping(url.decode()), top_urls))

    end = time()    # end timer
    scoring_time = round((end - start) * 1000, 2)
    print(f'Calculate and return top urls runtime: {scoring_time}ms')

    return top_urls


'''
Search through common doc_ids, sort by tf-idf and weight, and return top N results
'''
def get_top_results(scores, N):
    urls = []

    counter = 1
    for doc_id in sorted(scores.keys(), key = lambda k: scores[k], reverse = True):
        url = get_url_mapping(doc_id.decode())
        urls.append(url)
        # urls.append(url_id_map[doc_id])

        if counter == N:
            break

        counter += 1

    return urls

if __name__ == "__main__":
    # Load index and url map from file
    load_index()
    load_url_map()

    # Get multiple queries in a loop
    while True:
        query = input("\nWhat would you like to search for: ")

        if query == EXIT_COMMAND:
            break

        start = time()  # start timer

        top_urls = handle_query(query)

        end = time()    # end timer
        search_time = round((end - start) * 1000, 2)
        print(f'Search time: {search_time}ms')

        if top_urls:
            #print urls
            print("\nTop 5 URLs:")
            for i, url in enumerate(top_urls, 1):
                print(f"{i}. {url}")
            
            print()
        else:
            print("No results found.")