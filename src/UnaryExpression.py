from MemberExpression import *
import numpy as np


def gen_unary_exp_token(assign_tree):
    op = [assign_tree.operator]
    x_pos = []
    x_neg = []
    
    if assign_tree.argument.type == "Identifier":
        arg = [assign_tree.argument.name]
    else:
        arg = [assign_tree.argument.type]


    x_pos = x_pos + op
    x_pos = x_pos + arg

    # negated condition
    x_neg = arg

    return x_pos, x_neg
       
