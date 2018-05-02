""" The :mod:`command_line` module is used for obtaining execution paramteters.

"""

import re


def get_execution_parameters(options, args):
    """  Obtains execution parameters.
 
    Args:
        options : Parameter `options` represents options of the execution.
        args (:list): Parameter `args` represents the argument list.
    Returns:
        dictionary: Execution parameters.
      """
    parameters = {'InputFile': 'XXX.in', 
                  'InputFormat': 'in',
                  'RandomSeed': -1,
                  'PopulationSize': 5}

    if len(args) == 0:
        raise ValueError("Error!\nCommand line parameters:\n" + usage_explanation(parameters))
    if len(args) > 300:
        raise ValueError("Error!\nCommand line parameters:\n" + usage_explanation(parameters))

    if options.debug:
        print( 'option debug is activated')
    else:
        print( 'option debug is deactivated')       
    if options.verbose:
        print ('option verbose is activated')
    else:
        print( 'option verbose is deactivated')           
    if options.debug or options.verbose:
       print("Command-line parameters:", end=' ')
       for arg in args:
           print( arg, end = ' ')
       print()     
    
    inputFile_re = re.compile(r'[I|i]nput[F|f]ile=.*\.in')
    inputFormat_re = re.compile(r'[I|i]nput[F|f]ormat=.*')
    randomSeed_re = re.compile(r'[R|r]andom[S|s]eed=[0-9]+')
    populationSize_re = re.compile(r'[P|p]opulation[S|s]ize=[0-9]+')

    inputFileIsSet = False
    for arg in args:
        if inputFile_re.match(arg):
            parameters['InputFile'] = arg.split('=')[1]
            parameters['InputFormat'] = parameters['InputFile'].split('.')[-1]
            inputFileIsSet = True
            break
    if not inputFileIsSet:
        raise ValueError("Usage:\n" + usage_explanation(parameters))

    for arg in args:    
        if inputFormat_re.match(arg) :
            parameters['InputFormat'] = arg.split('=')[1]
            break

    for arg in args:    
        if randomSeed_re.match(arg) :
            parameters['RandomSeed'] = arg.split('=')[1]
            break
        
    for arg in args:    
        if populationSize_re.match(arg) :
            parameters['PopulationSize'] = arg.split('=')[1]
            break

    return parameters
 
def usage_explanation(parameters):
    """  Create ussage explanation text.
 
    Args:
        parameters : Parameter `papramters is a dictionary that` represents parameters of the execution.
    """
    ret = ""
    ret += "InputFile=<file_name>\t(mandatory, string) \n"
    ret += "InputFormat=<format>\t(optional, string - default value: '" + parameters['InputFormat'] + "')\n"
    ret += "RandomSeed=<seed_value>\t(optional, integer - default value: " + str(parameters['RandomSeed']) + ")\n"
    ret += "\t Note: if parameter RandomSeed is negative, random number sequence will start with current time\n"
    ret += "PopulationaSize=<size>\t(optional, integer - default value: '" + str(parameters['PopulationaSize']) + "')\n"
    return ret
    