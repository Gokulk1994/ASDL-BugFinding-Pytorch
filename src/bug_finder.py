from get_token_from_AST import *

def find_bugs(fp):
    return [1,2,3]


if __name__ == '__main__':
    
    token_list, token_label, line_list, test_list = get_token("10055_7513_a_dynamicContent.json")
    for i,token in enumerate(token_list):
        print(line_list[i])
        print(test_list[i])
        print(token)
        print(token_label[i])
        print("----------------------------")

    
                
