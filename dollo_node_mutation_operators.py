""" The :mod:`dollo_node_mutation_operators` module contains operators
for mutation of DolloNode individuals.

"""
import copy
import random

from bitstring import BitArray

from anytree import search

from dollo_node import DolloNode

from dollo_node_helpers import dollo_subtree_add_correct_minus_node

def mutation_dollo_node_add(labels,dollo_k,individual):
    """ Mutation of the individual, by randomly adding one node

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
         individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    #print("************************************************************")
    #print("* mutation_dollo_node_add                                  *")
    #print(" at begin: ",individual)
    #print("* mutation_dollo_node_add:                                 *")
    #print("************************************************************")                               
    random01 = random.random()
    label_is_plus = random01 < (len(labels)/float(1+len(individual.descendants)) ) 
    if(label_is_plus):
        # adding plus label and removing same plus label
        random_parent = random.choice(individual.descendants)
        random_label = random.choice(labels)
        while( random_label + '+' == random_parent.node_label ):
            random_label = random.choice(labels)
        #print("random_parent: ", random_parent, "\n")
        #print("random_label: ", random_label, "\n")
        # remove old plus node
        old_plus_node = individual.tree_node_find(random_label+'+')
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
            dollo_subtree_add_correct_minus_node(individual, labels, dollo_k)
    else:
        # adding minus label and removing same plus label
        dollo_subtree_add_correct_minus_node(individual,labels,dollo_k)
    individual.tree_compact_vertical()
    individual.tree_compact_horizontal()
    individual.tree_rearange_by_label()
    individual.tree_set_binary_tags(labels)
    #print("************************************************************")
    #print("* mutation_dollo_node_add                                  *")
    #print("at end: ",individual)
    #print("* mutation_dollo_node_add:                                 *")
    #print("************************************************************")                               
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    return (True,individual)

def mutation_dollo_node_remove(labels, dollo_k, individual):
    """ Mutation of the individual, by randomly removing one node

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    #print("************************************************************")
    #print("* mutation_dollo_node_remove                               *")
    #print("at start: ",individual)
    #print("* mutation_dollo_node_remove                               *")
    #print("************************************************************")                               
    random_node = random.choice(individual.descendants)
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
        # print(individual_n)
        # create new plus node and attach it
        parent_of_new_node = random.choice(individual.descendants)
        new_bit_array = BitArray()
        new_node = DolloNode(random_label+'+',new_bit_array)
        parent_of_new_node.attach_child(new_node)
        for i in range(0,num_removed-1):
            dollo_subtree_add_correct_minus_node(parent_of_new_node, labels, dollo_k)
    individual.tree_compact_vertical()
    individual.tree_compact_horizontal()
    individual.tree_rearange_by_label()
    individual.tree_set_binary_tags(labels)
    #print("************************************************************")
    #print("* mutation_dollo_node_remove                               *")
    #print("at end: ",individual_n)
    #print("* mutation_dollo_node_remove                               *")
    #print("************************************************************")                               
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    return (True,individual)

def mutation_dollo_node_promote(labels, dollo_k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        up to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    return (False,individual)


def mutation_dollo_node_demote(labels, dollo_k, level, individual):
    """ Mutation of the individual, by randomly randomly selected node
        down to the tree for given level.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
        level (int): level for move
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    return (False,individual)


def mutation_dollo_node_combine(labels, dollo_k, individual):
    """ Mutatuion of the individual.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    random01 = random.random()
    if(random01 <= 0.5): 
        (success,individual) = mutation_dollo_node_add(labels, dollo_k, individual)
        if(success):
            return (individual,)
        else:
            (success,individual) = mutation_dollo_node_remove(labels, dollo_k, individual)
            return (individual,)
    elif(random01 > 0.5): 
        (success,individual) = mutation_dollo_node_remove(labels, dollo_k, individual)
        if(success):
            return (individual,)
        else:
            (success,individual) = mutation_dollo_node_add(labels, dollo_k, individual)
            return (individual,)
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    return (individual)


def mutation_dollo_node_local_search(labels, dollo_k, individual):
    """ Mutatuion of the individual.

    Args:
        labels (list): list of the lables of the nodes in the tree that should 
            be initialized.
        dollo_k(int): Value od the Dollo k parameter.
        individual (DolloNode): individual that will be mutated.
     
    Returns:            
        tuple where the first elelemt is mutataed e.g. output of the
        mutation process.
    """
    if(not individual.is_correct(labels, dollo_k)):
        raise ValueError("Error! \n inidividual: \n", individual) 
    (success,individual) = mutation_dollo_node_add(labels, dollo_k, individual)
    if(success):
        if(not individual.is_correct(labels, dollo_k)):
            raise ValueError("Error! \n inidividual: \n", individual) 
        return (individual,)
    else:
        if(not individual.is_correct(labels, dollo_k)):
            raise ValueError("Error! \n inidividual: \n", individual) 
        return (individual,)
