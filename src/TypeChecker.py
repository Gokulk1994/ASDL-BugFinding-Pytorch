import AssignmentExpression
import UnaryExpression
import BinaryExpression


def check_type_get_token(test_tree):

    test_type = test_tree.type

    x_pos = [test_type]
    x_neg = None

    if test_type == "Identifier":
        x_pos = [test_tree.name]
    elif test_type == "Literal":
        x_pos = [test_tree.raw]
    elif test_type == "AssignmentExpression":
        x_pos, x_neg = AssignmentExpression.gen_assign_exp_token(test_tree)        
    elif test_type == "BinaryExpression":
        x_pos, x_neg = BinaryExpression.gen_binary_exp_token(test_tree)
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
        x_pos, x_neg = UnaryExpression.gen_unary_exp_token(test_tree) 
    elif test_type == "UpdateExpression":
        pass
    else:
        pass

    return x_pos, x_neg
    
    
    
            
    
