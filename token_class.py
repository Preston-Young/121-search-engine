class Index:
    def __init__(self):
        self.index = {}

    def add_token(self, token: str):
        self.index[token] = {
            "token_frequency": frequency (int),
            "document_frequency": frequency (int),
            "tf_idf_score": score (int),
            "doc_ids": [
                {
                    "id": page id (string?),
                    "weight": weight (int)
                },
                {
                    "id": page id (string?),
                    "weight": weight (int)
                }
            ]
        }