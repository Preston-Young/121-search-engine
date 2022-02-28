import cython
import array
from collections import defaultdict

from term_loading import get_term_dict

def score_results(dict scores, int N):
    cdef int k
    sort = sorted(scores.keys(), key = lambda k: scores[k], reverse = True)
    top = sort[0:N]

    return top

# common_doc_ids must be integer array, not byte string array
def get_top_results(query_terms, list common_doc_ids, int N):
    cdef int score
    cdef bytes doc_id
    cdef str term
    cdef dict term_dict
    
    cdef dict scores = {}
    # cdef bytes[:] doc_ids = common_doc_ids

    for term in query_terms:
        term_dict = get_term_dict(term).as_dict()
        for doc_id in common_doc_ids:
            score = term_dict[b"doc_ids"][doc_id][b"tf_idf_score"] * term_dict[b"doc_ids"][doc_id][b"weight"]

            if doc_id in scores:
                scores[doc_id] += score
            else:
                scores[doc_id] = score

    return score_results(scores, N)