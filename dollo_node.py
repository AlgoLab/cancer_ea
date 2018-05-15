"""
The :mod:`dollo_node` module contains DolloNode classes.

DolloNode class is an node of the mutation tree to be build and evaluated.
"""

import random

from ea_node import EaNode

from anytree import NodeMixin, RenderTree, PostOrderIter
from bitstring import BitArray

from collection_helpers import next_element_in_cyclic
from collection_helpers import remove_empty_set_occurences

class DolloNode(EaNode):
    """ Information about nodes of the mutattion tree, according to Dollo model.
    """
 
    def __init__(self, node_label, binary_tag, parent=None):
        """ Instance initialization.
        
         Args:
            node_label (str): Parameter `node_label`represents the label of the 
                node.
            binary_tag (:BitArray): Parameter `binary_tag` represents the
                binary number that is atached to node of the GaTree.
        """
        super(EaNode, self).__init__()
        self.node_label = node_label
        self.binary_tag = binary_tag
        self.parent = parent

    def tree_get_partition(self, partition):
        """ Function for obtaining partitions od the tree that is make by each
            of the plus nodes.
        
        Args:
            partition (dicitionary): Partition created so far.

        Returns:
            dicitionary: dictionary that have label of the plus node as key and
                a list of its partitions as value.
        """
        ret = partition
        if( self.node_label[-1]!='+' and self.node_label != "--"):
            return ret
        if( self.children is None):
            ret[self.node_label] = []
            return ret
        plus_sub_labels = self.tree_get_plus_labels_contains() 
        if( len(plus_sub_labels) == 0 
           or (len(plus_sub_labels)==1 and self.node_label in plus_sub_labels) ):
            ret[self.node_label] = []
            return ret
        l = []
        for x in self.children:
            l.append( x.tree_get_plus_labels_contains())
        ret[self.node_label] = l
        for x in self.children:
            ret = x.tree_get_partition(ret)
        ret2 = remove_empty_set_occurences(ret)
        return ret2

    def tree_initialize(self, labels, k):
        """ Function for initialization od the tree.
        
        Args:
            labels (list): Parameter `labels`represents the list of the labels
                that are given to nodes with sufix '+' or '-'.
            k (:int): Parameter `k` represents k parameter in Dollo model.            
        
        Note
            Firstly, (pseudo) randomly is decided if plus node or minus node 
            is added.
            Then, relevant node is added to the tree.

        """
        plus_not_used = set(labels)
        minus_not_used = {}
        for l in labels:
            minus_not_used[l] = k
        current_tree_size = 1
        max_size = len(labels) + int(random.random()*len(labels))  
        i=1
        while((i<= max_size) or len(plus_not_used)>0 ): 
            i += 1
            # determine the position for parent of the node to be added
            position = random.randint(0, current_tree_size)
            parent_of_leaf = self.tree_node_at_position_postorder(position)
            # determine if node will be  plus or minus
            if(random.randrange(max_size)<len(plus_not_used)):
                # plus node should be added
                # determine which label should be inserted (initially)
                label_to_insert = random.choice( labels ) 
                # prepare loop
                placed_plus_node = False
                iterations = 1
                while(not placed_plus_node and iterations <= len(labels)):
                    # check if plus node can be placed 
                    # it can be placed only if it is not placed into tree till now
                    if( not label_to_insert in plus_not_used ):
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue   
                    # plus node can be added into tree, so we are adding it
                    # create new leaf node
                    leaf_bit_array = BitArray()
                    leaf = DolloNode(label_to_insert+'+', leaf_bit_array)
                    # attach leaf node
                    parent_of_leaf.attach_child(leaf)
                    current_tree_size += 1
                    plus_not_used.discard(label_to_insert)
                    placed_plus_node = True
            else: 
                # minus node should be added
                # determine which label should be inserted (initially)
                label_to_insert = random.choice( labels ) 
                # prepare loop
                placed_minus_node = False
                iterations = 1
                while(not placed_minus_node and iterations <= len(labels)):
                    # check if minus node can be placed 
                    # it can be placed only if it is palced less than k times till now
                    if( minus_not_used[label_to_insert] <= 0 ):
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue                
                    # check if minus node can be placed on this position
                    # it can be placed only if some of his ancesstors is relevant plus node
                    anc = parent_of_leaf.tree_node_ancesstor_find(label_to_insert+'+')
                    if(anc is None):
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue
                    # check if minus node can be placed on this position
                    # it can be placed only if his parent is not is relevant plus node
                    can_be_placed = not (parent_of_leaf.node_label == label_to_insert + "+") 
                    if(not can_be_placed):
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue
                    # check if minus node can be placed on this position
                    # it can be placed only if none his ancesstors is relevant minus node
                    anc = parent_of_leaf.tree_node_ancesstor_find(label_to_insert+'-') 
                    if(not anc is None):
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue
                    # check if minus node can be placed on this position
                    # it can be placed only if label is not duplicate within siblings
                    can_be_placed = True
                    for node in parent_of_leaf.children:
                        if(node.node_label == label_to_insert):
                            can_be_placed = False
                            break
                    if(not can_be_placed):    
                        # next label should br tried
                        label_to_insert = next_element_in_cyclic(label_to_insert, labels)
                        iterations +=1
                        continue
                    # minus node can be added into tree, so we are adding it
                    # create new leaf node
                    leaf_bit_array = BitArray()
                    leaf = DolloNode(label_to_insert+'-',leaf_bit_array)
                    # attach leaf node
                    parent_of_leaf.attach_child(leaf)
                    minus_not_used[label_to_insert] -= 1
                    current_tree_size += 1
                    placed_minus_node = True 
        self.tree_compact_vertical()
        self.tree_compact_horizontal()
        self.tree_rearange_by_label()
        self.tree_set_binary_tags(labels)
        return
            
