from population import *
import math 




class TSPProblem:

    max_generation = 100
    max_population = 100
    mutation_method = None
    mutation_rate = None
    cross_method = None
    cross_rate = None
    selection_method = None


    coordinates = [] #a dictionary of coordinates
    distance_matrix=[]#an matrix of distances, for example distance_matrix[1][2] means distance between city 1 and 2
    best_individuals = []#every generation's best performed individual
    best_distances = [] #every generation's best performed individual's distance
    city_count = 0 # how many city in this problem
    file_name = None #which file to read

    def __init__(self,max_generation,max_population,mutation_method,mutation_rate,cross_method,cross_rate,selection_method,file_name):
        self.max_generation = max_generation
        self.max_population = max_population
        self.mutation_method = mutation_method
        self.mutation_rate = mutation_rate
        self.cross_method = cross_method
        self.cross_rate = cross_rate
        self.selection_method =selection_method
        self.file_name = "./files/"+file_name
        self.read_coordinates()
        self.get_distance_matrix()



    def read_coordinates(self):
        #return a dictionary of coordinates,and set city_count
        coordinates = []
        city_count = 0
        #read self.filename and get coordinates

        x_nums = 3  #each entry has 3 numbers 
        global cities_count

        try:
            data_file = open(self.file_name) 
        except FileNotFoundError:
            print("File read error")
            return None

        #get the file line by line 
        #the first 5 lines consisted of unwant data 
        for i in range(6):
            unwant_data = data_file.readline()

        #read the coordinate of cities 
        line = data_file.readline()
        while line:
            temp_line_splits = line.split() 
            temp = list(temp_line_splits[1:x_nums])
            coordinates.append(temp)

            city_count += 1       

            #getting rid of last entry 
            line = data_file.readline()
            if "EOF" in line: break 
            # count += 1 
        data_file.close()

        self.coordinates = coordinates
        self.city_count = city_count

    def get_distance_matrix(self):
        #return an matrix of distances
        #for example distance_matrix[1][2] means distance between city 1 and 2
        distances = []
        #calculate distance using self.coordinates

        #initilise the matrice with all entries 0 
        distances = [ [ 0 for i in range(self.city_count) ] for j in range(self.city_count) ]

        for i in range(self.city_count):
            # so we need to find the x and y coordinate of city i
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]

            for j in range(self.city_count):
                # x and y coordinate of city j
                x2 = self.coordinates[j][0]
                y2 = self.coordinates[j][1] 

                #using the Pythagorean theorem to calculate the distance 
                distances[i][j] =  (math.sqrt(((float(x2)-float(x))**2) + ((float(y2)-float(y))**2)))

        self.distance_matrix = distances

    def push_best_individual(self, best_individual):
        self.best_individuals.append(best_individual)
        self.best_distances.append(best_individual.distance)

    def get_distance_between(self, city1,city2):
        return self.distance_matrix[city1-1][city2-1]


