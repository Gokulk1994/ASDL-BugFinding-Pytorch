import TypeChecker

def gen_logical_exp_token(logical_tree, call_from_main):
    op = logical_tree.operator
    x_pos = []
    x_neg = []
    x_neg_list = []

    left, left_neg  = TypeChecker.check_type_get_token(logical_tree.left)
    right, right_neg = TypeChecker.check_type_get_token(logical_tree.right)
    
    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    cond1_type = ["LogicalExpression", "BinaryExpression"]
    cond2_type = ["MemberExpression", "CallExpression"]

   
    if op == "&&":
        # Type 1 : Incomplete Conditional Expression
        if (logical_tree.left.type == "Identifier") and (logical_tree.right.type in cond1_type): 
            x_neg = left

        # Type 2 : incorrectly ordered Boolean expression
        else:
          if logical_tree.right.type in cond2_type :

            x_neg = x_neg + right
            x_neg = x_neg + [op]
            x_neg = x_neg + left

    """
    x_neg_list.append(x_neg)
    
    if left_neg != []:
        for i in left_neg:
            x_neg_list.append(i)

    if right_neg != []:
        for j in right_neg:
            x_neg_list.append(j)
    """
    
    return x_pos, x_neg
       
        
    
