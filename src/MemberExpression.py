import TypeChecker
import numpy as np

def gen_member_exp_token(member_tree, call_from_main=False):
    """
    generate correct and incorrect string tokens from the member expression tree
    args:
        member_tree : the test tree of MemberExpression type
        call_from_main : to check function is called my main or as a part of sub expression
    return:
        list of correct and incorrect string tokens
    """
    x_pos = []
    x_neg = []

    # get the object and property sub tree tree
    obj, _  = TypeChecker.check_type_get_token(member_tree.object)
    prop, _ = TypeChecker.check_type_get_token(member_tree.property)

    # form the correct token
    x_pos = x_pos + obj
    x_pos = x_pos + prop

    return x_pos, x_neg
       
        
    
