""" The :mod:`command_line` module is used for obtaining execution paramteters.

"""

import re


def get_execution_parameters(options, args, parameters):
    """  Obtains execution parameters.
 
    Args:
        parameters (:dictionary) : Parameter 'parameters' represent initial 
            values of execution parameters
        options : Parameter `options` represents options of the execution.
        args (:list): Parameter `args` represents the argument list.
    Returns:
        dictionary: Execution parameters affter reading command line.
      """

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
    if options.evaluateDirect:
        print ('option evaluateDirect is activated')
    if options.evaluateLikelihood:
        print ('option evaluteLikelihood is activated')
    if options.debug or options.verbose:
       print("Command-line parameters:", end=' ')
       for arg in args:
           print( arg, end = ' ')
       print()     
    
    inputFile_re = re.compile(r'[I|i]nput[F|f]ile=.*\.in')
    inputFormat_re = re.compile(r'[I|i]nput[F|f]ormat=.*')
    dolloK_re = re.compile(r'[D|d]ollo[K|k]=[0-9]+')
    alpha_re = re.compile(r'[A|a]lpha=[0-9].[0-9]+')
    beta_re = re.compile(r'[B|b]eta=[0-9].[0-9]+')    
    randomSeed_re = re.compile(r'[R|r]andom[S|s]eed=[0-9]+')
    populationSize_re = re.compile(r'[P|p]opulation[S|s]ize=[0-9]+')
    eliteSize_re = re.compile(r'[E|e]lite[S|s]ize=[0-9]+')
    crossoverProbability_re = re.compile(r'[C|c]rossover[P|p]robability=[0-9].[0-9]+')
    mutationProbability_re = re.compile(r'[M|m]utation[P|p]robability=[0-9].[0-9]+')
    fineGrainedTournamentSize_re = re.compile(r'[F|f]ine[G|g]rained[T|t]ournament[S|s]ize=[0-9].[0-9]+')
    maxNumberGenerations_re = re.compile(r'[M|m]ax[N|n]umber[G|g]enerations=[0-9]+')
   
    inputFileIsSet = False
    for arg in args:
        if inputFile_re.match(arg):
            parameters['InputFile'] = arg.split('=')[1]
            parameters['InputFormat'] = parameters['InputFile'].split('.')[-1]
            inputFileIsSet = True
            break
    if not inputFileIsSet:
        raise ValueError("Error!\nCommand line parameters:\n" + usage_explanation(parameters))
    for arg in args:    
        if inputFormat_re.match(arg) :
            parameters['InputFormat'] = arg.split('=')[1]
            break
    for arg in args:    
        if dolloK_re.match(arg) :
            parameters['DolloK'] = arg.split('=')[1]
            break        
    for arg in args:    
        if alpha_re.match(arg) :
            parameters['Alpha'] = arg.split('=')[1]
            break        
    for arg in args:    
        if beta_re.match(arg) :
            parameters['Beta'] = arg.split('=')[1]
            break        
    for arg in args:    
        if randomSeed_re.match(arg) :
            parameters['RandomSeed'] = arg.split('=')[1]
            break        
    for arg in args:    
        if populationSize_re.match(arg) :
            parameters['PopulationSize'] = arg.split('=')[1]
            break
    for arg in args:    
        if eliteSize_re.match(arg) :
            parameters['EliteSize'] = arg.split('=')[1]
            break
    for arg in args:    
        if crossoverProbability_re.match(arg) :
            parameters['CrossoverProbability'] = arg.split('=')[1]
            break
    for arg in args:    
        if mutationProbability_re.match(arg) :
            parameters['MutationProbability'] = arg.split('=')[1]
            break
    for arg in args:    
        if fineGrainedTournamentSize_re.match(arg) :
            parameters['FineGrainedTournamentSize'] = arg.split('=')[1]
            break
    for arg in args:    
        if maxNumberGenerations_re.match(arg) :
            parameters['MaxNumberGenerations'] = arg.split('=')[1]
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
    ret += "DolloK=<k_value>\t(optional, integer - default value: " + str(parameters['DolloK']) + ")\n"
    ret += "Alpha=<alpha_value>\t(optional, float - default value: '" + str(parameters['Alpha']) + "')\n"
    ret += "Beta=<beta_value>\t(optional, float - default value: '" + str(parameters['Beta']) + "')\n"
    ret += "RandomSeed=<seed_value>\t(optional, integer - default value: " + str(parameters['RandomSeed']) + ")\n"
    ret += "\t Note: if parameter RandomSeed is negative, random number sequence will start with current time\n"
    ret += "PopulationSize=<size>\t(optional, integer - default value: '" + str(parameters['PopulationSize']) + "')\n"
    ret += "EliteSize=<size>\t(optional, integer - default value: '" + str(parameters['EliteSize']) + "')\n"
    ret += "CrossoverProbability=<probability>\t(optional, float - default value: '" + str(parameters['CrossoverProbability']) + "')\n"
    ret += "MutationProbability=<probability>\t(optional, float - default value: '" + str(parameters['MutationProbability']) + "')\n"
    ret += "FineGrainedTournamentSize=<fgts_size>\t(optional, float - default value: '" + str(parameters['MutationProbability']) + "')\n"
    ret += "MaxNumberGenerations=<max_num>\t(optional, integer - default value: '" + str(parameters['MaxNumberGenerations']) + "')\n"
    return ret
    