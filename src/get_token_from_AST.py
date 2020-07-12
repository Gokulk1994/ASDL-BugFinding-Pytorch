from typing import List, Dict, Union, DefaultDict
import visitor
import codecs
import json
from TypeChecker import check_type_get_token
from collections import Counter


class UnknownNodeTypeError(Exception):
    """Raised if we encounter a node with an unknown type."""
    pass


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
        print("invalid data file", json_file_path)
        # Most likely malformed JSON file
        return []

def get_token(file_path, Get_Negative = False):
    if_nodes = []
    line_list = []
    test_list = []
    token_list = []
    token_label = []
    token_line_num = []

    type_list_pos = []
    type_list_neg = []

    data = read_json_file(file_path)
    if data != []:
        try:
            program = visitor.objectify(data["ast"])
        except:
            #print("ERROR : ", file_path)
            return token_list, token_label, line_list, type_list_pos,type_list_neg
        try:
            for node in program.traverse():
                #print(node)
                if node.type == "IfStatement":
                    x_pos, x_neg = check_type_get_token(node.test, True)
                    if len(x_pos):
                        token_list.append(x_pos)
                        token_label.append(0)
                        line_list.append(node.loc['start']['line'])
                        type_list_pos.append(node.test.type)
                        
                    if Get_Negative == True and len(x_neg):                        
                        token_list.append(x_neg)
                        token_label.append(1)
                        line_list.append(node.loc['start']['line'])
                        type_list_neg.append(node.test.type)

            assert len(token_list) == len(line_list) == len(token_label)
            return token_list, token_label, line_list, type_list_pos,type_list_neg

        except:
           #print("Traverse Error .. ",file_path)
           return token_list, token_label, line_list, type_list_pos,type_list_neg     
    else:
        #print("file read error")
        return token_list, token_label, line_list, type_list_pos,type_list_neg
