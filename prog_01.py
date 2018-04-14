# -*- coding: utf-8 -*-
"""
Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from ga_node import GaNode

# creating GA tree
root = GaNode('--', int('01100000', 2))
my1 = GaNode('A+', int('01110000', 2), parent=root)
my2 = GaNode('B+', int('01101000', 2), parent=root)
# printing GP tree
root.printGaSubtree()
# rearanginig nodes
my2.parent = my1
# printing GP tree
root.printGaSubtree()


