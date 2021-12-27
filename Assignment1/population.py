
from random import seed
from random import choice
from random import shuffle

def not_repeat(gene,function_name):
    not_repeat = True

    #####  check not repeat ####
    if len(gene) != len(set(gene)):
        not_repeat = False
    #####  check not repeat ####

    if not_repeat:
        return True
    else:
        print(f"function {function_name} has problem of repeated route")
        return False

def length_not_change(gene,city_count,function_name):
    length_not_change = True

    #####  check length_not_change  ####
    if len(gene) != city_count:
        length_not_change = False
    #####  check length_not_change ####

    if length_not_change:
        return True
    else:
        print(f"function {function_name} has problem of length changed")
        return False




###  every time create new gene/ change gene, use this to check
def check_valid_gene(gene,city_count,function_name):
    
    if not_repeat(gene,function_name) and length_not_change(gene,city_count,function_name):
        return True
    else:
        return False



def get_randomized_gene(city_count):
    #get a randomized gene with 
    # from 1 to city_count
    # not repeated 
    # check valid
    randomized_gene = []

    #number of path  = cities_count 
    #generate a random number in cities_count 
    # seed random number generator
    # remove city 1 ( =0.0) and access it last 
    sequence = [i for i in range(1,city_count+1)]

    #get random index in range 0 to city_count
    shuffle(sequence)
    return sequence


    # #remove the original city 
    # sequence.remove(0) #since it will contain a cycle 


    # #Attention!!!!!!!!!, get the distance matrix not in the class 
    # dist_matrice = TSPProblem.get_distance_matrix()

    # last_city = 0
    # for new_city in range(city_count-1):
    #     randomized_gene.append(dist_matrice[last_city][new_city])
    #     last_city = new_city

    # randomized_gene.append(dist_matrice[last_city][0])

    # return randomized_gene



class Individual:
    gene = []# the order to pass every points
    distance = 0 #distance of this tour 
    fitness = 0 #search to know how to calculate fitness
    city_count = 0 #len of gene

    def __init__(self,gene,city_count):#takes gene list as parameter
        self.gene = gene
        self.city_count = city_count


    def calculate_distance(self,get_distance_between):
        #using self.gene to calculate distance,return an int
        #note that needs to add the distance between the last and first point
        distance = 0
        for i in range(self.city_count):
            if i != self.city_count-1:
                # print(self.gene[i])
                # print(self.gene[i+1])
                distance += get_distance_between(self.gene[i],self.gene[i+1])
                # print(get_distance_between(self.gene[i],self.gene[i+1]))
            else:
                # print(self.gene[i])
                # print(self.gene[0])
                distance += get_distance_between(self.gene[i],self.gene[0])
                # print(get_distance_between(self.gene[i],self.gene[0]))
        self.distance = distance
        return self.distance

    def calculate_fitness(self):
        #using self.gene to calculate fitness,return an int
        fitness = 0
        return fitness


class Population:
    individuals = []
    max_population = 0
    generation = 0
    city_count =0 

    def __init__(self,max_population,city_count):
        self.max_population = max_population
        self.city_count = city_count

    def set_first_generation(self):#set first generation randomly 
        for i in range(self.max_population):#{max_population} number of individuals
            randomized_gene = get_randomized_gene(self.city_count)#
            this_individual = Individual(randomized_gene,self.city_count)#each individual has {city_count} number of points
            self.individuals.append(this_individual)

    def push(self,individual):
        self.individuals.append(individual)

    def find_best_individual(self):
        #find the best individual and return
        best_distance = self.individuals[0].distance
        best_individual = self.individuals[0]
        for individual in self.individuals:
            if individual.distance < best_distance:
                best_individual = individual
                best_distance = individual.distance
            
        # best_individual = self.individuals[0]

        return best_individual

    def calculate_fitness(self, individual,get_distance_between):
        # gene with smaller distance get higher fitness,
        # let fitness of the gene with largest distance be 1,
        # and any gene with distance=d will get a fitness = 1 + (max_dist - d)^p
        p = 1
        return 1 + pow(max([individual.calculate_distance(get_distance_between) for individual in self.individuals]) - individual.calculate_distance(get_distance_between), p)