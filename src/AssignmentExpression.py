from MemberExpression import *

def gen_assign_exp_token(assign_tree):
    op = assign_tree.operator
    x_pos = []
    x_neg = []

    if assign_tree.left.type == "Identifier" or node.test.type == "Literal":
        left = [assign_tree.left.name]
    else:
        left = [assign_tree.left.type]

    if assign_tree.right.type == "Identifier":
        right = [assign_tree.right.name]
    else:
        right = [assign_tree.right.type]

    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right
    
    x_neg = [x_pos[2], x_pos[1], x_pos[0]]

    return x_pos, x_neg
       
        
    
