
from AssignmentExpression import *
from UnaryExpression import *



def check_type_get_token(test_tree):

    test_type = test_tree.type

    x_pos = [test_type]
    x_neg = None

    if test_type == "Identifier" or test_type == "Literal":
        x_pos = [test_tree.name]
    elif test_type == "AssignmentExpression":
        x_pos, x_neg = gen_assign_exp_token(test_tree)        
    elif test_type == "BinaryExpression":
        pass
    elif test_type == "CallExpression":
        pass
    elif test_type == "LogicalExpression":
        pass
    elif test_type == "MemberExpression":
        pass
    elif test_type == "NewExpression":
        pass
    elif test_type == "ThisExpression":
        pass
    elif test_type == "UnaryExpression":
        x_pos, x_neg = gen_unary_exp_token(test_tree) 
    elif test_type == "UpdateExpression":
        pass
    else:
        pass

    return x_pos, x_neg
    
    
    
            
    
