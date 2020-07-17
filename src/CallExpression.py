import TypeChecker

def gen_logical_exp_token(Call_tree, call_from_main=False):
    """
    generate correct and incorrect string tokens from the callee expression tree
    args:
        Call_tree : the test tree of CalleeExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """

    x_pos = []
    x_neg = []

    argument_vector = []
    wrong_arg_done = False

    # get the token for the callee 
    callee, _    = TypeChecker.check_type_get_token(Call_tree.callee)
    
    # get the string token for each argument from the AST tree
    for arg in Call_tree.arguments:
        arg_token, _ = TypeChecker.check_type_get_token(arg)
        argument_vector.append(arg_token)

    # geenrate correct sample
    x_pos = x_pos + callee

    for arg in argument_vector:
        x_pos = x_pos + arg

    # Type 3: Wrong Identifier
    # generate incorrect sample by changing the argument  to "incorrect"
    if call_from_main == True:
        x_neg = x_neg + callee
        for arg in argument_vector:
            if not wrong_arg_done and len(arg) == 1:
                arg = ["wrong_arg"]
                wrong_arg_done = True
            
            x_neg = x_neg + arg

    return x_pos, x_neg
       
        
    
