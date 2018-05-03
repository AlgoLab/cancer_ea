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

    def tree_initialize(self, labels, size):
        """ Function for initialization od the tree.
        
        Args:
            labels (list): Parameter `labels`represents the list of the labels
                that are given to nodes with sufix '+' or '-'.
            size (:int): Parameter `size` represents nuber of the nodes in the 
                tree.
        """
        current_tree_size = 1
        probability_of_node_creation = 0.9
        for i in range( 2 * size ):
               if( random.random() < probability_of_node_creation):
                   # create new leaf node
                   label_to_insert = random.choice( labels ) + '+'
                   leaf_bit_array = BitArray()
                   leaf = EaNode(label_to_insert, leaf_bit_array)
                   # find the parent of the leaf node
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
                   # attach leaf node
                   parent_of_leaf.attach_child(leaf)
                   # reverse node label, if necessary
                   node = leaf.parent
                   while( node.parent != None):
                       if( leaf.node_label == node.node_label):
                           leaf.flip_node_label()
                           break
                       if( leaf.node_label[:-1] == node.node_label[:-1]):
                           break
                       node = node.parent
                   current_tree_size += 1 
                   # delete leaf is label is duplicate within siblings
                   for node in leaf.parent.children:
                       if( node.node_label == leaf.node_label and node != leaf):
                           leaf.parent = None;
                           current_tree_size -= 1
                           break
               if( i > size ):
                    probability_of_node_creation *= 0.7
        self.tree_compress_vertical()
        self.tree_compress_horizontal()
        self.tree_set_binary_tags(labels)
        return
      
    def tree_compress_horizontal(self):
        """ Horizontal compression od the tree.
        
        Whenever there are two childs of the node that have the same label, tree
        should be compresed.
        """
        print( "Tree Compress horizontal" )
        return
        
    def tree_compress_vertical(self):
        """ Vertical compression od the tree.
  
        Whenever there are parent and the child that have oposite labels, tree
        should be compresed.
        """
        print( "Tree Compress vertical" )
        #for n in self.children:
        #    for c in n.children:
        #        if( n.node_label[:-1] == c.node_label[:-1]):
        #            for x in c.children:
        #                x.parent = self
        #for n1 in self.children:
        #    for n2 in self.children:
        #        if n1.node_label == n2.node_label and n1!=n2:
        #            n2.parent = None
        #            for c in n2.children:
        #                c.parent = n1  
        #for n in self.children:
        #     n.compressTree()
        return
 
    def closest_node_in_tree( self, read ):
        """ Finds the closest node in the tree for the given read.
        
        Node is the closest according to metrics that is induced with Hamming
        distance.
        """
        closest = self
        closest_bit_array = self.binary_tag ^ read.binary_read 
        closest_distance = closest_bit_array.count(True)
        for node in PostOrderIter(self):
            current_bit_array = node.binary_tag ^ read.binary_read
            current_distance = current_bit_array.count(True)
            if( current_distance < closest_distance):
                closest = node
                closest_bit_array = current_bit_array
                closest_distance = current_distance
        return (closest, closest_distance)

