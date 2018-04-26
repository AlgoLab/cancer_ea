"""
This module contains ReadInfo and ReadElement classes.

Created on Thu Apr 12 11:44:04 2018

@author: vlado.filipovic
"""


class ReadInfo(object):
    """
    Represents informations about reads.
    """
    typeDescription = "ReadInfo"


class ReadElement(ReadInfo):  
    """
    Represents one read.
    """
    
    def __init__(self, read_label, binary_read):
        """
        Instance initialization.
        """
        super(ReadInfo, self).__init__()
        self.read_label = read_label
        self.binary_read = binary_read
    
    def __repr__(self):
        """
        Obtaining represetnation of the instance.
        """
        return "%s: %s" % (self.read_label, self.binary_read.bin)
 
    def __str__(self):
        """
        Obtaining string representation of the instance.
        """
        return "%s: %s" % (self.read_label, self.binary_read.bin)
           
        
    
