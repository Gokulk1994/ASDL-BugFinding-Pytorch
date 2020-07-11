import TypeChecker

def gen_binary_exp_token(assign_tree, call_from_main):

    wrong_op = {">"  : "<",
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

    op = assign_tree.operator

    x_pos = []
    x_neg = []

    left, _  = TypeChecker.check_type_get_token(assign_tree.left)
    right, _ = TypeChecker.check_type_get_token(assign_tree.right)

    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    if op in wrong_op.keys():

        x_neg = x_neg + left
        x_neg = x_neg + [wrong_op[op]]
        x_neg = x_neg + right   

    return x_pos, x_neg
       
        
