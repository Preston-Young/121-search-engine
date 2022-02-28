import cython

def intersection_helper(stemmer, list query_terms):
    if len(query_terms) < 2: return
    for term in query_terms:
        print(term)
