#cython: language_level=3

import cython
import array
from collections import defaultdict
import heapq

from term_loading import get_term_dict

def score_results(dict scores, int N):
    # cdef int k
    # sort = sorted(scores.items(), key=lambda x:x[1], reverse = True)
    # top = sort[0:N]
    
    top = heapq.nlargest(N, scores, key=scores.get)

    return top

# Disabling checks for performance
@cython.boundscheck(False)
@cython.wraparound(False)
def get_top_results(query_terms, list common_doc_ids, int N):
    cdef int score, i, j
    cdef int query_term_len = len(query_terms)
    cdef int doc_id_len = len(common_doc_ids)
    cdef bytes doc_id
    cdef str term
    cdef dict term_dict
    
    cdef dict scores = {}
    # cdef bytes[:] doc_ids = common_doc_ids

    for i in range(query_term_len):
        term_dict = get_term_dict(query_terms[i]).as_dict()
        for j in range(doc_id_len):
            doc_id = common_doc_ids[j]
            score = term_dict[b"doc_ids"][doc_id][b"tf_idf_score"] * term_dict[b"doc_ids"][doc_id][b"weight"]

            if doc_id in scores:
                scores[doc_id] += score
            else:
                scores[doc_id] = score

    return score_results(scores, N)