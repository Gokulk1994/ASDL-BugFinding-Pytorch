import TypeChecker

def gen_update_exp_token(update_tree,call_from_main):
    """
    generate correct and incorrect string tokens from the update expression tree
    args:
        Call_tree : the test tree of UpdateExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """

    # get the operator of the update expression
    op = update_tree.operator

    # type of update expression, pre operation or post operation 
    prefix = update_tree.prefix
    
    x_pos = []
    x_neg = []

    # string token of the argument
    arg, _ = TypeChecker.check_type_get_token(update_tree.argument)

    # form correct token
    # Type 3: wrong identifier
    # if the argument is of type identifier, change the identifier to "incorrect" 
    if prefix == "True":
        x_pos = x_pos + [op]
        x_pos = x_pos + arg
        
        if update_tree.argument.type == "Identifier":
            x_neg = x_neg + [op]
            x_neg = ["incorrect"]
    else:
        x_pos = x_pos + arg
        x_pos = x_pos + [op]

        if update_tree.argument.type == "Identifier":
            x_neg = ["incorrect"]
            x_neg = x_neg + [op]
    
    
        
    return x_pos, x_neg
       
