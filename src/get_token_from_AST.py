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
        print("invalid data file")
        # Most likely malformed JSON file
        return []

def all_if_as_bugs(json_file):

    data = read_json_file(json_file)
    raw_code = data['raw_source_code']
    split_rawcode = raw_code.split("\n")
    ifcase_linenumber = []
    print(json_file)
    for i,line in enumerate(split_rawcode):
        if ('if (' in line) or ('if(' in line):
            ifcase_linenumber.append(i+1)
    return ifcase_linenumber

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

    try:
        program = visitor.objectify(data["ast"])
    except:
        print("ERROR : ", file_path)
        return token_list, token_label, line_list, type_list_pos,type_list_neg
    try:
        for node in program.traverse():
            if node.type == "IfStatement":
                x_pos, x_neg = check_type_get_token(node.test, True)
                
                if x_pos != None and len(x_pos):
                    token_list.append(x_pos)
                    token_label.append(0)
                    line_list.append(node.loc['start']['line'])
                    type_list_pos.append(node.test.type)
                    
                if Get_Negative == True and x_neg!= None and len(x_neg):
                    token_list.append(x_neg)
                    token_label.append(1)
                    line_list.append(node.loc['start']['line'])
                    type_list_neg.append(node.test.type)

        assert len(token_list) == len(line_list) == len(token_label)

        """
        if (len(token_list) != len(line_list)) or (len(token_list) != len(token_label)):
            print("Assert Error : len mismatch error")
            return [],[],[],[],[]
        """
        return token_list, token_label, line_list, type_list_pos,type_list_neg
    except:
        print("Traverse Error .. ",file_path)
        return [],[],[],[],[]
        #raise UnknownNodeTypeError(file_path)
    
    #return token_list, token_label, line_list
