# Nodes of the GA Tree
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from anytree import NodeMixin, RenderTree
from bitstring import BitArray


class GaNodeInfo(object):
    typeDescription = "GaNodeInfo"

class GaNode(GaNodeInfo, NodeMixin):  # Add Node feature
    
    def __init__(self, nodeLabel, binaryTag, parent=None):
        super(GaNodeInfo, self).__init__()
        self.nodeLabel = nodeLabel
        self.binaryTag = binaryTag
        self.parent = parent

    # function for printing GP subtree
    def printGaSubtree( self, endS = '\n'):
        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node.nodeLabel)
            print(treestr.ljust(8), node.binaryTag.bin )
        print(end=endS);
    
     


