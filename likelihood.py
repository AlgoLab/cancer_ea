#node : Node('/root/ST13/ASNS/DNAJC17/MLL3')
#individual : ['2', '1', '2', '2', '2', '2', '1', '0', '2', '2', '2', '0', '0', '0', '2', '1', '2', '2']
import math
from anytree import Node 

mutations =['PDE4DIP', 'NTRK1', 'SESN2', 'ARHGAP5', 'DNAJC17', 
			'USP32', 'ANAPC1', 'RETSAT', 'ST13', 'DLEC1', 'FRG1', 'DMXL1', 
			'FAM115C', 'MLL3', 'ABCB5', 'ASNS', 'PABPC1', 'TOP1MT']

def path(node):
		array=[]
		antenati=node.ancestors
		#list of mutations in the node path
		m=[]
		m.append(node.name)
		for i in antenati:
			m.append(i.name)
		for j in mutations:
			if (j in m) and not("-"+j in m):
				array.append(1)
			elif "-"+j in m and j in m:
				array.append(0)
			elif "-"+j in m and not(j in m):
				array.append(-1)
			else :
				array.append(0)
		return array
# array : [0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0]

alfa=0.15
beta=0.001
def evaluate(individual,node):
		likelihood=0
		path_node=path(node)
		for j in range(len(individual)):
			if individual[j] == '0':
				if path_node[j] == 0:
					likelihood+=math.log10(1-beta)
				elif path_node[j] == 1:
					likelihood+=math.log10(beta)
				elif path_node[j] == -1:
					return print("error")
			elif individual[j] == '1':
				if path_node[j] == 0:
					likelihood+=math.log10(1-alfa)
				elif path_node[j] == 1:
					likelihood+=math.log10(alfa)
				elif path_node[j] == -1:
					return print("error")
			elif individual[j]== '2':
				likelihood+=0
        return likelihood