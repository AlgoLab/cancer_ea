# Nodes of the GA Tree
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

import random

from anytree import NodeMixin, RenderTree, PostOrderIter

from bitstring import BitArray

def flip(label):
    if(label.endswith('+')):
        return label.replace('+', '-')
    elif(label.endswith('+')): 
        return label.replace('-', '+')
    return label

def count(collection):
    i=0
    for node in collection:
        i+=1
    return i


class GaNodeInfo(object):
    typeDescription = "GaNodeInfo"

class GaNode(GaNodeInfo, NodeMixin):  # Add Node feature
    
    def __init__(self, nodeLabel, binaryTag, parent=None):
        super(GaNodeInfo, self).__init__()
        self.nodeLabel = nodeLabel
        self.binaryTag = binaryTag
        self.parent = parent

    # function for printing GA subtree
    def printGaSubtree( self, endS = '\n'):
        for pre, _, node in RenderTree(self):
            treestr = u"%s%s" % (pre, node.nodeLabel)
            print(treestr.ljust(8), node.binaryTag.bin )
        print(end=endS)
        return
    
    # function for adding child GA node
    def attachAsChild( self, child):
        child.parent = self
        return

    # initialization od the tree
    def initializeSubtree(self, labels, size):
           currentTreeSize = 1
           probabilityOfNodeCreation = 0.9
           for i in range(2 * size):
               if( random.random() < probabilityOfNodeCreation):
                   # create new leaf node
                   labelToInsert = random.choice( labels ) + '+'
                   leafBitArray = BitArray()
                   leaf = GaNode(labelToInsert, leafBitArray)
                   # find the parent of the leaf node
                   position = random.randint(0, currentTreeSize)
                   if( position == 0):
                       parentOfLeaf = self
                   else:
                       j = 1
                       for node in PostOrderIter(self):
                           if( j== position):
                               parentOfLeaf = node
                               break
                           else:
                               j += 1    
                   # attach leaf node
                   leaf.parent = parentOfLeaf
                   leaf.binaryTag.append( leaf.parent.binaryTag )
                   indexBit = count( leaf.parent.children ) - 1
                   #print("#", indexBit)
                   #indexBit = leaf.binaryTag.find(False, start = indexBit)
                   #print("#", indexBit)
                   leaf.binaryTag.invert(indexBit)
                   node = leaf.parent
                   # reverse mutation label, if necessary
                   while( node.parent != None):
                       if( leaf.nodeLabel == node.nodeLabel):
                           leaf.nodeLabel = flip(leaf.nodeLabel)
                           break
                       node = node.parent
                   currentTreeSize += 1 
                   # delete leaf is label is duplicate
                   for node in leaf.parent.children:
                       if( node.nodeLabel == leaf.nodeLabel and node != leaf):
                           leaf.parent = None;
                           currentTreeSize -= 1
                           break
               if( i > size ):
                    probabilityOfNodeCreation *= 0.6
 

         
