from time import time
from nltk.stem import PorterStemmer

from term_loading import load_index
from top_results_helper import get_top_results

# Removed from git
# from common import common_doc_ids

if __name__ == '__main__':
    query_terms = ['machine', 'learning']
    
    stemmer = PorterStemmer()
    query_terms = list(map(lambda term: stemmer.stem(term), query_terms))
    load_index()

    start = time()  # start timer

    get_top_results(query_terms, common_doc_ids, 5) # Python 472ms -> Cython 106ms

    end = time()    # end timer
    run_time = round((end - start) * 1000, 4)
    print(f'\nRuntime: {run_time}ms')