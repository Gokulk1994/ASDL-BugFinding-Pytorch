import TypeChecker

def gen_unary_exp_token(unary_tree,call_from_main):
    
    """
    generate correct and incorrect string tokens from the unary expression tree
    args:
        unary_tree : the test tree of UnaryExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """

    # get the unary operator
    op = unary_tree.operator
    x_pos = []
    x_neg = []

    #unary_operator = ["!", "~", "-"]
    unary_operator = ["!"]

    # get the argument of the unary tree
    arg, _ = TypeChecker.check_type_get_token(unary_tree.argument)

    # form the correct token
    x_pos = x_pos + [op]
    x_pos = x_pos + arg

    # Type 4: negated condition
    # add only the argument, remove the ! unary operator 
    if op in unary_operator:
        x_neg += arg

    
    return x_pos, x_neg
       
