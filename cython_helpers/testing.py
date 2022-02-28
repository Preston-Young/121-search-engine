from time import time
from nltk.stem import PorterStemmer

from intersection import intersection_helper

if __name__ == '__main__':
    query_terms = ['machine', 'learning']

    stemmer = PorterStemmer()

    start = time()  # start timer

    intersection_helper(stemmer, query_terms)

    end = time()    # end timer
    run_time = round((end - start) * 1000, 4)
    print(f'\nRuntime: {run_time}ms')