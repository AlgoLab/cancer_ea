"""  The :mod:`main_random_init_ea_node` module contains an example how to use 
methods from `GaNode` class and functions from module `gp_ea_node_operators`.

"""
import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from ea_node.ea_node import EaNode
from gp_ea_node_operators import init_ea_node_individual, mutate_ea_node_individual

import random


def main():
    """  This function is an entry  point of the application.
    """
    random.seed( 111133 )

    x = init_ea_node_individual(EaNode, ['a','b','c','d','e'], 10)  
    x.tree_print() 
    
    y = init_ea_node_individual(EaNode, ['a','b','c','d','e'], 10)  
    y.tree_print() 
    
    z = init_ea_node_individual(EaNode, ['a','b','c','d','e'], 10)  
    z.tree_print() 
    
    mutate_ea_node_individual(z)

    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()

