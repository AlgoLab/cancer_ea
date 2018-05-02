""" The :mod:`read_element` module contains ReadInfo and ReadElement classes.

"""


class ReadInfo(object):
    """ Represents informations about reads.
    
    """
    typeDescription = "ReadInfo"


class ReadElement(ReadInfo):  
    """ Represents one read.
    """
    
    def __init__(self, read_label, binary_read):
        """ Instance initialization.
        
         Args:
            read_label (str): Parameter `read_label`represents the label of the 
                read.
            binary_read (:BitArray): Parameter `binary_read` represents the
                binary number that indicate which mutation occures.
        """
        super(ReadInfo, self).__init__()
        self.read_label = read_label
        self.binary_read = binary_read
    
    def __repr__(self):
        """ Obtaining representation of the instance.
      
        Returns:
            str: Representation of the instance.
        """
        return "%s: %s" % (self.read_label, self.binary_read.bin)
 
    def __str__(self):
        """ Obtaining string representation of the instance.

        Returns:
            str: String representation of the instance.
        """
        return "%s: %s" % (self.read_label, self.binary_read.bin)
           
        
    
