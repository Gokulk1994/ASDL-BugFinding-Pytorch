import TypeChecker

def gen_logical_exp_token(Call_tree, call_from_main=False):

    x_pos = []
    x_neg = []

    argument_vector = []
    wrong_arg_done = False

    callee, _    = TypeChecker.check_type_get_token(Call_tree.callee)
    
    for arg in Call_tree.arguments:
        arg_token, _ = TypeChecker.check_type_get_token(arg)
        argument_vector.append(arg_token)

    x_pos = x_pos + callee

    for arg in argument_vector:
        x_pos = x_pos + arg

    if call_from_main == True:
        x_neg = x_neg + callee
        for arg in argument_vector:
            if not wrong_arg_done and len(arg) == 1:
                arg = ["wrong_arg"]
                wrong_arg_done = True
            
            x_neg = x_neg + arg

    return x_pos, x_neg
       
        
    
