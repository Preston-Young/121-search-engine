import re
#import numpy as np
from operator import itemgetter
from index import valid_token
from time import time
from collections import defaultdict
from nltk.stem import PorterStemmer

from stopwords import STOPWORDS_SET 
from term_loading import load_index, load_url_map, get_term_dict, get_url_mapping

from cython_helpers import get_top_results as c_top_results

TOP_RESULT_COUNT = 5
EXIT_COMMAND = '/end'

QUERY_ERR = {
    'urls': None,
    'search_time': -1
}

def handle_query(query: str) -> dict:
    print('top of handle query')
    start = time()
    query_terms = re.sub("[^\s0-9a-zA-Z']+", "", query)
    query_terms = query_terms.split()

    # Filter out invalid tokens
    query_terms = list(filter(valid_token, query_terms))

    if len(query_terms) == 0:
        return QUERY_ERR
    
    print('valid query terms')

    # TODO (done): Change this intersection logic to work for 1 and >2

    stemmer = PorterStemmer()
    query_terms = list(map(lambda term: stemmer.stem(term), query_terms))

    term1 = query_terms[0]

    term1_dict = get_term_dict(term1)
    if not term1_dict: return QUERY_ERR
    common_doc_ids = list(sorted(term1_dict[b'doc_ids'].keys()))
    #sorted = np.as_array(term1_dict[b'doc_ids'].keys())
    #common_doc_ids = np.sort(sorted, kind='timsort')

    print('term1 done')

    # print(f'split query: {query_terms}')
    # print(f'after stemming: {term1}')
    # print(f'term info: {dict(index[term1])}')
    # print(f"Common doc ids: {common_doc_ids}")
    
    for term2 in query_terms[1:]:
        term2_dict = get_term_dict(term2)
        if not term2_dict: return QUERY_ERR
        term2_doc_ids = list(sorted(term2_dict[b'doc_ids'].keys()))
        #sorted = np.as_array(term2_dict[b'doc_ids'].keys())
        #term2_doc_ids = np.sort(sorted, kind='timsort')

        ptr1 = ptr2 = 0

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
    
    print('other terms done')

    print(f'Finish handle query: {round((time() - start) * 1000, 3)} ms')

    # ~~~~~~~~~~~~~~~~Build score dictionary for common doc doc_ids~~~~~~~~~~~~~~~~~~
    # Format:
    #   {doc_id: score}
    #   {1: 10, 4: 50}

    print('fetching top urls')
    start_fetch = time()

    top_urls = c_top_results(query_terms, common_doc_ids, 5)
    top_urls = list(map(lambda url: get_url_mapping(url.decode()), top_urls))

    print(f'top urls fetched: {round((time() - start_fetch) * 1000, 3)} ms')

    search_time = round((time() - start) * 1000, 2)

    return {
        'urls': top_urls,
        'search_time': search_time,
    }

# TODO: Delete this function as we might not need it (converted to cython)
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

'''
Main function
'''
def main():
    # Load index and url map from file
    # TODO: Figure out if we still need this function since we're no longer preprocessing index
    # load_index()
    load_url_map()

    # Get multiple queries in a loop
    while True:
        query = input("\nWhat would you like to search for: ")

        if query == EXIT_COMMAND:
            break

        res = handle_query(query)
        top_urls, search_time = itemgetter('urls', 'search_time')(res)

        print(f'Search time: {search_time}ms')

        if top_urls:
            # print urls
            print("\nTop 5 URLs:")
            for i, url in enumerate(top_urls, 1):
                print(f"{i}. {url}")
            
            print()
        else:
            print("No results found.")

if __name__ == "__main__":
    main()