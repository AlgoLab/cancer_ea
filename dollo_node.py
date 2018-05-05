"""
The :mod:`dollo_node` module contains DolloNode classes.

DolloNode class is an node of the mutation tree to be build and evaluated.
"""

import random

from ea_node import EaNode

from anytree import NodeMixin, RenderTree, PostOrderIter
from bitstring import BitArray

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
        return ret

    def tree_initialize(self, labels, k):
        """ Function for initialization od the tree.
        
        Args:
            labels (list): Parameter `labels`represents the list of the labels
                that are given to nodes with sufix '+' or '-'.
            k (:int): Parameter `k` represents k parameter in Dollo model.
        """
        plus_not_used = set(labels)
        # print( "tree_initialize", plus_not_used)
        minus_not_used = {"nothing":0}
        for l in labels:
            minus_not_used[l] = k
        current_tree_size = 1
        max_size = int((1+k-random.random())*len(labels))  
        i=1
        while((i<= max_size) or len(plus_not_used )>0 ): 
            i += 1
            # determine which label should be inserted
            label_to_insert = random.choice( labels ) 
            # determine the position for parent of the leaf node
            position = random.randint(0, current_tree_size)
            if( position == 0):
                parent_of_leaf = self
            else:
                j = 1
                for node in PostOrderIter(self):
                   if( j== position):
                       parent_of_leaf = node
                       break
                   else:
                       j += 1    
            # check if newly added label is used so far
            if( label_to_insert in plus_not_used ):
                # if not, add plus node into tree
                plus_not_used.discard(label_to_insert)
                label_to_insert += "+"
                # create new leaf node
                leaf_bit_array = BitArray()
                leaf = DolloNode(label_to_insert, leaf_bit_array)
                # attach leaf node
                parent_of_leaf.attach_child(leaf)
                current_tree_size += 1
                continue
            # label is already used, so node can only be minus node
            # check if minus node is avaliable for that label
            placed_minus_node = False
            iterations = 1
            while(not placed_minus_node and iterations <= len(labels)):
                if( minus_not_used[label_to_insert] <= 0 ):
                    # next label should br tried
                    ind = labels.index( label_to_insert )
                    ind = (ind+1)%len(labels)
                    label_to_insert = labels[ind]
                    iterations +=1
                    continue                
                # check if minus node can be placed on this position
                # it can be placed only if some of his ancesstors is relevant plus node
                can_be_placed = False
                anc = parent_of_leaf 
                while(anc != self):
                    if( anc.node_label == label_to_insert + '+'):
                        can_be_placed = True
                        break
                    else:
                        anc = anc.parent
                if(not can_be_placed):
                    # next label should br tried
                    ind = labels.index( label_to_insert )
                    ind = (ind+1)%len(labels)
                    label_to_insert = labels[ind]
                    iterations +=1
                    continue
                # check if minus node can be placed on this position
                # it can be placed only if his parent is not is relevant plus node
                can_be_placed = not (parent_of_leaf.node_label == label_to_insert + "+") 
                if(not can_be_placed):
                    # next label should br tried
                    ind = labels.index( label_to_insert )
                    ind = (ind+1)%len(labels)
                    label_to_insert = labels[ind]
                    iterations +=1
                    continue
                # check if minus node can be placed on this position
                # it can be placed only if none his ancesstors is relevant minus node
                can_be_placed = True
                anc = parent_of_leaf 
                while(anc != self):
                    if( anc.node_label == label_to_insert + '-'):
                        can_be_placed = False
                        break
                    else:
                        anc = anc.parent
                if(not can_be_placed):
                    # next label should br tried
                    ind = labels.index( label_to_insert )
                    ind = (ind+1)%len(labels)
                    label_to_insert = labels[ind]
                    iterations +=1
                    continue
                # check if minus node can be placed on this position
                # it can be placed only if label is not duplicate within children of parent
                can_be_placed = True
                for node in parent_of_leaf.children:
                    if( node.node_label == label_to_insert):
                        can_be_placed = False
                        break
                if( not can_be_placed):    
                    # next label should br tried
                    ind = labels.index( label_to_insert )
                    ind = (ind+1)%len(labels)
                    label_to_insert = labels[ind]
                    iterations +=1
                    continue
                # adding minus node on specified position
                minus_not_used[label_to_insert] -= 1
                label_to_insert += "-"
                # create new leaf node
                leaf_bit_array = BitArray()
                leaf = DolloNode(label_to_insert, leaf_bit_array)
                # attach leaf node
                parent_of_leaf.attach_child(leaf)
                current_tree_size += 1
                placed_minus_node = True 
        self.tree_compact_vertical()
        self.tree_compact_horizontal()
        self.tree_rearange_by_label()
        self.tree_set_binary_tags(labels)
        return
      
