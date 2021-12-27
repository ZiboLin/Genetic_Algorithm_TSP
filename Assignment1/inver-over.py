from TspProblem import *
from GA import *
from population import *
import random
import matplotlib.pyplot as plt
import copy

##########   change setting here    ##################
fileName = "eil51.tsp" 
p_value = 0.2
##########   change setting here    ##################


def inverse(gene, start, end):
    new_sub_gene = []
    # print(".....................")
    # print(gene)
    if start < end:
        for i in range(end-start):
            num = gene.pop((start+1) % len(gene))
            new_sub_gene.append(num)

        for i in range(end-start):
            gene.insert(start+1, new_sub_gene[i])
    else:
        gene = gene[::-1]
        for i in range(start-end):
            num = gene.pop((end+1) % len(gene))
            new_sub_gene.append(num)

        for i in range(start-end):
            gene.insert(end+1, new_sub_gene[i])

    # print(gene)
    # print(".....................")

    return gene


def guotao(p):
    # random initialization of the population P
    setting = {
        'max_generation': 20000,
        'max_population': 50,
        'mutation_method': None,
        'mutation_rate': None,
        'cross_method': None,
        'cross_rate': None,
        'selection_method': None,
        'file_name': fileName,
    }
    print(setting["file_name"])

    tsp_problem = TSPProblem(**setting)

    # pass how many population and how many cities to the population
    population = Population(tsp_problem.max_population, tsp_problem.city_count)
    population.set_first_generation()
    # for individual in population.individuals:
    #     print( individual.gene)

    for individual in population.individuals:
        # print (individual.city_count)
        individual.calculate_distance(tsp_problem.get_distance_between)

    generation = 0
    # while (not satied termination-condition) do
    while generation < setting["max_generation"]:
        generation += 1
        for Si in population.individuals:

            Si_index = population.individuals.index(Si)
            S_dash = copy.deepcopy(Si)
            S_dash.gene = copy.deepcopy(Si.gene)
            c_index = random.randint(0, population.city_count-1)
            c = S_dash.gene[c_index]

            # print(population.individuals[Si_index].gene)
            while 1:
                if random.random() <= p:
                    c_dash_index = random.randint(0, population.city_count-1)
                    c_dash = S_dash.gene[c_dash_index]
                    while c_dash_index == c_index:
                        c_dash_index = random.randint(
                            0, population.city_count-1)
                        c_dash = S_dash.gene[c_dash_index]
                else:
                    select_individual_index = random.randint(
                        0, setting["max_population"]-1)
                    while select_individual_index == Si_index:
                        select_individual_index = random.randint(
                            0, setting["max_population"]-1)
                    selected_individual = population.individuals[select_individual_index]
                    # assign to c' the `next' city to the city c in the selected individual
                    c_index_selected = selected_individual.gene.index(c)
                    if c_index_selected + 1 >= population.city_count:
                        c_dash_index = 0
                    else:
                        c_dash_index = c_index_selected + 1
                    c_dash = selected_individual.gene[c_dash_index]
                # if (the next city or the previous city of city c in S' is c')
                if S_dash.gene.index(c_dash) == (c_index+1) % population.city_count or S_dash.gene.index(c_dash) == (c_index-1) % population.city_count:
                    break
                S_dash.gene = inverse(
                    S_dash.gene, c_index, S_dash.gene.index(c_dash))

                c = c_dash
                c_index = c_dash_index

            eval_Si = Si.calculate_distance(
                tsp_problem.get_distance_between)
            eval_S_dash = S_dash.calculate_distance(
                tsp_problem.get_distance_between)
            # print(eval_Si, eval_S_dash)

            if eval_S_dash <= eval_Si:
                Si = copy.deepcopy(S_dash)
            
            eval_Si = Si.calculate_distance(
                tsp_problem.get_distance_between)
            # print(f"Si.distance: {Si.distance}")
            population.individuals[Si_index] = Si
            # print(f"population.individuals[Si_index]: {population.individuals[Si_index].distance}")
        # print("....................")

        best_individual = population.find_best_individual()
        tsp_problem.push_best_individual(best_individual)
    # for individual in tsp_problem.best_individuals:
    #     print(individual.gene)
    #     print(individual.distance)
    #     print("...............................")
        print(generation)
    return best_individual, tsp_problem


best_individual, tsp_problem = guotao(p_value)


best_distances = []
for individual in tsp_problem.best_individuals:
    best_distances.append(individual.distance)
    # print(best_distances)
print(f"the final best route is {tsp_problem.best_individuals[-1].gene}")
print(
    f"the final best distance is {tsp_problem.best_individuals[-1].distance}")
plt.plot(best_distances)
plt.ylabel('distance')
plt.xlabel('generations')
plt.show()


# ind = Individual([1,
#                   8,
#                   38,
#                   31,
#                   44,
#                   18,
#                   7,
#                   28,
#                   6,
#                   37,
#                   19,
#                   27,
#                   17,
#                   43,
#                   30,
#                   36,
#                   46,
#                   33,
#                   20,
#                   47,
#                   21,
#                   32,
#                   39,
#                   48,
#                   5,
#                   42,
#                   24,
#                   10,
#                   45,
#                   35,
#                   4,
#                   26,
#                   2,
#                   29,
#                   34,
#                   41,
#                   16,
#                   22,
#                   3,
#                   23,
#                   14,
#                   25,
#                   13,
#                   11,
#                   12,
#                   15,
#                   40,
#                   9], 48)
# ind.calculate_distance(tsp_problem.get_distance_between)
# print(ind.distance)
