import json

# Saves dictionary term_dict into filename, with 1 term per line
# Also builds index of index, with mappings for each term to a specific character
# that can be seeked to later
# "index/a.json"
# "index_of_index/a.json"
def save_sub_index(term_dict):
    # TODO: Change this later to fit letter.json
    filename = 'output.json'

    # Load index_of_index/filename
    with open(f"seek_reading_testing/index_of_index/{filename}") as index_of_index_file:
        index_of_index_dict = json.load(index_of_index_file)

    # Writing into index file for terms
    with open(f'seek_reading_testing/index/{filename}', 'w') as output_file:
        # Grab keys
        keys = list(term_dict.keys())
        
        # Write opening curly brace for valid JSON
        output_file.write('{\n')

        # Write each term on its own line as valid JSON
        # Adds a comma to the end of every term except the last
        # Store position in index_of_index_dict
        for i in range(len(keys) - 1):
            index_of_index_dict[keys[i]] = output_file.tell()
            output_file.write(f'"{keys[i]}": {json.dumps(term_dict[keys[i]])},\n')
        
        # Handle last term in dict
        index_of_index_dict[keys[-1]] = output_file.tell()
        output_file.write(f'"{keys[-1]}": {json.dumps(term_dict[keys[-1]])}\n')
        
        # Write closing curly brace
        output_file.write('}')

    # Dumping index_of_index_dict into appropriate file
    with open(f"seek_reading_testing/index_of_index/{filename}", "w") as index_of_index_file:
        json.dump(index_of_index_dict, index_of_index_file)

def get_term_dict(term):
    # TODO: Change this later to fit letter.json
    filename = 'output.json'

    # Load index_of_index/filename
    with open(f"seek_reading_testing/index_of_index/{filename}") as index_of_index_file:
        index_of_index_dict = json.load(index_of_index_file)

        # Load index/filename and move file pointer directly to correct position
        with open(f"seek_reading_testing/index/{filename}") as index_file:
            index_file.seek(index_of_index_dict[term])
            # Wrap in curly braces and strip off newline, tailing comma
            json_string = '{' + index_file.readline().strip(',\n') + '}'
            term_dict = json.loads(json_string)
            
    return term_dict


if __name__ == '__main__':
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

    with open('index/a.json') as f:
        print(json.load(f))

    # save_sub_index(test_dict)
    # print(get_term_dict("term1"))