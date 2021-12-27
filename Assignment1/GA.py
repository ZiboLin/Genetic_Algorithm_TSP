import random
from population import *


#mutation operators take 1 parameter and return one new individual
#DONT directly change individuals,copy it to new individual, then perform operators


# generate a pair (lp, rp) in range(n), where 0 <= lp <= rp < n.
def generate_pair(n):
    lp = random.randrange(n)
    rp = random.randrange(n)
    if lp > rp :
        lp, rp = rp, lp
    return lp, rp

# generate a pair (lp, rp) in range(n), where 0 <= lp < rp < n.
# the (lp, rp) should be evenly distributed with a probability 2/(n*(n-1)), and selecting
# rp basing on lp won't achieve this goal.
def generate_pair_different(n):
    lp, rp = -1, -1
    while lp == rp :
        lp, rp = generate_pair(n)
    return lp, rp

# this method will return -1 if the num is not in the list.
def find_index(num, lst):
    for i in range(len(lst)):
        if lst[i] == num:
            return i
    return -1

# remove all elems from the table of edges.
def remove_from_edges_table(elem, edges_table):
    for item in range(1, len(edges_table)):
        edges = edges_table[item]
        idx = find_index(elem, edges)
        while idx != -1 :
            edges.remove(elem)
            idx = find_index(elem, edges)

# remove the list of common edges in a given edges list.
def get_common_edges(edges):
    common_edges = []
    for i in range(len(edges)):
        for j in range(i):
            if edges[i] == edges[j] :
                common_edges.append(edges[i])
    return common_edges

# get the items count, disgarding the duplicated one.
def get_items_count(edges):
    count = 0
    for i in range(len(edges)):
        common = False
        for j in range(i):
            if edges[i] == edges[j] :
                common = True
        if not common:
            count = count + 1
    return count

#########################end of helper functions and begin GA algorithms############################




def insert(individual,len):
    gene = list(individual.gene)
    count = individual.city_count

    lp, rp = generate_pair_different(count)
    ritem = gene[rp]
    for i in range(rp-1, lp, -1):
        gene[i+1] = gene[i]
    gene[lp+1] = ritem
    
    new_individual = Individual(gene, count)

    return new_individual


def swap(individual,len):
    gene = list(individual.gene)
    count = individual.city_count

    lp, rp = generate_pair_different(count)
    gene[lp], gene[rp] = gene[rp], gene[lp]

    new_individual = Individual(gene, count)

    return new_individual

def inversion(individual,len):
    gene = list(individual.gene)
    count = individual.city_count

    lp, rp = generate_pair_different(count)
    while lp < rp :
        gene[lp], gene[rp] = gene[rp], gene[lp]
        lp = lp + 1
        rp = rp - 1
        
    new_individual = Individual(gene, count)
    return new_individual

def scram(individual,len):
    gene = list(individual.gene)
    count = individual.city_count
    old_gene = list(gene)

    # randomly select a subset and shuffle
    indexes = []
    for i in range(count):
        if random.random() < 0.5:
            indexes.append(i)
    indexes_rearanged = list(indexes)
    random.shuffle(indexes_rearanged)

    for index, index_rearanged in zip(indexes, indexes_rearanged):
        gene[index] = old_gene[index_rearanged]
        
    new_individual = Individual(gene, count)
    return new_individual


