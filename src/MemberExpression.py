import TypeChecker
import numpy as np

def gen_member_exp_token(member_tree, call_from_main=False):

    x_pos = []
    x_neg = []

    """
    if member_tree.object.type == "MemberExpression":
        x_pos = x_pos + [member_tree.object.name]

    if member_tree.property.type == "Identifier":
        x_pos = x_pos + [member_tree.property.name]
    else:
        x_pos = x_pos + [member_tree.property.type]
    """
    
    obj, _  = TypeChecker.check_type_get_token(member_tree.object)
    prop, _ = TypeChecker.check_type_get_token(member_tree.property)

    x_pos = x_pos + obj
    x_pos = x_pos + prop

    return x_pos, x_neg
       
        
    
