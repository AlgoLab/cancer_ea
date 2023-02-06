""" The :mod:`ea_node_operators` module contains ovolutionary operators
for EaNode individuals.

"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from anytree import NodeMixin, RenderTree, PostOrderIter
from bitstring import BitArray

from utils.collections import count, index_of, last_index_of
from ea_node import EaNode


def assign_reads_to_ea_tree( root, reads):
    """ Assigns all the reads to the closest nodes in the tree,
    respectively.
    
    Args:
        root (EaNode): root of the tree to whose nodes reads should be assigned.
        reads (list): list of the reads that should be assigned to various nodes in the tree.

    Returns:            
        list that contains two components: 
            1) list of the asignments  - list of pairs (node, read);
            2) sum of the distances among reads and the closest nodes that
            are assigned to those reads respectively.
    
    Note:
        Function uses the func:`~EaNode.closest_node_in_tree` function 
        from the :mod:`ga_node` module.
    """
    total_distance = 0
    complete_assignment = {}
    for read in reads:
        (node, d) = root.closest_node_in_tree( read )
        complete_assignment[read] = node
        total_distance += d
    return (complete_assignment, total_distance)    
    
    
def init_ea_node_individual(ind_class, labels, size):
    """ Initialization of the individual.
    Args:
        ind_class: class of the individual to be initialized.
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        size(int): size of the tree that should be initialized.
    Returns: 
        EaNode: individuak that is initialized.           
    """
    rootBitArray = BitArray(int = 0, length = len(labels) )
    root = ind_class('--', rootBitArray)
    root.tree_initialize(labels, size)
    return root

def evaluate_ea_node_individual(reads, individual):
    """ Evaluation of the individual.

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (EaNode): individual that should be evaluated.

    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    objection_value = 0
    for read in reads:
        (node, d) = individual.closest_node_in_tree( read )
        objection_value += d
    return (objection_value,)    

def crossover_ea_node_individuals(individual1, individual2):
    """ Crossover between individual1 and individual2.
    
    Args: individual1 (EaNode): first individual in crossover.
        individual2 (EaNode): second individual in crossover.

    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    print( "In crossover" )
    return (individual1, individual2)

def mutate_ea_node_individual(individual):
    """ Mutatuion of the individual.

    Args:
        individual (EaNode): individual that will be mutated.

    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    print( "In mutation" )
    #randomIndex = random.choice(individual.children)
    return (individual,)
