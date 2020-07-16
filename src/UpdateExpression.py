import TypeChecker

def gen_update_exp_token(update_tree,call_from_main):
    op = update_tree.operator
    prefix = update_tree.prefix
    
    x_pos = []
    x_neg = []

    arg, _ = TypeChecker.check_type_get_token(update_tree.argument)

    if prefix == "True":
        x_pos = x_pos + [op]
        x_pos = x_pos + arg
    else:
        x_pos = x_pos + arg
        x_pos = x_pos + [op]
        
    return x_pos, x_neg
       
