from typing import List, Dict, Union, DefaultDict
import visitor
import codecs
import json

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

def find_bugs(fp):
    return [1,2,3]


if __name__ == '__main__':
    data = read_json_file("89_7787_c_layout.json")
    program = visitor.objectify(data["ast"])
    if_nodes = []
    line_list = []
    test_list = []
    test_type_list = []
    token_list = []

    for node in program.traverse():
        if node.type == "IfStatement":
            if_nodes.append(node)

    for ifcase in if_nodes:
        if_cond = visitor.objectify(ifcase)
        for node in if_cond.traverse():
            fields = node.fields
            for field in fields:
                if field == 'loc':
                    line_list.append(node.loc['start']['line'])
                if field == 'test':
                    test_list.append(node.test)
                if field == 'consequent':
                    # for later use
                    pass
                
    assert len(if_nodes) == len(line_list) == len(test_list)

    found  = False
    for i, test_tree in enumerate(test_list):
        token = []
        test_type = test_tree.type
        test_type_list.append(test_type)
        token.append(test_type)

        for test in test_tree.traverse():
            if test_type == "AssignmentExpression":
                fields = test.fields
                for field in fields:
                    if field == "operator":
                        token.append(test.left.dict()['type'])
                        token.append(test.operator)
                        token.append(test.right.dict()['type'])
                        left = test.left
                        right = test.right
                        found = True
                        break

                

                for node in left.traverse():
                    if left.type == 'Identifier':
                        token.append(node.name)
                        break
                    
                for node in right.traverse():
                    if right.type == 'Identifier':
                        token.append(node.name)
                        break
                    
            if found == True:
                break
                        
                        
        token_list.append(token)
        print(token_list)
        print("---------------------")
    
    
                
