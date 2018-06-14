""" The :mod:`dollo_node_crossover_operators` module contains operators
for crossover of DolloNode individuals.

"""
import copy
import random

from anytree import search

from collection_helpers import index_of_largest_set_in_list
from collection_helpers import intersection_list_dictionary
from collection_helpers import next_element_in_cyclic

from dollo_node_helpers import dollo_subtree_add_correct_minus_node


def dollo_node_exchange_subtrees(individual1, individual2, labels, dollo_k):
    """ Exchanginig between two individuals, by exchanging its subtrees

    Args:
        individual1 (DolloNode): first individual in crossover.
        individual2 (DolloNode): second individual in crossover.
        labels (list): list of the lables of the nodes that exists in the tree.
     
    Returns:            
        pair where the first componet is indicator of succes and the second is
        individual that is mutated e.g. output of the mutation process.
    
    Notes:
        Subtrees that are exchanged should cover same plus nodes and subtrees 
        should not be same.
        Minus nodes will be set after exchanging.
    """
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    part1 = {}
    part1 = individual1.tree_get_partition(part1)
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    part2 = {}
    part2 = individual2.tree_get_partition(part2)
    #print("*************************************************")
    #print("* dollo_node_exchange_subtrees:                 *")
    #print(" partitions:")
    #print(individual1)
    #print(part1)
    #print(individual2)
    #print(part2)
    #print("* dollo_node_exchange_subtrees:                 *")
    #print("*************************************************")
    ret = False
    random_label = random.choice(labels)
    iteration = 1
    while(iteration<=len(labels)):
        lab_plus = random_label + '+'
        if(not lab_plus in part1):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        if(not lab_plus in part2):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        intersection = intersection_list_dictionary(part1[lab_plus],part2,lab_plus)
        if(len(intersection)==0):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        #print("*************************************************")
        #print("* dollo_node_exchange_subtrees:                 *")
        #print(" label:", lab_plus)
        #print(" intersection:", intersection)
        #print("* dollo_node_exchange_subtrees:                 *")
        #print("*************************************************")
        node1_label = lab_plus
        ind_max = index_of_largest_set_in_list(intersection)
        if(ind_max < 0):
            continue
        (node2_label, intersection_set) = intersection[ind_max]            
        node1 = individual1.tree_node_find(node1_label)
        node2 = individual2.tree_node_find(node2_label)
        #print("*************************************************")
        #print("* dollo_node_exchange_subtrees:                 *")
        #print(" node1")
        #print(node1)
        #print(" node2")
        #print(node2)
        #print("* dollo_node_exchange_subtrees:                 *")
        #print("*************************************************")
        # find roots of subrees
        label_in_subtree = next(iter(intersection_set))
        subnode1 = individual1.tree_node_find(label_in_subtree)
        while( not (subnode1.parent == node1) ):
            subnode1 = subnode1.parent
        subnode2 = individual2.tree_node_find(label_in_subtree)
        while( not (subnode2.parent == node2) ):
            subnode2 = subnode2.parent
        #print("*************************************************")
        #print("* dollo_node_exchange_subtrees:                 *")
        #print(" subnode1")
        #print(subnode1)
        #print(" subnode2")
        #print(subnode2)
        #print("* dollo_node_exchange_subtrees:                 *")
        #print("*************************************************")
        # check if subtrees are equal
        if(subnode1.tree_is_equal(subnode2)):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        # exchange subtrees
        subnode1.parent = node2
        subnode2.parent = node1
        # Compaction and regularization in subtree roted with node1
        num_removed = subnode1.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            dollo_subtree_add_correct_minus_node(subnode1,labels,dollo_k)
         # Compaction and regularization in subtree roted with node2
        num_removed = subnode2.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            dollo_subtree_add_correct_minus_node(subnode2,labels,dollo_k)
        individual1.tree_compact_vertical()
        individual1.tree_compact_horizontal()
        individual1.tree_rearange_by_label()
        individual1.tree_set_binary_tags(labels)
        individual2.tree_compact_vertical()
        individual2.tree_compact_horizontal()
        individual2.tree_rearange_by_label()
        individual2.tree_set_binary_tags(labels)
        ret = True
        break
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    return (ret,individual1,individual2)


