import json
import readline

def formatting_testing():
    output = 'output.json'

    test_dict = {
        "term1": {
            "token_frequency": 1,
            "document_frequency": 1,
            "doc_ids": {
                "1": {
                    "id": 1,
                    "token_frequency": 0.1,
                    "weight": 1,
                    "tf_idf_score": 0.1
                }
            }
        },
        "term2": {
            "token_frequency": 2,
            "document_frequency": 2,
            "doc_ids": {
                "2": {
                    "id": 2,
                    "token_frequency": 0.2,
                    "weight": 2,
                    "tf_idf_score": 0.2
                }
            }
        }
    }

    # Open file in append mode
    with open(output, 'a') as output_file:
        # Grab keys
        keys = list(test_dict.keys())
        
        # Write opening curly brace for valid JSON
        output_file.write('{\n')

        # Write each term on its own line as valid JSON
        # Adds a comma to the end of every term except the last
        for i in range(len(keys) - 1):
            output_file.write(f'"{keys[i]}": {json.dumps(test_dict[keys[i]])},\n')
        output_file.write(f'"{keys[-1]}": {json.dumps(test_dict[keys[-1]])}\n')
        
        # Write closing curly brace
        output_file.write('}')

# Saves dictionary term_dict into filename, with 1 term per line
# Also builds index of index, with mappings for each term to a specific character
# that can be seeked to later
# "index/a.json"
# "index_of_index/a.json"
def save_sub_index(term_dict, filename):
    # Load index_of_index/filename
    index_of_index_dict = dict()

    # Creating index file for terms
    with open(f'index/{filename}', 'a') as output_file:
        # Grab keys
        keys = list(term_dict.keys())
        
        # Write opening curly brace for valid JSON
        output_file.write('{\n')

        # Write each term on its own line as valid JSON
        # Adds a comma to the end of every term except the last
        for i in range(len(keys) - 1):
            index_of_index_dict[keys[i]] = output_file.tell()
            output_file.write(f'"{keys[i]}": {json.dumps(term_dict[keys[i]])},\n')
        
        # Handle last term in dict
        index_of_index_dict[keys[-1]] = output_file.tell()
        output_file.write(f'"{keys[-1]}": {json.dumps(term_dict[keys[-1]])}\n')
        
        # Write closing curly brace
        output_file.write('}')

    # Creating index file for terms
    print(f"Index of index dict: {index_of_index_dict}")
    with open(f"index_of_index/{filename}", "w") as index_of_index_file:
        json.dump(index_of_index_dict, index_of_index_file)

def load_sub_index(term_dict, filename):
    pass


if __name__ == '__main__':
    output_file = 'output.json'
    test_dict = {
        "term1": {
            "token_frequency": 1,
            "document_frequency": 1,
            "doc_ids": {
                "1": {
                    "id": 1,
                    "token_frequency": 0.1,
                    "weight": 1,
                    "tf_idf_score": 0.1
                }
            }
        },
        "term2": {
            "token_frequency": 2,
            "document_frequency": 2,
            "doc_ids": {
                "2": {
                    "id": 2,
                    "token_frequency": 0.2,
                    "weight": 2,
                    "tf_idf_score": 0.2
                }
            }
        }
    }

    # save_sub_index(test_dict, output_file)
    with open(f"index/output.json", "r") as file:
        file.seek(147)
        print(file.readline())