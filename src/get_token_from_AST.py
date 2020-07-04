from typing import List, Dict, Union, DefaultDict
import visitor
import codecs
import json
from TypeChecker import check_type_get_token
from collections import Counter

def read_json_file(json_file_path: str) -> List:
    """ Read a JSON file given path """
    try:
        obj_text = codecs.open(json_file_path, 'r',
                               encoding='utf-8').read()
        return json.loads(obj_text)
    except FileNotFoundError:
        print(
            "File {} not found. Please provide a correct file path Eg. ./results/hello.json".format(json_file_path))
        return []
    except Exception as e:
        print("invalid data file")
        # Most likely malformed JSON file
        return []



def get_token(file_path):
    data = read_json_file("10055_7513_a_dynamicContent.json")
    program = visitor.objectify(data["ast"])
    if_nodes = []
    line_list = []
    test_list = []
    token_list = []
    token_label = []
    token_line_num = []

    type_count = Counter()

    for node in program.traverse():
        if node.type == "IfStatement":
            type_count[node.test.type] += 1
            
            x_pos, x_neg = check_type_get_token(node.test)
            
            if x_pos != None:
                token_list.append(x_pos)
                token_label.append(0)
                line_list.append(node.loc['start']['line'])
                test_list.append(node.test.type)
            if x_neg != None:
                token_list.append(x_neg)
                token_label.append(1)
                line_list.append(node.loc['start']['line'])
                test_list.append(node.test.type)

    assert len(token_list) == len(line_list) == len(token_label) == len(test_list)
    return token_list, token_label, line_list, test_list
    