#cross operators take 2 parameter and return one or two new individual
#DONT directly change individuals,copy it to new individual, then perform operators
def order_crossover(individual1,individual2,len):
    gene1 = list(individual1.gene)
    gene2 = list(individual2.gene)
    count = individual1.city_count
    flag1 = [False] * (count+1)
    flag2 = [False] * (count+1)

    lp, rp = generate_pair(len)
    # lp, rp = 3, 6 # for test.
    for i in range(lp, rp+1):
        gene1[i] = individual1.gene[i]
        flag1[gene1[i]] = True
        gene2[i] = individual2.gene[i]
        flag2[gene2[i]] = True
    
    # add elem not in child1 as the order in parent2.
    p1 = (rp+1) % count
    p2 = (rp+1) % count
    while p1 != lp :
        while flag1[individual2.gene[p2]] :
            p2 = (p2+1) % count
        gene1[p1] = individual2.gene[p2]
        flag1[gene1[p1]] = True
        p1 = (p1+1) % count
        p2 = (p2+1) % count

    p1 = (rp+1) % count
    p2 = (rp+1) % count
    while p2 != lp :
        while flag2[individual1.gene[p1]] :
            p1 = (p1+1) % count
        gene2[p2] = individual1.gene[p1]
        flag2[gene2[p2]] = True
        p1 = (p1+1) % count
        p2 = (p2+1) % count

    new_individual1 = Individual(gene1, count)
    new_individual2 = Individual(gene2, count)
    return new_individual1, new_individual2

def PMX_crossover(individual1,individual2,len):
    gene1 = list(individual1.gene)
    gene2 = list(individual2.gene)
    count = individual1.city_count
    flag1 = [False] * (count+1)
    flag2 = [False] * (count+1)

    lp, rp = generate_pair(len)
    # lp, rp = 3, 6 # for test.
    for i in range(lp, rp+1):
        gene1[i] = individual1.gene[i]
        flag1[gene1[i]] = True
        gene2[i] = individual2.gene[i]
        flag2[gene2[i]] = True
    
    # the main process of PMX.
    for i in range(lp, rp+1):
        item1 = gene1[i]
        item2 = gene2[i]
        if flag1[item2]:
            continue
        
        idx = individual2.gene.index(item1)
        while (idx >= lp) and (idx <= rp) :
            item1 = gene1[idx]
            idx = individual2.gene.index(item1)
        
        gene1[idx] = item2
        flag1[item2] = True

    for i in range(lp, rp+1):
        item1 = gene1[i]
        item2 = gene2[i]
        if flag2[item1]:
            continue

        idx = individual1.gene.index(item2)
        while (idx >= lp) and (idx <= rp) :
            item2 = gene2[idx]
            idx = individual1.gene.index(item2)
        
        gene2[idx] = item1
        flag2[item1] = True
    
    # the others are correspond.
    for i in range(count):
        if not flag1[individual2.gene[i]] :
            gene1[i] = individual2.gene[i]
            flag1[gene1[i]] = True
        if not flag2[individual1.gene[i]] :
            gene2[i] = individual1.gene[i]
            flag2[gene2[i]] = True


    new_individual1 = Individual(gene1, count)
    new_individual2 = Individual(gene2, count)

    return new_individual1, new_individual2

def cycle_crossover(individual1,individual2,len):
    gene1 = list(individual1.gene)
    gene2 = list(individual2.gene)
    count = individual1.city_count
    cycle_id = [0] * count

    # label the index from 0 to count-1 with the id of cycle.
    cycle_cnt = 1
    for i in range(count):
        if cycle_id[i] == 0 :
            target = individual1.gene[i]
            cycle_id[i] = cycle_cnt

            idx = individual1.gene.index(individual2.gene[i])
            while individual1.gene[idx] != target :
                cycle_id[idx] = cycle_cnt
                idx = individual1.gene.index(individual2.gene[idx])
            
            cycle_cnt = cycle_cnt + 1
    
    for i in range(count):
        if (cycle_id[i] % 2) == 1 :
            gene1[i] = individual1.gene[i]
            gene2[i] = individual2.gene[i]
        else:
            gene1[i] = individual2.gene[i]
            gene2[i] = individual1.gene[i]


    new_individual1 = Individual(gene1, count)
    new_individual2 = Individual(gene2, count)

    return new_individual1, new_individual2



