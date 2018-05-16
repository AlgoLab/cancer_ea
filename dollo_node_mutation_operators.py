""" The :mod:`dollo_node_mutation_operators` module contains operators
for mutation of DolloNode individuals.

"""
import copy
import random

from bitstring import BitArray

from anytree import search

from dollo_node import DolloNode

from dollo_node_helpers import dollo_subtree_add_correct_minus_node

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
    #print("************************************************************")
    #print("* mutation_dollo_node_add                                  *")
    #print("at start: ",individual)
    #print("* mutation_dollo_node_add:                                 *")
    #print("************************************************************")                               
    individual_n = copy.deepcopy( individual )
    random01 = random.random()
    label_is_plus = random01 < (len(labels)/float(1+len(individual_n.descendants)) ) 
    if(label_is_plus):
        # adding plus label and removing same plus label
        random_parent = random.choice(individual_n.descendants)
        random_label = random.choice(labels)
        # remove old plus node
        old_plus_node = search.find(individual_n,lambda node: node.node_label == random_label+'+')
        parent_old_plus_node = old_plus_node.parent
        for child in old_plus_node.children:
            child.parent = parent_old_plus_node
        old_plus_node.parent = None
        num_removed = parent_old_plus_node.tree_remove_incorrect_minus_nodes()
        # create new leaf node
        new_bit_array = BitArray()
        new_node = DolloNode(random_label+'+',new_bit_array)
        # attach leaf node
        random_parent.attach_child(new_node)
        # randomly add minus correct nodes
        for i in range(0,num_removed):
            dollo_subtree_add_correct_minus_node(individual_n, labels, k)
    else:
        # adding minus label and removing same plus label
        dollo_subtree_add_correct_minus_node(individual_n,labels,k)
    individual_n.tree_compact_vertical()
    individual_n.tree_compact_horizontal()
    individual_n.tree_rearange_by_label()
    #print("************************************************************")
    #print("* mutation_dollo_node_add                                  *")
    #print("at end: ",individual_n)
    #print("* mutation_dollo_node_add:                                 *")
    #print("************************************************************")                               
    mutant_is_different = not individual.tree_is_equal(individual_n)
    return (mutant_is_different,individual_n)

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
    #print("************************************************************")
    #print("* mutation_dollo_node_remove                               *")
    #print("at start: ",individual)
    #print("* mutation_dollo_node_remove                               *")
    #print("************************************************************")                               
    individual_n = copy.deepcopy( individual )
    random_node = random.choice(individual_n.descendants)
    random_label = random_node.node_label[:-1]
    if(random_node.node_label==random_label+'-'):
        # delete minus node
        parent_random_node = random_node.parent
        for child in random_node.children:
            child.parent = parent_random_node
        random_node.parent = None
    elif(random_node.node_label==random_label+'+'):
        # delete plus node
        parent_random_node = random_node.parent
        for child in random_node.children:
            child.parent = parent_random_node
        random_node.parent = None
        num_removed = parent_random_node.tree_remove_incorrect_minus_nodes()
        print(individual_n)
        # create new plus node and attach it
        parent_of_new_node = random.choice(individual_n.descendants)
        new_bit_array = BitArray()
        new_node = DolloNode(random_label+'+',new_bit_array)
        parent_of_new_node.attach_child(new_node)
        for i in range(0,num_removed-1):
            dollo_subtree_add_correct_minus_node(parent_of_new_node, labels, k)
    individual_n.tree_compact_vertical()
    individual_n.tree_compact_horizontal()
    individual_n.tree_rearange_by_label()
    #print("************************************************************")
    #print("* mutation_dollo_node_remove                               *")
    #print("at end: ",individual_n)
    #print("* mutation_dollo_node_remove                               *")
    #print("************************************************************")                               
    mutant_is_different = not individual.tree_is_equal(individual_n)
    return (mutant_is_different,individual_n)

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


def mutation_dollo_node_combine(labels, k, individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    random01 = random.random()
    if(random01 <= 0.5): 
        (success,individual_new) = mutation_dollo_node_add(labels, k, individual)
        if(success):
            return (individual_new,)
        else:
            (success,individual_new) = mutation_dollo_node_remove(labels, k, individual)
            return (individual_new,)
    elif(random01 > 0.5): 
        (success,individual_new) = mutation_dollo_node_remove(labels, k, individual)
        if(success):
            return (individual_new,)
        else:
            (success,individual_new) = mutation_dollo_node_add(labels, k, individual)
            return (individual_new,)
    individual_n = copy.deepcopy( individual )
    return (False,individual_n)


def mutation_dollo_node_local_search(labels, k, individual):
    """ Mutatuion of the individual.

    Args:
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    (success,individual_new) = mutation_dollo_node_add(labels, k, individual)
    if(success):
        return (individual_new,)
    else:
        individual_n = copy.deepcopy( individual )
        return (individual_n,)
