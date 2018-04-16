# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from bitstring import BitArray
from ga_node import GaNode


# creating GA tree
root = GaNode('--', BitArray(bin = '0110000001100000'))
my1 = GaNode('A+', BitArray(bin = '0111000001100000'), parent=root)
my2 = GaNode('B+', BitArray(bin='0110100001100000'), parent=root)
# printing GA tree
root.printGaSubtree()
# rearanginig nodes
my2.parent = my1
# printing GA tree
root.printGaSubtree()

# creating new root node
my3 = GaNode('C+', BitArray(bin='0110110001100000'))
# rearanginig nodes
root.attachAsChild(my3)
# printing GA tree
root.printGaSubtree()


