""" The :mod:`dollo_node_crossover_operators` module contains operators
for crossover of DolloNode individuals.

"""
import copy
import random

from anytree import search

from collection_helpers import next_element_in_cyclic
from collection_helpers import set_in_both_lists



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
    individual1_n = copy.deepcopy(individual1)
    individual2_n = copy.deepcopy(individual2)
    random_label = random.choice(labels)
    exchange_executed =  False
    iteration = 1
    while(not exchange_executed and iteration<=len(labels)):
        plus_label = random_label + '+'
        node1 = search.find(individual1_n,lambda node: node.node_label == plus_label)
        node2 = search.find(individual2_n,lambda node: node.node_label == plus_label)
        # if labels of parents are the same, then there is no need for crossover 
        if(node1.parent.node_label==node2.parent.node_label):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue            
        # if parent in one tree exists among descendants in another, then crossover is impossible 
        problem_child_1 = search.find(node1,lambda node: node.node_label == node2.parent.node_label)
        problem_child_2 = search.find(node2,lambda node: node.node_label == node1.parent.node_label)
        if((not problem_child_1 is None)or(not problem_child_2 is None)):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue            
        #print("************************************************************")
        #print("* dollo_node_exchange_parent_indices: label selected       *")
        #print(plus_label)
        #print("1: ", individual1_n)
        #print("2: ", individual2_n)
        #print("* dollo_node_exchange_parent_indices: label selected       *")
        #print("************************************************************")            
        # redefine edges
        if( not node2.parent is None ):
            new_parent_1 = search.find(individual1_n,lambda node: node.node_label == node2.parent.node_label)
        else:
            new_parent_1 = individual1_n
        if( not node1.parent is None ):
            new_parent_2 = search.find(individual2_n,lambda node: node.node_label == node1.parent.node_label)
        else:
            new_parent_2 = individual2_n
        # do the switch
        node1.parent = new_parent_1
        node2.parent = new_parent_2
        num_removed = node1.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            node1.add_correct_minus_node(labels, dollo_k)
        node1.tree_compact_vertical()
        node1.tree_compact_horizontal()
        node1.tree_rearange_by_label()
        num_removed = node2.tree_remove_incorrect_minus_nodes()
        for i in range(0,num_removed):
            node2.add_correct_minus_node(labels, dollo_k)
        node2.tree_compact_vertical()
        node2.tree_compact_horizontal()
        node2.tree_rearange_by_label()
        print("************************************************************")
        print("* dollo_node_exchange_parent_indices: after switch         *")
        print("1: ", individual1_n)
        print("2: ", individual2_n)
        print("* dollo_node_exchange_parent_indices: after switch         *")
        print("************************************************************")                        
        # remove or change incorrect minus nodes within node1 and node2            
        exchange_executed = True
    return (exchange_executed,individual1_n,individual2_n)

          
def dollo_node_exchange_subtrees(individual1, individual2, labels):
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
    individual1_n = copy.deepcopy( individual1 )
    individual2_n = copy.deepcopy( individual2 )
    part1 = {}
    part1 = individual1_n.tree_get_partition(part1)
    part2 = {}
    part2 = individual2_n.tree_get_partition(part2)
    print("*************************************************")
    print("* DolloNode.exchange_subtrees: partitions       *")
    print(individual1_n)
    print(part1)
    print(individual2_n)
    print(part2)
    print("* DolloNode.exchange_subtrees: partitions *")
    print("*************************************************")
    ret = False
    random_label = random.choice(labels)
    crossover_executed =  False
    iteration = 1
    while(not crossover_executed and iteration<=len(labels)):
        lab_plus = random_label + '+'
        if(not lab_plus in part1):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        if(not lab_plus in part2):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        common_set = set_in_both_lists(part1[lab_plus],part2[lab_plus])
        if(len(common_set)==0):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        else:
            print("*************************************************")
            print("* DolloNode.exchange_subtrees:                  *")
            print("label: ", lab_plus)
            print("common set: ", common_set)
            print("* DolloNode.exchange_subtrees:                  *")
            print("*************************************************")            
        node1 = search.find(individual1_n,lambda node: node.node_label == lab_plus)
        node2 = search.find(individual2_n,lambda node: node.node_label == lab_plus)
        if(node1.tree_is_equal(node2)):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        # exchange subtrees
        parent1 = node1.parent
        parent2 = node2.parent
        node1.parent = parent2
        node2.parent = parent1
        # Compaction and regularization in subtree roted with node1
        node1.tree_remove_incorrect_minus_nodes()
        node1.tree_compact_vertical()
        node1.tree_compact_horizontal()
        node1.tree_rearange_by_label()
        node1.tree_set_binary_tags(labels)
        # Compaction and regularization in subtree roted with node2
        node2.tree_remove_incorrect_minus_nodes()
        node2.tree_compact_vertical()
        node2.tree_compact_horizontal()
        node2.tree_rearange_by_label()
        node2.tree_set_binary_tags(labels)
        ret = True
        break
    if(ret):
        print("***********************************************")
        print("* DolloNode.exchange_subtrees: succesed       *")
        print("***********************************************")
    else:
        print("***********************************************")
        print("* DolloNode.exchange_subtrees: failed         *")
        print("***********************************************")
    return (ret,individual1_n,individual2_n)


def crossover_dollo_node_exchange_parent_indices(labels,dollo_k,individual1,individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         labels (list): list of the lables of the nodes that exists in the tree.
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
         dollo_k (int): parametar k in Dollo model
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    print("* Executing crossover step *")
    if(individual1.tree_is_equal(individual2)):
        print("* Crossover: both individuals are same *")
        individual1_new = copy.deepcopy( individual1 )
        individual2_new = copy.deepcopy( individual2 )
        return(individual1_new,individual2_new)
    (success,individual1_new,individual2_new) = dollo_node_exchange_parent_indices(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1_new,individual2_new,)
    individual1_new = copy.deepcopy( individual1 )
    individual2_new = copy.deepcopy( individual2 )
    return (individual1_new,individual2_new)



def crossover_dollo_node_combined(labels,dollo_k,individual1,individual2):
    """ Crossover between individual1 and individual2.
    
    Args:
         labels (list): list of the lables of the nodes that exists in the tree.
         individual1 (DolloNode): first individual in crossover.
         individual2 (DolloNode): second individual in crossover.
         dollo_k (int): parametar k in Dollo model
     
    Returns:            
        two-element tuple which contains offsprings e.g. output of the
        crossover process.
    """
    print("* Executing crossover step *")
    if(individual1.tree_is_equal(individual2)):
        print("* Crossover: both individuals are same *")
        individual1_new = copy.deepcopy( individual1 )
        individual2_new = copy.deepcopy( individual2 )
        return(individual1_new,individual2_new)
    (success,individual1_new,individual2_new) = dollo_node_exchange_subtrees(
            individual1, individual2, labels)
    if(success):
        return (individual1_new,individual2_new,)
    (success,individual1_new,individual2_new) = dollo_node_exchange_parent_indices(
            individual1, individual2, labels, dollo_k)
    if(success):
        return (individual1_new,individual2_new,)
    individual1_new = copy.deepcopy( individual1 )
    individual2_new = copy.deepcopy( individual2 )
    return (individual1_new,individual2_new)

