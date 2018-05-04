""" The :mod:`dollo_node_operators` module contains ovolutionary operators
for DolloNode individuals.

"""
import random

from functools import lru_cache 

from bitstring import BitArray

from read_element import ReadElement

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

@lru_cache(maxsize=8192, typed=True)
def dolo_closest_node_distance(individual, read):
    """ Finds the closest node within the tree for the given read, as well
        as distance betwwen that node and read.
    
    Args:
         individual (DoloNode): individual that represents root of the node.
         read : read that should be assigned to the node in the tree.

    Notes:    
        Node is the closest according to metrics that is induced with Hamming
        distance.
        This method consults informations about unknown reads (that are stored 
        in bitarry unknown_read) within read element. 
    """
    (c_n,d) = individual.closest_node_in_tree(read)
    return (c_n,d)

def dollo_evaluate_direct_level0(reads, alpha, individual):
    """ Evaluation of the individual. Doesnt't count false positives.

    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
         objection value of the individual to be evaluated.    
    """
    objection_value = 0
    for read in reads:
        (node, d) = dolo_closest_node_distance(individual,read)
        objection_value += d
    return objection_value

def dollo_evaluate_direct_level1(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        one position.        

    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
         objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_level0(reads, alpha, individual)
    for read in reads:
        for i in range(0,read.binary_read.length):
            if( read.binary_read[i]):
                read2 = BitArray(read.binary_read)
                read2[i]=False
                re2 = ReadElement("XXX2", read2, read.unknown_read)
                (node, d) = dolo_closest_node_distance(individual,re2)
                objection_value += d * alpha
    return objection_value

def dollo_evaluate_direct_level2(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        two positions.        
    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
         objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_level1(reads, alpha, individual)
    for read in reads:
        for i in range(0,read.binary_read.length):
            for j in range(i+1, read.binary_read.length):
                if( read.binary_read[i] and read.binary_read[j]):
                    read2 = BitArray(read.binary_read)
                    read2[i]=False
                    read2[j]=False
                    re2 = ReadElement("XXX2", read2, read.unknown_read)
                    (node, d) = dolo_closest_node_distance(individual,re2)
                    objection_value += d * alpha * alpha
    return objection_value


def dollo_evaluate_direct_level3(reads, alpha, individual):
    """ Evaluation of the individual. Takes into account false positives on
        three positions.        
    Args:
         reads (list): list of the reads that should be assigned to various nodes 
                  in the tree.
         individual (DoloNode): individual that should be evaluated.
         alpha: probability of false positive
    Returns:            
         objection value of the individual to be evaluated.    
    """
    objection_value = dollo_evaluate_direct_level2(reads, alpha, individual)
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
                        (node, d) = dolo_closest_node_distance(individual,re2)
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
    return (dollo_evaluate_direct_level2(reads, individual, alpha),)    



def crossover_dollo_node_individuals(individual1, individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    return (individual1, individual2)

def dollo_mutation_minus_node_add(labels, k, individual):
    """ Mutation of the individual, by randomly adding one minus node

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        individual that is mutated e.g. output of the mutation process.
    """
    random_parent = random.choice(individual.descendants)
    random_label = random.choice(labels)
    # print( "In mutation" )
    # print (random_parent, random_label)
    return individual

def dollo_mutation_minus_node_remove(labels, k, individual):
    """ Mutation of the individual, by randomly removing one minus node

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        individual that is mutated e.g. output of the mutation process.
    """
    return individual

def dollo_mutation_node_up(labels, k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        up to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        individual that is mutated e.g. output of the mutation process.
    """
    return individual


def dollo_mutation_node_down(labels, k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        down to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        indidivual that is mutated e.g. output of the mutation process.
    """
    return individual


def mutate_dollo_node_individual(labels, k, individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    individual = dollo_mutation_minus_node_add(labels, k, individual)
    return (individual,)
