"""
This module is used for obtaining execution paramteters.

"""

import re


def get_execution_parameters(options, args):
    """
    Obtains execution paramteters.
    """
    randomSeed_re = re.compile(r'[R|r]andom[S|s]eed=[0-9]+')
    inputFile_re = re.compile(r'[I|i]nput[F|f]ile=.*\.in')

    if options.debug:
        print( 'option debug is activated')
    else:
        print( 'option debug is deactivated')       
    if options.randomized:
        print ('option randomized is activated')
    else:
        print( 'option randomized is deactivated')           
    if options.debug:
       print("Command-line parameters are:", end=' ')
       for arg in args:
           print( arg, end = ' ')
       print()     
    if len(args) > 2:
        raise ValueError("Too many command line arguments. Format: 'inputFile=XXX.in radnomSeed=999'.")
    if len(args) <= 1:
        raise ValueError("Too few command line arguments. Format: 'inputFile=XXX.in radnomSeed=999'.")  
    
    parameters = {'InputFile': 'XXX.in', 'RandomSeed': 111}
    if not randomSeed_re.match(args[0]) :
        if not randomSeed_re.match(args[1]):
            raise ValueError("There must be an argument: 'randomSeed=DDD', where 'DDD' is postitive integer.")
        else:
            parameters['RandomSeed'] = args[1].split('=')[1]
    else:
        parameters['RandomSeed'] = args[0].split('=')[1]
    if not inputFile_re.match(args[0]):
        if not inputFile_re.match(args[1]):
            raise ValueError("There must be an argument: 'inputFile=XXX.in' where 'XXX' is file name.")
        else:
            parameters['InputFile'] = args[1].split('=')[1]
    else:
        parameters['InputFile'] = args[0].split('=')[1]
    return parameters
 