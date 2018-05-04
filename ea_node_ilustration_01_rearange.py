""" The :mod:`ea_node_ilustration_01` module contains an example how to use 
methods from EaNode class.

"""

from bitstring import BitArray

from ea_node import EaNode


def main():
    """ This function is an entry  point of the application.
    """
    # creating GA tree
    root = EaNode('--', BitArray(bin = '0110000001100000'))
    my1 = EaNode('A+', BitArray(bin = '0111000001100000'), parent=root)
    my2 = EaNode('B+', BitArray(bin='0110100001100000'), parent=root)
    # printing GA tree
    root.tree_print()
    # rearanginig nodes
    my2.parent = my1
    # printing GA tree
    root.tree_print()
    
    # creating new root node
    my3 = EaNode('C+', BitArray(bin='0110110001100000'))
    # rearanginig nodes
    root.attach_child(my3)
    # printing GA tree
    root.tree_print()
    return


# this means that if this script is executed, then 
# main() will be executed
if __name__ == "__main__":
    main()



