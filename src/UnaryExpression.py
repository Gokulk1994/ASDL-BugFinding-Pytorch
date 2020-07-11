import TypeChecker

def gen_unary_exp_token(assign_tree,call_from_main):
    op = assign_tree.operator
    x_pos = []
    x_neg = []

    unary_operator = ["!", "~", "-"]

    arg, _ = TypeChecker.check_type_get_token(assign_tree.argument)

    x_pos = x_pos + [op]
    x_pos = x_pos + arg

    # negated condition
    if op in unary_operator:
        x_neg += arg
        
    return x_pos, x_neg
       
