from TspProblem import *
from GA import *
from population import *
import random
import copy
import matplotlib.pyplot as plt

#################  setting here  ###############

##change here to change the file name
##note that this only needs the file name, do not include the path
fileName = "kroC100.tsp" 


setting1 = {
    'max_generation' : 5000,
    'max_population' : 10,
    'mutation_method' : "inversion",
    'mutation_rate' : 0.5,
    'cross_method' : "order_crossover",
    'cross_rate' : 0.5,
    'selection_method' : "elitism",
    'file_name' : fileName,
}

setting2 = {
    'max_generation' : 5000,
    'max_population' : 10,
    'mutation_method' : "inversion",
    'mutation_rate' : 0.6,
    'cross_method' : "cycle_crossover",
    'cross_rate' : 0.7,
    'selection_method' : "elitism",
    'file_name' : fileName,
}

setting3 = {
    'max_generation' : 5000,
    'max_population' : 10,
    'mutation_method' : "inversion",
    'mutation_rate' : 0.7,
    'cross_method' : "edge_recombination",
    'cross_rate' : 0.6,
    'selection_method' : "elitism",
    'file_name' : fileName,
}


##change setting inorder to try the different algorithms
setting = setting3  #setting1 can be changed to setting1/setting2/setting3

#################  setting here  ###############






def evolution(population,tsp_problem):
    generation = 0
    
    # current_population.individuals.append(Individual([1,2,3,4,5,6],6)) 
    # for individual in population.individuals:
    #     print(individual.gene)
    for i in range(tsp_problem.max_generation):
        current_population =copy.deepcopy(population)
        current_population.individuals = copy.deepcopy(population.individuals)
        generation +=1
        while 1:
            individual1  = random.choice(population.individuals)
                    ####mutation###
            if random.random() < tsp_problem.mutation_rate:
                mutation_function_name = tsp_problem.mutation_method
                new_individual = eval(mutation_function_name + "( individual1 ,tsp_problem.city_count )")
                new_individual.calculate_distance(tsp_problem.get_distance_between)
                # print(new_individual.distance)
                current_population.individuals.append(new_individual)
        
            ####mutation#####
            individual2  = random.choice(population.individuals)
            while individual2 == individual1:
                individual2  = random.choice(population.individuals)
            if individual1 != individual2:
                ###cross##
                if random.random() < tsp_problem.cross_rate:
                    cross_function_name = tsp_problem.cross_method
                    if cross_function_name != "edge_recombination":
                        new_individual1,new_individual2 = eval(cross_function_name + "( individual1,individual2 ,tsp_problem.city_count )")
                        new_individual1.calculate_distance(tsp_problem.get_distance_between)
                        new_individual2.calculate_distance(tsp_problem.get_distance_between)
                    
                        current_population.individuals.append(new_individual1)
                        current_population.individuals.append(new_individual2)
                    else:
                        new_individual = eval(cross_function_name + "( individual1,individual2 ,tsp_problem.city_count )")
                        new_individual.calculate_distance(tsp_problem.get_distance_between)
                    
                        current_population.individuals.append(new_individual)
                    ###cross##
            if len(current_population.individuals) >= 1.5 * tsp_problem.max_population:
                break

            

        # select until num of individual equals to max_population
        selection_method = tsp_problem.selection_method
        # print(selection_method)
        population = eval(selection_method + "(current_population,tsp_problem.get_distance_between)")

        # for individual in population.individuals:
        #     print(individual.distance)
        if i != 0:
            population.individuals.append(best_individual)
        print(generation)
        best_individual =population.find_best_individual()  
        tsp_problem.push_best_individual(best_individual)



    # for individual in tsp_problem.best_individuals:
    #     print(individual.distance)


            
    return tsp_problem.coordinates , tsp_problem.best_individuals
    







###############3   initialize   ##################
tsp_problem = TSPProblem(**setting)
print(setting["file_name"])

#pass how many population and how many cities to the population
population = Population(tsp_problem.max_population, tsp_problem.city_count)
population.set_first_generation()

for individual in population.individuals:
    # print (individual.city_count)
    individual.calculate_distance(tsp_problem.get_distance_between)
#     print(individual.gene)
# print(".............................................")
# print(distance_matrix)

###############3   initialize   ##################

############ cross and mutation #########

coordinations, best_individuals = evolution(population,tsp_problem)

best_distances =[]
for individual in best_individuals:
    best_distances.append(individual.distance)
print(f"the final best route is {best_individuals[-1].gene}")
print(f"the final best distance is {best_individuals[-1].distance}")
plt.plot(best_distances)
plt.ylabel('distance')
plt.xlabel('generations')
plt.show()