def dollo_node_exchange_parent_indices(individual1, individual2, labels, dollo_k):
    """ Excanging between two individuals, by restructuring upon parent indices
    of the another indivirual. 
    
    Args:
        individual1 (DolloNode): first individual in exchanging.
        individual2 (DolloNode): second individual in exchanging.
        labels (list): list of the lables of the nodes that exists in the tree.
        dollo_k (int): parametar k in Dollo model
     
    Returns:            
        triple where the first componet is indicator of succes and the second 
        and third are resulted individuals after exchanging.    
     """
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    random_label = random.choice(labels)
    ret = False
    iteration = 1
    while(iteration<=len(labels)):
        plus_label = random_label + '+'
        node1 = individual1.tree_node_find(plus_label)
        if(node1 is None):
            raise ValueError("Error: This shouldn't happend!\n",
                             "plusabel: ", plus_label, "\n",
                             "tree: \n", individual1, "\n",
                             "labels: ", labels)
        node2 = individual2.tree_node_find(plus_label)
        if(node2 is None):
            raise ValueError("Error: This shouldn't happend!\n",
                             "plusabel: ", plus_label, "\n",
                             "tree: \n", individual2, "\n",
                             "labels: ", labels)
        # obtain the most inner plus parrent of node1 
        n1_pn = node1.parent
        while( not (n1_pn is None) and n1_pn.node_label[-1] != '+' ):
            n1_pn = n1_pn.parent
        # obtain the most inner plus parrent of node2 
        n2_pn = node2.parent
        while( not (n2_pn is None) and n2_pn.node_label[-1] != '+' ):
            n2_pn = n2_pn.parent
        # if labels of plus parents are the same, then there is no need for crossover 
        if( n1_pn is None or n2_pn is None or n1_pn.node_label==n2_pn.node_label):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue            
        # if parent in one tree exists among descendants in another, then crossover is impossible 
        problem_child_1 = node1.tree_node_find(n2_pn.node_label)
        problem_child_2 = node2.tree_node_find(n1_pn.node_label)
        if((not problem_child_1 is None)or(not problem_child_2 is None)):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue            
        #print("************************************************************")
        #print("* dollo_node_exchange_parent_indices: label selected       *")
        #print(plus_label)
        #print("1: ", individual1)
        #print("2: ", individual2)
        #print("* dollo_node_exchange_parent_indices: label selected       *")
        #print("************************************************************")            
        # redefine edges
        if( not node2.parent is None ):
            new_parent_1 = individual1.tree_node_find(n2_pn.node_label)
        else:
            new_parent_1 = individual1
        if( not node1.parent is None ):
            new_parent_2 = individual2.tree_node_find( n1_pn.node_label)
        else:
            new_parent_2 = individual2
        # do the switch
        node1.parent = new_parent_1
        node2.parent = new_parent_2
        num_removed = node1.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            dollo_subtree_add_correct_minus_node(node1,labels, dollo_k)
        num_removed = node2.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            dollo_subtree_add_correct_minus_node(node2, labels, dollo_k)
        individual1.tree_compact_vertical()
        individual1.tree_compact_horizontal()
        individual1.tree_set_binary_tags(labels)
        individual1.tree_rearange_by_label()
        individual2.tree_compact_vertical()
        individual2.tree_compact_horizontal()
        individual2.tree_rearange_by_label()
        individual2.tree_set_binary_tags(labels)
        #print("************************************************************")
        #print("* dollo_node_exchange_parent_indices: after switch         *")
        #print("1: ", individual1)
        #print("2: ", individual2)
        #print("* dollo_node_exchange_parent_indices: after switch         *")
        #print("************************************************************")                               
        ret = True
        break
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    return (ret,individual1,individual2)

          
def crossover_dollo_node_exchange_subtrees(labels,dollo_k,individual1,individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         labels (list): list of the lables of the nodes that exists in the tree.
         dollo_k (int): parametar k in Dollo model
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
         dollo_k (int): parametar k in Dollo model
    
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    if(individual1.tree_is_equal(individual2)):
        return(individual1,individual2)
    (success,individual1,individual2) = dollo_node_exchange_subtrees(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1,individual2,)
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    return (individual1,individual2)


def crossover_dollo_node_exchange_parent_indices(labels,dollo_k,individual1,individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         labels (list): list of the lables of the nodes that exists in the tree.
         dollo_k (int): parametar k in Dollo model
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    if(individual1.tree_is_equal(individual2)):
         return(individual1,individual2)
    (success,individual1,individual2) = dollo_node_exchange_parent_indices(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1,individual2,)
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    return (individual1,individual2)


def crossover_dollo_node_combined(labels,dollo_k,individual1,individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         labels (list): list of the lables of the nodes that exists in the tree.
         dollo_k (int): parametar k in Dollo model
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    if(individual1.tree_is_equal(individual2)):
        return(individual1,individual2)
    (success,individual1,individual2) = dollo_node_exchange_subtrees(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1,individual2,)
    (success,individual1,individual2) = dollo_node_exchange_parent_indices(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1,individual2,)
    #if(not individual1.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual1: \n", individual1) 
    #if(not individual2.is_correct(labels, dollo_k)):
    #    raise ValueError("Error! \n inidividual2: \n", individual2) 
    return (individual1,individual2)

