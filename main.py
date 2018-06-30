"""  The :mod:`cancer_gp` module represents an entry  point of the application.

Example for command-line parameters:
inputFile=example_01.in RandomSeed=1113 PopulationSize=150 EliteSize=50 --debug

"""

import optparse
import random
import time

from datetime import datetime

from deap import base
from deap import creator
from deap import tools


from command_line import get_execution_parameters
from read_input import read_labels_scrs_format_in

from dollo_node import DolloNode


from dollo_node_initialization_operators import init_dollo_node_individual

from dollo_node_evaluation_operators import dollo_closest_node_distance
from dollo_node_evaluation_operators import evaluate_dollo_node_direct 

from dollo_node_crossover_operators import crossover_dollo_node_exchange_parent_indices
from dollo_node_crossover_operators import crossover_dollo_node_exchange_subtrees
from dollo_node_crossover_operators import crossover_dollo_node_combined

from dollo_node_mutation_operators import mutation_dollo_node_add
from dollo_node_mutation_operators import mutation_dollo_node_combine
from dollo_node_mutation_operators import mutation_dollo_node_remove


def contains(individuals, individual):
    """ This function check if list of individuals contains an
        fixed individual.
    """
    for x in individuals:
        if( x is None):
            continue
        if( x.fitness.values[0] != individual.fitness.values[0]):
            continue
        if( x.tree_is_equal(individual) ):
            return True
    return False

