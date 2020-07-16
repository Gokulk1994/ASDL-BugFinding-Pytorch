import AssignmentExpression
import UnaryExpression
import BinaryExpression
import LogicalExpression
import CallExpression
import MemberExpression
import UpdateExpression

def check_type_get_token(test_tree, call_from_main = False):

    test_type = test_tree.type

    x_pos = [test_type]
    x_neg = []

    if test_type == "Identifier":
        x_pos = [test_tree.name]

    elif test_type == "Literal":
        x_pos = [test_tree.raw]

    elif test_type == "AssignmentExpression":
        x_pos, x_neg = AssignmentExpression.gen_assign_exp_token(test_tree,call_from_main)     

    elif test_type == "BinaryExpression":
        x_pos, x_neg = BinaryExpression.gen_binary_exp_token(test_tree,call_from_main)

    elif test_type == "CallExpression":
        x_pos, x_neg = CallExpression.gen_logical_exp_token(test_tree,call_from_main)
        
    elif test_type == "LogicalExpression":
        x_pos, x_neg = LogicalExpression.gen_logical_exp_token(test_tree,call_from_main)

    elif test_type == "MemberExpression":
        x_pos, x_neg = MemberExpression.gen_member_exp_token(test_tree,call_from_main)

    elif test_type == "NewExpression":
        pass

    elif test_type == "ThisExpression":
        pass

    elif test_type == "UnaryExpression":
        x_pos, x_neg = UnaryExpression.gen_unary_exp_token(test_tree,call_from_main)
        

    elif test_type == "UpdateExpression":
        x_pos, x_neg = UpdateExpression.gen_update_exp_token(test_tree,call_from_main)

    else:
        pass

    return x_pos, x_neg
    
    
    
            
    
