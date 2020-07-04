import TypeChecker

def gen_binary_exp_token(assign_tree):

    wrong_op = {">" : "<",
                "<" : "> ",
                ">=": "<=",
                "<=": ">=",
               }
        
    op = assign_tree.operator
    x_pos = []
    x_neg = None

    left, _  = TypeChecker.check_type_get_token(assign_tree.left)
    right, _ = TypeChecker.check_type_get_token(assign_tree.right)

    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    if op in wrong_op.keys():
        x_neg = [x_pos[0], wrong_op[op], x_pos[2]]
    else:
        x_neg = [x_pos[2], x_pos[1] , x_pos[0]]

    return x_pos, x_neg
       
        