def main():
    """ This function is an entry  point of the application.
    """
    # reading command-line argumets and options
    parser = optparse.OptionParser()
    parser.set_defaults(debug=False,xls=False)
    parser.add_option('--debug', action='store_true', dest='debug')
    parser.add_option('--verbose', action='store_true', dest='verbose')
    (options, args) = parser.parse_args()
    
    # obtaining execution paramters
    parameters = {'InputFile': 'xxx.in', 
                  'InputFormat': 'in',
                  'DolloK': 1,
                  'Alpha': 0.4,
                  'Beta': 0.00001,
                  'RandomSeed': 1528981076,
                  'PopulationSize': 9,
                  'EliteSize': 3,
                  'CrossoverProbability': 0.96,
                  'MutationProbability': 0.64,
                  'FineGrainedTournamentSize': 3.5,
                  'MaxNumberGenerations': 50}
    parameters = get_execution_parameters(options, args, parameters)
    print("Execution parameters: ", parameters);
    print("------------------------")
    
    # setting random seed
    random_seed_value = 0
    if( int(parameters['RandomSeed']) > 0 ):
        random_seed_value = int(parameters['RandomSeed'])
    else:
        random_seed_value = int(time.mktime(datetime.now().timetuple()))
    random.seed( random_seed_value )
    print("Random seed: ",random_seed_value);
    time_of_start = time.time()
    print("Execution starts at time: ", time_of_start )
    print("------------------------")
    
        
    # reading read elements from input file
    if( parameters['InputFormat'] == 'in' ):
        (labels, reads) = read_labels_scrs_format_in(options, parameters)
        if(options.debug or options.verbose):
            print("Mutation labels (from input file):\n", labels);
            print("Reads[Unknowns] (from input file):")
            for x in reads:
                print(x);
    else:
        print("Error: Input format is not right.")
        return
    if( options.verbose):
        current_time = time.time()
        print("Parameters read after: ", current_time - time_of_start)
        time_of_start = current_time

    if( options.debug or options.verbose):
        print("Start of evolution")
    # create fitness function
    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
   
    # create strucute of the individual
    creator.create("Individual", DolloNode, fitness=creator.FitnessMin)
    
    # create toolbox for execution of the evolutionary algorithm
    toolbox = base.Toolbox()
    
    # register bolean attribute to toolbbox 
    toolbox.register("attr_bool", random.randint, 0, 1)

    # parameter k in Dollo model
    dollo_k = int(parameters['DolloK'])
    if( dollo_k < 0):
        print("Error: parameter DolloK should not be negative.")
        return
    # register individual creation to toolbbox 
    toolbox.register("individual", 
                     init_dollo_node_individual, 
                     creator.Individual, 
                     labels=labels, 
                     k=dollo_k)
      
    # register population to toolbbox 
    toolbox.register("population", 
                     tools.initRepeat, 
                     list, 
                     toolbox.individual)
 
    # probability of false positives and false negatives
    alpha = float(parameters['Alpha'])
    if( alpha < 0):
        print("Error: parameter Alpha should not be negative.")
        return
    if( alpha >= 1):
        print("Error: parameter Alpha should be less than 1.")
        return
    beta = float(parameters['Beta'])
    if( beta < 0):
        print("Error: parameter Beta should not be negative.")
        return
    if( beta >= 1):
        print("Error: parameter Beta should be less than 1.")
        return
    # register evaluation function
    toolbox.register("evaluate", 
                     evaluate_dollo_node_direct, 
                     reads,
                     alpha)

    # register the crossover operator
    toolbox.register("mate", 
                     crossover_dollo_node_exchange_parent_indices,
                     labels, dollo_k)
    # probability with which two individuals are crossed
    crossover_probability = float(parameters['CrossoverProbability'])
    if( crossover_probability < 0):
        print("Error: parameter CrossoverProbability should not be negative.")
        return
    if( crossover_probability > 1):
        print("Error: parameter CrossoverProbability should not be greater than 1.")
        return
           
    # register a mutation operator 
    toolbox.register("mutate", 
                     mutation_dollo_node_combine, 
                     labels,
                     dollo_k)
    # probability for mutating an individual
    mutation_probability = float(parameters['MutationProbability'])
    if( mutation_probability < 0):
        print("Error: parameter MutationProbability should not be negative.")
        return
    if( mutation_probability > 1):
        print("Error: parameter MutationProbability should not be greater than 1.")
        return

    # create an initial population, where each individual is a tree
    population_size = int(parameters['PopulationSize'])
    if( population_size <= 0):
        print("Error: parameter PopulationSize should be positive.")
        return
    pop = toolbox.population(n=population_size)
    if( options.verbose):
        print("Population (size %d) - initial\n"%len(pop))
        print (pop)
 
    # operator for selecting individuals for breeding the next
    # generation
    fgt_size = float(parameters['FineGrainedTournamentSize'])
    if( fgt_size <= 0):
        print("Error: parameter FineGrainedTournamentSize should be positive.")
        return
    toolbox.register("select", 
                     tools.selTournamentFineGrained, 
                     fgtournsize=fgt_size)

    if( options.verbose):
        current_time = time.time()
        print("Registering operators for deap after: ", current_time - time_of_start)
        time_of_start = current_time
    
    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    if( options.debug):
        print("Fitnesses of individuals in population - initial")
        print (fitnesses)

    if( options.verbose):
        current_time = time.time()
        print("Initial evaluating the entire population after: ", current_time - time_of_start)
        time_of_start = current_time
    
    # Assign fitness to individuals in population
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    
    # Variable for maximum number of generations    
    max_number_generations = int(parameters['MaxNumberGenerations'])
    if( max_number_generations < 0):
        print("Error: parameter MaxNumberGenerations should not be negative.")
        return
    # Variable keeping track of the number of generations
    generation = 0
  
    # Begin the evolution
    while True:
        if( options.debug or options.verbose):
            print("-- Generation %i --" % generation)
            print("Generation at: ",  time.time())
   
        if( options.debug or options.verbose):
            fits = [ind.fitness.values[0] for ind in pop]
            length = len(pop)
            mean = sum(fits) / length
            sum2 = sum(x*x for x in fits)
            std = abs(sum2 / length - mean**2)**0.5
            print("  Fitnesses: ", fits)
            print("  Min %s" % min(fits))
            print("  Max %s" % max(fits))
            print("  Avg %s" % mean)
            print("  Std %s" % std)
            best_in_generation = tools.selBest(pop, 1)[0]
            print("  Best individual: \n %s", best_in_generation)
            print("  Best individual fitness: ", best_in_generation.fitness.values[0]); 
        
        # A new generation
        generation += 1

        # size of the elite part of the population
        elite_size = int(parameters['EliteSize'])
        if( elite_size < 0):
            print("Error: parameter EliteSize should not be negative.")
            return
        if( elite_size > population_size):
            print("Error: parameter EliteSize should not be greather than PopulationSize.")
            return
        # elite individuals
        elite = tools.selBest(pop,elite_size)
        # clone elite individuals
        elite = list(map(toolbox.clone, elite))
        if(options.verbose):
            print("elite =", elite)
        # non-elite individuals
        non_elite =  tools.selWorst(pop, population_size-elite_size)
        # clone non-elite individuals
        non_elite = list(map(toolbox.clone, non_elite))
        if(options.verbose):
            print("non_elite =", non_elite)
         
        # Select the ofsprings
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected offsprings
        offspring = list(map(toolbox.clone, offspring))
        if(options.verbose):
            print("offspring (after selection) \n =", offspring)
        if( options.verbose):
            current_time = time.time()
            print("Selecting offsprings after: ", current_time - time_of_start)
            time_of_start = current_time
  
        # Apply crossover on the offsprings
        for i in range(0,len(offspring)):
            # cross two individuals with previously determined probability 
            if random.random() < crossover_probability:
                child1 = random.choice(offspring)
                index2 = random.choice(range(0,len(offspring)))
                child2 = offspring[index2]
                i = 0
                while(child2.tree_is_equal(child1) and i<=len(offspring)):
                    i += 1
                    child2 = offspring[(index2+i)%len(offspring)]
                toolbox.mate(child1, child2)
                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values
        if(options.verbose):
            print("offspring (after crossover) \n =", offspring)
        if( options.verbose):
            current_time = time.time()
            print("Crossover after: ", current_time - time_of_start)
            time_of_start = current_time

        # Apply mutation on the offspring
        for mutant in offspring:
            # mutate an individual with previously determined probability 
            if random.random() < mutation_probability:
                toolbox.mutate(mutant)
                # fitness values of the mutant
                # must be recalculated later
                del mutant.fitness.values
        if(options.verbose):
            print("offspring (after mutation) \n =", offspring)
        if( options.verbose):
            current_time = time.time()
            print("Mutation after: ", current_time - time_of_start)
            time_of_start = current_time
   
        # Evaluate the new individuals that has no fitness until now
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
            
        # Pool of items that should be copies into new generation
        # offsprings are put into pool
        pool = offspring
        # non-elite individuals are put into pool
        for i in range(0, population_size-elite_size):
            pool.append(non_elite[i])
        if(options.verbose):
            print("pool (for new generation) \n =", pool)
      
        # Elite individuals are copied into population
        for i in range(0,elite_size):
            pop[i] = elite[i]
        if(options.verbose):
            print("population (elites are copied) \n =", pop)

        # Remainning part of population is filled individuals from pool, 
        # taking into account that there will be no
        # repetition of the individuals 
        for i in range(elite_size,population_size):
            pop[i] = None
        j=0
        for i in range(elite_size,population_size):
            while(j<len(pool) and contains(pop, pool[j])):
                j+=1
            if( j < len(pool)):
                pop[i] = pool[j]
            else:
                pop[i] = pool[i-elite_size]
        if(options.verbose):
            print("population (all items are copied) \n =", pop)
        if( options.verbose):
            current_time = time.time()
            print("Evaluation of changed individuals after: ", current_time - time_of_start)
            time_of_start = current_time


        # Check if any of finishing criteria is meet
        # Criteria based on number of generations
        if( generation > max_number_generations ):
            break
        # Criteria based on standard deviation of fitness in population
        fits = [ind.fitness.values[0] for ind in pop]
        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5 
        if( std <= 0):
            break
          
    if( options.debug or options.verbose):
        print("-- End of evolution --")
    if( options.verbose):
        print("Population (size %d) - at end\n"%len(pop))
        print (pop)  
    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is\n%s\n, with fitness %s" % (best_ind, best_ind.fitness.values))
    if( options.debug):        
        print("Efficiency of cashing for funcion dolo_closest_node_distance")
        print(dollo_closest_node_distance.cache_info())
    return

# this means that if this script is executed, then 
# main() will be executed
if __name__ == '__main__':
    main()



