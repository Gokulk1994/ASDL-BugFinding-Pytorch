import TypeChecker

def gen_binary_exp_token(assign_tree, call_from_main):
    """
    generate correct and incorrect string tokens from the binary expression tree
    args:
        assign_tree : the test tree of BinaryExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """
    # Keys : all binary operators, values : coressponding wrong operator
    wrong_op = {
                ">"  : "<",
                "<"  : "> ",
                ">=" : "<=",
                "<=" : ">=",
                "!=" : "==",
                "==" : "!=",
                "===" : "!==",
                "!==" : "===",
                "&"  : "&&",
                "|"  : "||",
                "+"  : "-",
                "-"  : "+",
                "/"  : "*",
                "*"  : "/",
                "%"  : "/",
                "<<" : ">>",
                ">>" : "<<",
                ">>>" : "<<<"
               }

    # binary operator
    op = assign_tree.operator

    x_pos = []
    x_neg = []

    # get the tokens of the left and right tree of binary expression
    left, _  = TypeChecker.check_type_get_token(assign_tree.left)
    right, _ = TypeChecker.check_type_get_token(assign_tree.right)

    # form list of tokens
    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    # Type 5: Wrong operator
    # replace binary operator with corresponding wrong operator to generate incorrect examples
    if op in wrong_op.keys():
        x_neg = x_neg + left
        x_neg = x_neg + [wrong_op[op]]
        x_neg = x_neg + right   
    
    return x_pos, x_neg
       
        
