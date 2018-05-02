"""
The :mod:`dollo_node` module contains DolloNode classes.

DolloNode class is an node of the mutation tree to be build and evaluated.
"""

import random

from ea_node import EaNode

from anytree import NodeMixin, RenderTree, PostOrderIter
from bitstring import BitArray

class DolloNodeInfo(EaNode):
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
        super( self, node_label, binary_tag).__init__()

