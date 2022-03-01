from time import time
from nltk.stem import PorterStemmer

from term_loading import load_index
from cython_helpers import get_top_results, score_results

# Removed from git
from common import common_doc_ids

def dict_sorting_test():
    score_size = 55000
    score_keys = [str(x).encode() for x in range(score_size)]
    score_vals = [str(x).encode() for x in range(score_size)]
    scores = dict(zip(score_keys, score_vals))
    
    start = time()  # start timer

    res = score_results(scores, 5)
    
    end = time()    # end timer
    run_time = round((end - start) * 1000, 4)
    print(f'\nRuntime: {run_time}ms')
    print(res)


def top_results_test():
    query_terms = ['machine', 'learning']
    
    stemmer = PorterStemmer()
    query_terms = list(map(lambda term: stemmer.stem(term), query_terms))
    load_index()

    start = time()  # start timer

    get_top_results(query_terms, common_doc_ids, 5) # Python 472ms -> Cython 106ms

    end = time()    # end timer
    run_time = round((end - start) * 1000, 4)
    print(f'\nRuntime: {run_time}ms')

if __name__ == '__main__':
    # top_results_test()
    dict_sorting_test()