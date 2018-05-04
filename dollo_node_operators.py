""" The :mod:`dollo_node_operators` module contains ovolutionary operators
for DolloNode individuals.

"""

from anytree import NodeMixin, RenderTree, PostOrderIter
from bitstring import BitArray

from collection_helpers import count, index_of, last_index_of
from read_element import ReadElement
from dollo_node import DolloNode


def assign_reads_to_dollo_tree(root, reads):
    """ Assigns all the reads to the closest nodes in the tree,
    respectively.
    
    Args:
         root (DolloNode): root of the tree to whose nodes reads should be assigned.
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
     
    Returns:            
        list that contains two components: 
            1) list of the asignments  - list of pairs (node, read);
            2) sum of the distances among reads and the closest nodes that
            are assigned to those reads respectively.
    
    Note:
        Function uses the func:`~DolloNode.closest_node_in_tree` function 
        from the :mod:`ga_node` module.
    """
    total_distance = 0
    complete_assignment = {}
    for read in reads:
        (node, d) = root.closest_node_in_tree( read )
        complete_assignment[read] = node
        total_distance += d
    return (complete_assignment, total_distance)    
    
    
def init_dollo_node_individual(ind_class, labels, k):
    """ Initialization of the individual.
    Args:
        ind_class: class of the individual to be initialized.
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        size(int): size of the tree that should be initialized.
    Returns: 
        DolloNode: individuak that is initialized.           
    """
    rootBitArray = BitArray(int = 0, length = len(labels) )
    root = ind_class('--', rootBitArray)
    root.tree_initialize(labels, k)
    return root

def evaluate_direct_level0(reads, alpha, individual):
    """ Evaluation of the individual. Doesnt't count false positives.

    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    objection_value = 0
    for read in reads:
        (node, d) = individual.closest_node_in_tree( read )
        objection_value += d
    return objection_value

def evaluate_direct_level1(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        one position.        

    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    objection_value = evaluate_direct_level0(reads, alpha, individual)
    for read in reads:
        for i in range(0,read.binary_read.length):
            if( read.binary_read[i]):
                read2 = BitArray(read.binary_read)
                read2[i]=False
                re2 = ReadElement("XXX2", read2, read.unknown_read)
                (node, d) = individual.closest_node_in_tree(re2)
                objection_value += d * alpha
    return objection_value

def evaluate_direct_level2(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        two positions.        
    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    objection_value = evaluate_direct_level1(reads, alpha, individual)
    for read in reads:
        for i in range(0,read.binary_read.length):
            for j in range(i+1, read.binary_read.length):
                if( read.binary_read[i] and read.binary_read[j]):
                    read2 = BitArray(read.binary_read)
                    read2[i]=False
                    read2[j]=False
                    re2 = ReadElement("XXX2", read2, read.unknown_read)
                    (node, d) = individual.closest_node_in_tree(re2)
                    objection_value += d * alpha * alpha
    return objection_value


def evaluate_direct_level3(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        three positions.        
    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    objection_value = evaluate_direct_level2(reads, alpha, individual)
    for read in reads:
        for i in range(0,read.binary_read.length):
            for j in range(i+1, read.binary_read.length):
                for k in range(j+1, read.binary_read.length):
                    if( read.binary_read[i] and read.binary_read[j] and read.binary_read[k]):
                        read2 = BitArray(read.binary_read)
                        read2[i]=False
                        read2[j]=False
                        read2[k]=False
                        re2 = ReadElement("XXX2", read2, read.unknown_read)
                        (node, d) = individual.closest_node_in_tree(re2)
                        objection_value += d * alpha * alpha
    return objection_value

def evaluate_dollo_node_individual(reads, individual, alpha):
    """ Evaluation of the individual.

    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    return (evaluate_direct_level2(reads, individual, alpha),)    


def crossover_dollo_node_individuals(individual1, individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    print( "In crossover" )
    return (individual1, individual2)

def mutate_dollo_node_individual(individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    print( "In mutation" )
    #randomIndex = random.choice(individual.children)
    return (individual,)
