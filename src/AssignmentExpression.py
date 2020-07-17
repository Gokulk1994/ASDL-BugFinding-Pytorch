import TypeChecker

def gen_assign_exp_token(assign_tree,call_from_main):
    """
    generate correct and incorrect string tokens from the AssignmentExpression tree
    args:
        assign_tree : the test tree of AssignmentExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """

    # get assignment operator
    op = assign_tree.operator
    x_pos = []
    x_neg = []

    # get the left and right tree
    left, _  = TypeChecker.check_type_get_token(assign_tree.left)
    right, _ = TypeChecker.check_type_get_token(assign_tree.right)

    # form the correct example
    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right
    

    return x_pos, x_neg
       
        
    
