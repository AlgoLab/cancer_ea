"""
This module contains an example how to GA methods that uses Deap.

Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from ga_node import GaNode
from ga_node import init_ga_node_individual, mutation_ga_node

import random


def main():
    random.seed( 111133 )
          
    x = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    x.tree_print() 
    
    y = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    y.tree_print() 
    
    z = init_ga_node_individual(GaNode, ['a','b','c','d','e'], 10)  
    z.tree_print() 
    
    mutation_ga_node(z)
   
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()

