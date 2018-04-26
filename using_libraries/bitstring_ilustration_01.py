"""
This module contains an example how to use bitstring
library.

Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""

from bitstring import BitArray

a = BitArray(bin='00101')
b = BitArray(bin='10101')

print(a)
print(b)