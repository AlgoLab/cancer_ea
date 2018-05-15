""" The :mod:`collection_helpers` module contains  contains helper functions 
for collection.

"""


def count(collection):
    """ Helper function that count elements in collection.
    """
    i=0
    for node in collection:
        i+=1
    return i


def index_of(collection, element, start=0):
    """ Helper function that fids a postion of the element in collection.
    
    Search in this fuction is executed from the begining toward end.
    """
    for i in range(start, collection.length):
        if( i < start ):
            continue;
        if( collection[i]==element):
            return i;
    return -1

def last_index_of(collection, element):
    """     Helper function that fids a postion of the element in collection.
    
    Search in this fuction is executed from the end toward begining.
    """
    for i in range(collection.length-1, -1, -1):
        if( collection[i]==element):
            return i;
    return -1

def next_element_in_cyclic(element, collection):
        """     Helper function that fids next element in collection. Next 
                element for the last element is the first one in collection. 
    
        Returns: next element in collection. If element is not in collection, 
        function will return None. 
        """
        ind = collection.index(element)
        if(ind<0):
            return None
        ind = (ind+1)%len(collection)
        return collection[ind]


def sets_are_equal(set1,set2):
    """ Checks if sets are equal

    Args:
        set1 (set): first set for comparison.
        set2 (set): second set for comparison.
     
    Returns:            
        boolean that indicate equality of the sets
    """
    for x in set1:
        if( not x in set2):
            return False;
    for x in set2:
        if( not x in set1):
            return False;
    return True


def set_in_both_lists(list1, list2):
    """ Checks if two lists are containing the same set

    Args:
        list1 (list): first list for check.
        list2 (list): second list for check.
     
    Returns:            
        set that is common for both lists. Empty set if there is no common 
        elements.
    """
    intersect = set()
    for s1 in list1:
        for s2 in list2:
            if(len(s1)>0 and len(s2)>0 and sets_are_equal(s1, s2)):
                if( len(s1)>len(intersect)):
                    intersect = s1
    return intersect
    

def set_consits_of_plus_lebels(list_of_sets):
    """ Ironing the list of sets and keeping only plus nodes.

    Args:
        list_of_sets (list): list of the set that is to be searched.
     
    Returns:            
        set of the plus labels in list
    """
    ret = {*[]}
    for s in list_of_sets:
        for x in s:
            if(x[-1]=='+'):
                ret.add(x)
    return ret


def remove_empty_set_occurences(original):
    """ Creating dictionary where all empty sets occurences are removed.

    Args:
        original (dicitionary): dictionary that should be cleared.
     
    Returns:            
        dictionary where empty sets are removed.
    """
    ret = {}
    for key in original:
        list_o = original[key]
        list_r = []
        for s in list_o:
            if(len(s)>0):
                list_r.append(s)
        ret[key] = list_r
    return ret


