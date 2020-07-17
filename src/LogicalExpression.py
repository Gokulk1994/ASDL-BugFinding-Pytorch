import TypeChecker

def gen_logical_exp_token(logical_tree, call_from_main):

    """
    generate correct and incorrect string tokens from the logical expression tree
    args:
        logical_tree : the test tree of LogicalExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    """

    # fetch the logical operator from the AST tree
    op = logical_tree.operator

    x_pos = []
    x_neg = []
    x_neg_list = []

    # obtain the left and right tree from the corresponding trees
    left, _  = TypeChecker.check_type_get_token(logical_tree.left)
    right, _ = TypeChecker.check_type_get_token(logical_tree.right)
    
    x_pos = x_pos + left
    x_pos = x_pos + [op]
    x_pos = x_pos + right

    cond1_type = ["Identifier", "Literal"]
    cond2_type = ["MemberExpression", "CallExpression"]

    # incorrect token formation
    if op == "&&":
        # Type 1 : Incomplete Conditional Expression
        # store only the right tree
        if (logical_tree.left.type == "Identifier") and (logical_tree.right.type not in cond1_type): 
            x_neg = right

        # Type 2 : incorrectly ordered Boolean expression
        # swap the left and right tree on both sides of the operator
        else:
          if logical_tree.right.type in cond2_type :

            x_neg = x_neg + right
            x_neg = x_neg + [op]
            x_neg = x_neg + left

    
    return x_pos, x_neg
       
        
    
