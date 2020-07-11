import ast
from collections import deque

def iter_fields(ast: dict):                                                    
    """Iterate import fields that could be nested"""                           
    for key, node_value in ast.items():                                        
        if key in SIMPLE_KEYS:                                                 
            continue                                                           
        yield node_value                                                       
                                                                               
                                                                               
def iter_child_nodes(node: dict):                                              
    """Iterate over child nodes"""                                             
    for field in iter_fields(node):                                            
        if isinstance(field, dict):                                            
            yield field                                                        
        elif isinstance(field, list):                                          
            for item in field:                                                 
                if isinstance(item, dict):                                     
                    yield item                                                 
                                                                               
                                                                               
def walk(node: dict):                                                          
    """Walk through ast dictionary"""                                          
    todo = deque([node])                                                       
    while todo:                                                                
        node = todo.popleft()                                                  
        for child in iter_child_nodes(node):                                   
            child['parent'] = node                                             
            todo.append(child)                                                 
        yield node                                                             
                                                                               
                                                                               
class NodeVisitor:                                                             
    """                                                                        
    A node visitor base class similar to python ast.NodeVisitor                
    """                                                                        
    def visit(self, node):                                                     
        """Visit a node"""                                                     
        for child in walk(node):                                               
            method = 'visit_{node_type}'.format(node_type=child.get('type'))   
            visitor = getattr(self, method, None)                              
            if visitor:                                                        
                visitor(child)

class ConditionVisitor(NodeVisitor):                                           
    """                                                                        
    Condition visitor class walk through all if statements and separates them  
    into single and binary conditions list                                     
    """                                                                        
    unique_operators = set()                                                   
    bin_conditions = []                                                        
    single_conditions = []                                                     
                                                                               
    def visit_IfStatement(self, node):                                         
        """Visit if condition"""                                               
        test = node.get('test')                                                
        cond = Condition(**test)                                               
        if not cond.is_valid:                                                  
            logger.debug('skipped %s', cond.data)                              
            return                                                             
        if test.get('type') in BIN_OP_TYPES:                                   
            self.bin_conditions.append(cond)                                   
            self.unique_operators.add(cond.op)                                 
        else:                                                                  
            self.single_conditions.append(cond)                                
                                                                               
    @property                                                                  
    def empty(self):                                                           
        """Check if it is empty"""                                             
        return len(self.bin_conditions) == 0