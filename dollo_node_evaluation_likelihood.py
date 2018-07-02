"""Questo modulo contiene le funzioni per il calcolo della funzione likelihood,
   evaluate_dollo_node_Evaluation e' la funzione principale e 
   sub evaluation e' la sotto funzione che prende una riga della matrice
   e il profilo genetico di un nodo.
   final matrix restituisce la matrice inferita E associata al valore likelihood di un albero
"""
  
from bitstring import BitArray
from anytree import RenderTree
from read_element import ReadElement
import math

matrix_inferita1={}

def evaluate_dollo_node_direct1(reads,alpha,beta,individual):

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
    matrix_inferita1[likelihood]=matrix_E
    return (likelihood,matrix_E)


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
    
def final_matrix(likelihood):
    if likelihood in matrix_inferita.keys():
        return matrix_inferita[likelihood]
