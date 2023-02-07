import path
import sys
directory = path.Path(__file__).abspath()
sys.path.append(directory.parent.parent)

from bitstring import BitArray
from anytree import RenderTree

from reads.read_element import ReadElement

import math

def matrix_inferred_E(reads,alpha,beta,individual):
    likelihood=0
    matrix_E=[]
    for read in reads:
        result={}
        for pre,_,node in RenderTree(individual):
            value=sub_evaluate(node.binary_tag.bin,read,alpha,beta)
            result[value]=node.binary_tag.bin
        max_single=max(result.keys())
        likelihood+=max_single
        matrix_E.append(result[max_single])
    return (matrix_E,)

def sub_evaluate(node,read,alpha,beta):
    likelihood=0

    for j in range(len(read.binary_read)):
        if read.binary_read.bin[j] == '0':
            if node[j] == '0':
                likelihood+=math.log(1-beta)
            elif node[j] == '1':
                likelihood+=math.log(alpha)
            elif node[j] == '-1':
                return print("error")
        elif read.binary_read.bin[j] == '1':
            if node[j] == '0':
                likelihood+=math.log(beta)
            elif node[j] == '1':
                likelihood+=math.log(1-alpha)
            elif node[j] == '-1':
                return print("error")
        elif read.binary_read.bin[j] == '2':
            likelihood+=0
    return likelihood

