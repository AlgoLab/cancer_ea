""" The :mod:`dollo_node_mutation_operators` module contains operators
for mutation of DolloNode individuals.

"""
import copy
import random

def mutation_dollo_node_add(labels,k,individual):
    """ Mutation of the individual, by randomly adding one node

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    individual_n = copy.deepcopy( individual )
    random_parent = random.choice(individual_n.descendants)
    random_label = random.choice(labels)
    random01 = random.random()
    label_is_plus = random01 < (len(labels)/float(1+len(individual_n.descendants)) ) 
    if(label_is_plus):
        # adding plus label and removing same plus label
        random_label += '+'
    else:
        # adding minus label and removing same plus label
        random_label += '-'
    return (False,individual_n)

def mutation_dollo_node_remove(labels, k, individual):
    """ Mutation of the individual, by randomly removing one node

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    individual_n = copy.deepcopy( individual )
    return (False,individual_n)

def mutation_dollo_node_promote(labels, k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        up to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    individual_n = copy.deepcopy( individual )
    return (False,individual_n)


def mutation_dollo_node_demote(labels, k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        down to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    individual_n = copy.deepcopy( individual )
    return (False,individual_n)


def mutation_dollo_node_combined(labels, k, individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    (success,individual_new) = dollo_mutation_node_add(labels, k, individual)
    if(success):
        return (individual_new,)
    else:
        individual_n = copy.deepcopy( individual )
        return (individual_n,)

def mutate_dollo_node_local_search(labels, k, individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    (success,individual_new) = dollo_mutation_node_add(labels, k, individual)
    if(success):
        return (individual_new,)
    else:
        individual_n = copy.deepcopy( individual )
        return (individual_n,)
