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
    data = read_json_file(file_path)
    program = visitor.objectify(data["ast"])
    if_nodes = []
    line_list = []
    test_list = []
    token_list = []
    token_label = []
    token_line_num = []

    type_list_pos = []
    type_list_neg = []

    for node in program.traverse():
        if node.type == "IfStatement":
            x_pos, x_neg = check_type_get_token(node.test)
            
            if x_pos != None:
                token_list.append(x_pos)
                token_label.append(0)
                line_list.append(node.loc['start']['line'])
                type_list_pos.append(node.test.type)
            if x_neg != None:
                token_list.append(x_neg)
                token_label.append(1)
                line_list.append(node.loc['start']['line'])
                type_list_neg.append(node.test.type)


    assert len(token_list) == len(line_list) == len(token_label) 

    return token_list, token_label, line_list, type_list_pos,type_list_neg
    #return token_list, token_label, line_list
