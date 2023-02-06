""" This module module contains an example how to use 
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
    # rearanginig nodes
    my2.parent = my1
    
    # creating new root node
    my3 = EaNode('C+', BitArray(bin='0110110001100000'))
    # rearanginig nodes
    root.attach_child(my3)

    print("==========================================")
    root.tree_print()
    my2.tree_print()
    print( root.tree_is_equal(my2)) 
    print( my2.tree_is_equal(root)) 

    my4 = EaNode('C+', BitArray(bin='0110110001100000'))

    print("==========================================")
    my3.tree_print()
    my4.tree_print()
    print( my4.tree_is_equal(my3)) 
    print( my3.tree_is_equal(my4)) 
 
    my5 = EaNode('--', BitArray(bin = '0110000001100000'))
    my6 = EaNode('A+', BitArray(bin = '0111000001100000'), parent=my5)
    my7 = EaNode('B+', BitArray(bin='0110100001100000'), parent=my6)
    my4.parent = my5

    print("==========================================")
    root.tree_print()
    my5.tree_print()
    print( root.tree_is_equal(my5)) 
    print( my5.tree_is_equal(root))   
    return


# this means that if this script is executed, then 
# main() will be executed
if __name__ == "__main__":
    main()



