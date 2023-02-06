""" script contente funzione per la generazione della matrice inferita
    in un file txt e per la generazione del formato DOT.
"""
from anytree import RenderTree

def generate_matrix(m,name_f):
    file=open(name_f,"w")
    for row in m:
        string=''
        for char in row:
            string+=char+' '
        string+='\n'
        file.write(string)
    file.close()

def label(node):
    sign=''
    label_node=''
    for char in node:
        if char=='+' or char=='-':
            sign=char
            break
        else:
            label_node+=char
    if sign =='-':
        return '" [color=indianred1, style=filled, label="'+label_node+'"];\n'
    if sign =='+':
        return '" [label="'+label_node+'"];\n'

def generate_digraph(tree,mutations,name_f):

    file=open(name_f,"w")
    file.write("digraph g { \n")
    index_parent={}
    list_tmp=[]
    node_children=[]
    for pre,_,node in RenderTree(tree):
        l=[]
        list_tmp.append(node.node_label)
        tmp=list_tmp.count(node.node_label)-1
        if not node.is_leaf:
            if node.node_label in index_parent.keys():
                for child in node.children:
                    l.append(child.node_label)
                    node_children.append(child.node_label)
                index_parent[node.node_label+str(tmp-1)]=l
            else:
                for child in node.children:
                    if child.node_label in list_tmp:
                        l.append(child.node_label+str(tmp))
                        node_children.append(child.node_label
                        +str(tmp))
                    elif child.node_label in node_children:
                        l.append(child.node_label+str(tmp-1))
                        node_children.append(child.node_label
                        +str(tmp-1))
                    else:
                        l.append(child.node_label)
                        node_children.append(child.node_label)
                if node.node_label+str(tmp-1) in node_children:
                    index_parent[node.node_label+str(tmp-1)]=l
                else:
                    index_parent[node.node_label]=l
    count=0
    dic_enum={}
    for element in index_parent.keys():
        if not element in dic_enum.keys():
            dic_enum[element]=count
            count+=1
        for val in index_parent[element]:
            if not val in dic_enum.keys():
                dic_enum[val]=count
                count+=1
    for key in index_parent.keys():
        for val in index_parent[key]:
            file.write("    "+'"'+str(dic_enum[key])+'" -> "'
            +str(dic_enum[val])+'";\n')
            file.write("    "+'"'+str(dic_enum[val])+label(val))
        
        
    file.write("    "+'"'+'0'+'" [label="germline"];\n')
    file.write("}")
    file.close()
