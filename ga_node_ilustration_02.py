"""  The :mod:`ga_node_ilustration_01` module contains an example how to use 
methods from `GaNode` class and functions from module `ga_node_operators`.

"""

from ga_node import GaNode
from ga_node_operators import init_ga_node_individual, mutate_ga_node_individual

import random


def main():
    """  This function is an entry  point of the application.
    """
    random.seed( 111133 )
          
    x = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    x.tree_print() 
    
    y = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    y.tree_print() 
    
    z = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    z.tree_print() 
    
    mutate_ga_node_individual(z)
   
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()

