""" The :mod:`dollo_node_initialization_operators` module contains operators
for initialization of DolloNode individuals.

"""

from bitstring import BitArray
 
    
def init_dollo_node_individual(ind_class, labels, k):
    """ Initialization of the individual.
    Args:
        ind_class: class of the individual to be initialized - should be 
            DolloNode.
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
    Returns: 
        DolloNode: individual that is initialized.           
    """
    rootBitArray = BitArray(int = 0, length = len(labels) )
    root = ind_class('--', rootBitArray)
    root.tree_initialize(labels, k)
    return root

