import re
#import mmap
from index import main, index, url_id_map
#import stopwards.py
from collections import defaultdict
from nltk.stem import PorterStemmer


def handle_query(query: str) -> None:
    query_terms = re.sub("[^0-9a-zA-Z']+", "", query)
    query_terms = query_terms.split()
    
    # Assuming that stopwards are not yet filtered:
    # with open('stopwards.py') as file:
    #     search = mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ)
    #     for word in query_terms:
    #         if re.search(br'(?i){word}', search):
    #             query_terms.replace(word, '') 

    # TODO: Change this intersection logic to work for 1 and >2

    print(f'split query: {query_terms}')

    stemmer = PorterStemmer()

    term1 = query_terms[0]
    term1 = stemmer.stem(term1)
    
    print(f'after stemming: {term1}')
    print(f'term info: {dict(index[term1])}')

    common_doc_ids = list(index[term1]["doc_ids"].keys())
    
    print(f'common doc ids: {common_doc_ids}')
    
    # Loop starts here for intersection
    for term2 in query_terms[1:]:
        term2 = stemmer.stem(term2)
        term2_doc_ids = list(index[term2]["doc_ids"].keys())
        
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

    # Build doc_id:score dict
    # {doc_id: score}
    # {1: 10, 4: 50}
    scores = defaultdict(int)
    for term in query_terms:
        for doc_id in common_doc_ids:
            # TODO: Change method for calculating score
            score = index[term]["doc_ids"][doc_id]["tf_idf_score"] * index[term]["doc_ids"][doc_id]["weight"]
            scores[doc_id] += score

    get_top_results(scores, 5)

'''
Search through common doc_ids, sort by tf-idf and weight, and return top N results
'''
def get_top_results(scores, N):
    urls = []

    counter = 1
    for doc_id in sorted(scores.keys(), key = lambda k: scores[k], reverse = True):
        urls.append(url_id_map[doc_id])

        if counter == N:
            break

        counter += 1

    print(urls)
    return urls

if __name__ == "__main__":
    main()
    query = input("What would you like to search for?\n")
    handle_query(query)