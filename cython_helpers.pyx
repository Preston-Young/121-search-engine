#cython: language_level=3

import cython
import array
from collections import defaultdict
import heapq

from term_loading import get_term_dict

def score_results(dict scores, int N):
    cdef list top = heapq.nlargest(N, scores, key=scores.get)
    return top

# Disabling checks for performance
@cython.boundscheck(False)
@cython.wraparound(False)
def get_top_results(list query_terms, list common_doc_ids, int N):
    cdef int score, i, j
    cdef int query_term_len = len(query_terms)
    cdef int doc_id_len = len(common_doc_ids)
    cdef str doc_id
    cdef str term
    cdef dict term_dict
    
    cdef dict scores = {}
    # cdef bytes[:] doc_ids = common_doc_ids

    for i in range(query_term_len):
        term_dict = get_term_dict(query_terms[i])
        for j in range(doc_id_len):
            doc_id = common_doc_ids[j]
            score = term_dict["doc_ids"][doc_id]["tf_idf_score"] * term_dict["doc_ids"][doc_id]["weight"]

            if doc_id in scores:
                scores[doc_id] += score
            else:
                scores[doc_id] = score

    return score_results(scores, N)