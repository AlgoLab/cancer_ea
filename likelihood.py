
from anytree import RenderTree
from bitstring import BitArray

import math

def evaluate(tree,rows_matrix,alpha,beta):
        leafs=[]
        cont=0
        for row in rows_matrix:
                result={}
                likelihood=0
                for pre,_,node in RenderTree(tree):
                        result[sub_evaluate(node.binary_tag.bin,row,alpha,beta)]=node
                likelihood+=max(result.keys())
                leafs.append((result[likelihood],"s"+str(cont),likelihood))
                cont+=1

        likelihood_tree=0
        for leaf in leafs:
                likelihood_tree+=leaf[2]
        return (leafs,likelihood_tree)

def sub_evaluate(node,row_matrix,alpha,beta):
        likelihood=0
        for j in range(len(row_matrix)):
                if row_matrix[j] == '0':
                        if node[j] == '0':
                                likelihood+=math.log(1-beta)
                        elif node[j] == '1':
                                likelihood+=math.log(alpha)
                        elif node[j] == '-1':
                                return print("error")
                elif row_matrix[j] == '1':
                        if node[j] == '0':
                                likelihood+=math.log(beta)
                        elif node[j] == '1':
                                likelihood+=math.log(1-alpha)
                        elif node[j] == '-1':
                                return print("error")
                elif row_matrix[j]== '2':
                        likelihood+=0

        return likelihood
