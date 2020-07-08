import TypeChecker

def gen_logical_exp_token(logical_tree, call_from_main):
    op = logical_tree.operator
    x_pos = []
    x_neg = []

    left, _  = TypeChecker.check_type_get_token(logical_tree.left)
    right, _ = TypeChecker.check_type_get_token(logical_tree.right)

    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    
    if op == "&&":
        # Type 1 : Incomplete Conditional Expression
        if (logical_tree.left.type == "Identifier") and (logical_tree.right.type != "Identifier" or logical_tree.right.type != "Literal"): 
            x_neg = left
        # Type 2 : incorrectly ordered Boolean expression
        else:
          #if ("Expression" in logical_tree.left.type) and ("Expression" in logical_tree.right.type) :
          if ("Expression" in logical_tree.right.type) :
              
            x_neg = x_neg + right
            x_neg = x_neg + [op]
            x_neg = x_neg + left
 
    return x_pos, x_neg
       
        
    
