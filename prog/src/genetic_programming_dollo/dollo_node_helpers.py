""" The :mod:`dollo_node_helpers` module contains helper functions
for DolloNode individuals.

"""

import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

import random

from bitstring import BitArray

from anytree import search

from dollo_node.dollo_node import DolloNode

from utils.collections import next_element_in_cyclic

def dollo_subtree_add_correct_minus_node(subtree, labels, dollo_k):
    """ Adds correct minus node into tree rooted with self. 

    Args:
        labels (list): list of the lables of the nodes that exists in the tree.
        dollo_k (int): parametar k in Dollo model

    Note: 
        If tree is too small, then minus node can not be added.    
    """
    if( subtree.depth <= 1):
        return
    position_num = random.randint(0, subtree.tree_size())
    position_node = subtree.tree_node_at_position_postorder(position_num)            
    random_label = random.choice(labels)
    iteration = 1
    while(iteration<=len(labels)):
        # check if exists relevant plus node
        position_parent = subtree.tree_node_find(random_label+'+')
        if( position_parent is None):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue       
        # check if direct parent of new minus node that should be addes is relevant plus node
        if( position_node.node_label == random_label+'+'):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue
        # count if overall number of that minus label is already dollo_k
        subtree_root = subtree.root
        nodes = subtree_root.tree_node_find_all(random_label+'-')
        if( len(nodes) >= dollo_k):
            iteration += 1
            random_label = next_element_in_cyclic(random_label, labels)
            continue               
        # create and attach leaf node
        leaf_bit_array = BitArray()
        leaf = DolloNode(random_label+'-',leaf_bit_array)
        position_node.attach_child(leaf)
        position_node.tree_compact_vertical()
        position_node.tree_compact_horizontal()
        position_node.tree_rearrange_by_label()
        return
    return

