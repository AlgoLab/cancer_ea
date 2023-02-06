"""  The :mod:`ga_node_ilustration_01` module contains an example how to use 
methods from `EaNode` class and functions from module `ea_node_operators`.

"""
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from dollonode.dollo_node import DolloNode
from dollo_node_initialization_operators import init_dollo_node_individual

import random


def main():
    """  This function is an entry  point of the application.
    """
    random.seed( 111133 )

    x = init_dollo_node_individual(DolloNode, ['a','b','c','d','e','f'], 2)  
    x.tree_print() 
    
    y = init_dollo_node_individual(DolloNode, ['a','b','c','d','e','f'], 2)  
    y.tree_print() 
    
    z = init_dollo_node_individual(DolloNode, ['a','b','c','d','e', 'f'], 2)  
    z.tree_print() 

    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()

