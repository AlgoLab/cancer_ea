""" This module contains an example how to use bitstring
library.

"""

from bitstring import BitArray

def main():
    """ This function is an entry  point of the application.
    """
    a = BitArray(bin='00101')
    b = BitArray(bin='10101')
    
    print(a)
    print(b)
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == "__main__":
    main()
