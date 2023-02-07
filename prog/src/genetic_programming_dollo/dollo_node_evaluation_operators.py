""" The :mod:`dollo_node_evaluation_operators` module contains operators
for evaluation of DolloNode individuals.

"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)


from functools import lru_cache 

from bitstring import BitArray

from reads.read_element import ReadElement

def assign_reads_to_dollo_tree(root, reads):
    """ Assigns all the reads to the closest nodes in the tree,
    respectively.
    
    Args:
        root (DolloNode): root of the tree to whose nodes reads should be assigned.
        reads (list): list of the reads that should be assigned to various nodes in the tree.

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
    
@lru_cache(maxsize=8192, typed=True)
def dollo_closest_node_distance(individual, read):
    """ Finds the closest node within the tree for the given read, as well
        as distance betwwen that node and read.
    
    Args:
        individual (DoloNode): individual that represents root of the node.
        read : read that should be assigned to the node in the tree.

    Notes:    
        Node is the closest according to metrics that is induced with Hamming
        distance.
        This method consults information about unknown reads (that are stored 
        in bitarray unknown_read) within read element. 
    """
    (c_n,d) = individual.closest_node_in_tree(read)
    return (c_n,d)

def dollo_evaluate_direct_only_level0(reads, alpha, beta, individual):
    """ Evaluation of the individual. Doesnt't count false positives.

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = 0
    for read in reads:
        (node, d) = dollo_closest_node_distance(individual,read)
        objection_value += d
    return objection_value

def dollo_evaluate_direct_only_level1(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        one position.        

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = 0
    for read in reads:
        for i in range(0,read.binary_read.length):
            if( read.binary_read[i]):
                read2 = BitArray(read.binary_read)
                read2[i]=False
                re2 = ReadElement("XXX2", read2, read.unknown_read)
                (node, d) = dollo_closest_node_distance(individual,re2)
                objection_value += d
    return objection_value

def dollo_evaluate_direct_only_level2(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        two positions.        
    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = 0
    for read in reads:
        for i in range(0,read.binary_read.length):
            for j in range(i+1, read.binary_read.length):
                if( read.binary_read[i] and read.binary_read[j]):
                    read2 = BitArray(read.binary_read)
                    read2[i]=False
                    read2[j]=False
                    re2 = ReadElement("XXX2", read2, read.unknown_read)
                    (node, d) = dollo_closest_node_distance(individual,re2)
                    objection_value += d 
    return objection_value

def dollo_evaluate_direct_only_level3(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        three positions.        
    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = 0
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
                        (node, d) = dollo_closest_node_distance(individual,re2)
                        objection_value += d * alpha * alpha * alpha
    return objection_value

def dollo_evaluate_direct_level0(reads, alpha, individual):
    """ Evaluation of the individual. Doesnt't count false positives.

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    return dollo_evaluate_direct_only_level0(reads, alpha, individual)

def dollo_evaluate_direct_level1(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        one position.        

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_only_level0(reads, alpha, beta, individual) * (1-alpha)
    objection_value += dollo_evaluate_direct_only_level1(reads, alpha, beta, individual) * alpha
    return objection_value

def dollo_evaluate_direct_level2(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        two positions.        
    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_only_level0(reads, alpha, beta, individual) * (1-alpha-alpha*alpha)
    objection_value += dollo_evaluate_direct_only_level1(reads, alpha, beta, individual) * alpha
    objection_value += dollo_evaluate_direct_only_level2(reads, alpha, beta, individual) * alpha * alpha
    return objection_value

def dollo_evaluate_direct_level3(reads, alpha, beta, individual):
    """ Evaluation of the individual. Takes into account false positives on
        three positions.        
    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_only_level0(reads, alpha, beta, individual) * (1-alpha-alpha*alpha-alpha*alpha*alpha)
    objection_value += dollo_evaluate_direct_only_level1(reads, alpha, beta,  individual) * alpha
    objection_value += dollo_evaluate_direct_only_level2(reads, alpha, beta, individual) * alpha * alpha
    objection_value += dollo_evaluate_direct_only_level3(reads, alpha, beta, individual) * alpha * alpha * alpha
    return objection_value

def evaluate_dollo_node_direct(reads, individual, alpha, beta):
    """ Evaluation of the individual.

    Args:
        reads (list): list of the reads that should be assigned to various nodes in the tree.
        individual (DoloNode): individual that should be evaluated.
        alpha: probability of false positive
    Returns:            
        pair where first element is objection value of the individual to be
            evaluated.    
    """
    return (dollo_evaluate_direct_level1(reads, individual, alpha, beta),)    

