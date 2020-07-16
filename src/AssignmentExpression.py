import TypeChecker

def gen_assign_exp_token(assign_tree,call_from_main):
    op = assign_tree.operator
    x_pos = []
    x_neg = []

    left, _  = TypeChecker.check_type_get_token(assign_tree.left)
    right, _ = TypeChecker.check_type_get_token(assign_tree.right)

    #print("Assign op ", op)
    
    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right
    
    #x_neg = [x_pos[2], x_pos[1], x_pos[0]]

    return x_pos, x_neg
       
        
    