def edge_recombination(individual1,individual2,lenth):
    gene = []
    count = individual1.city_count
    remaining = list(range(1, count+1))
    edges_table = []
    for i in range(count+1):
        edges_table.append([])

    for i in range(count):
        elem = individual1.gene[i]
        ledge = individual1.gene[(i-1+count) % count]
        redge = individual1.gene[(i+1) % count]
        edges_table[elem].append(ledge)
        edges_table[elem].append(redge)

        elem = individual2.gene[i]
        ledge = individual2.gene[(i-1+count) % count]
        redge = individual2.gene[(i+1) % count]
        edges_table[elem].append(ledge)
        edges_table[elem].append(redge)

    # elem = 1 # for test.
    elem = random.choice(remaining)
    gene.append(elem)
    remaining.remove(elem)
    remove_from_edges_table(elem, edges_table)
    other_end = False
    while len(gene) < count :  
        choices = edges_table[elem]

        # if there is no choice, start from the other end or select randomly.
        if len(choices) == 0 :
            if not other_end :
                elem = gene[0]
                other_end = True
            else:
                elem = random.choice(remaining)
                gene.append(elem)
                remaining.remove(elem)
                remove_from_edges_table(elem, edges_table)
                other_end = False
            continue
        
        # if there is common edges.
        common_edges = get_common_edges(choices)
        if len(common_edges) != 0 :
            elem = random.choice(common_edges)
            gene.append(elem)
            remaining.remove(elem)
            remove_from_edges_table(elem, edges_table)
            continue

        # select the elem with shortest list.
        items_count = [get_items_count(edges_table[elem]) for elem in choices]
        min_count = min(items_count)
        elems_with_shortest_list = [elem for elem in choices if get_items_count(edges_table[elem]) == min_count]
        elem = random.choice(elems_with_shortest_list)
        gene.append(elem)
        remaining.remove(elem)
        remove_from_edges_table(elem, edges_table)
    
    new_individual = Individual(gene, count)
    return new_individual

#selection operators takes population and make a new population with 
#{max_population} individuals, and return this
#DONT directly change population,copy it to new individual, then perform operators

import copy
def fitness_proportional(population,get_distance_between):
    new_population = copy.deepcopy(population)
    individuals = copy.deepcopy(new_population.individuals)
    new_population.individuals = []

    # # select the individual with the probability correspond to the fitness, update instantly and won't
    # # select an individual more than once.
    # while (individuals != []) and (len(new_population.individuals) < new_population.max_population) :
    #     fitnesses = [individual.calculate_fitness() for individual in individuals]
    #     individual = random.choices(individuals, weights=fitnesses, k=1)[0]
    #     new_population.push(individual)
    #     individuals.remove(individual)

    # this implementation may select an individual more than once.
    fitnesses = [population.calculate_fitness(individual,get_distance_between) for individual in individuals]
    new_population.individuals = random.choices(individuals, weights=fitnesses, k=new_population.max_population-1)
    for i in range(new_population.max_population-1):
        new_population.individuals[i] = copy.deepcopy(new_population.individuals[i])

    return new_population

def tournament_selection(population,get_distance_between):
    K = 3
    new_population = copy.deepcopy(population)
    individuals = copy.deepcopy(new_population.individuals)
    new_population.individuals = []

    while (individuals != []) and (len(new_population.individuals) < new_population.max_population-1) :
        k = 0
        samples = []

        # randomly select K participants if sufficient.
        while (k < K) and (individuals != []) :
            individual = random.choice(individuals)
            individuals.remove(individual)
            samples.append(individual)
            k = k+1
        
        max_fitness = 0
        for individual in samples :
            fitness = population.calculate_fitness(individual,get_distance_between)
            max_fitness = max(max_fitness, fitness)
        
        winners = [individual for individual in samples if population.calculate_fitness(individual,get_distance_between) == max_fitness]
        individual = random.choice(winners)
        new_population.push(individual)

        # put back the participants not selected.
        samples.remove(individual)
        individuals.extend(samples)

    return new_population

def elitism(population,get_distance_between):
    new_population = copy.deepcopy(population)
    individuals = copy.deepcopy(new_population.individuals)
    new_population.individuals = []

    # select the individuals with largest fitness.
    individuals.sort(key=lambda x: population.calculate_fitness(x,get_distance_between), reverse=True)
    for i in range(new_population.max_population-1):
        new_population.push(individuals[i])

    return new_population
