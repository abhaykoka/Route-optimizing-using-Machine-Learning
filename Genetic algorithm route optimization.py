'''
1. Agra
2. Ahmedabad
3. Bengaluru
4. Bhubaneswar
5. Chennai
6. Delhi
7. Goa
8. Hyderabad
9. Jaipur
10. Kanpur
11. Kochi
12. Kolkata
13. Lucknow
14. Mumbai
15. Patna
16. Pune
17. Udaipur
18. Varanasi
19. Vishakhapatnam
'''
'''
sample input
------
6
Agra
Bengaluru, Chennai, Delhi, Hyderabad, Jaipur, Mumbai
'''
import numpy as np
import pandas as pd

# Load the dataset
data = pd.read_csv("indian-cities-dataset.csv")

# Define genetic algorithm parameters
population_size = 50
mutation_rate = 0.01
num_generations = 100


# Define functions for genetic operations
def initialize_population(data, population_size):
    # Randomly initialize population
    population = [np.random.permutation(data.shape[0]) for _ in range(population_size)]
    return population


def calculate_fitness(individual, data):
    # Calculate total distance for the individual's route
    distance = sum(data.iloc[individual[i], 2] for i in range(len(individual)))

    # Handle division by zero and very small distances
    if distance == 0:
        fitness = float('inf')  # Assign a very large fitness value
    else:
        fitness = 1 / distance

    return fitness


def selection(population, data):
    # Select parents based on tournament selection
    parents = []
    for _ in range(len(population)):
        tournament = np.random.choice(len(population), size=5, replace=False)
        best_individual = max(tournament, key=lambda x: calculate_fitness(population[x], data))
        parents.append(population[best_individual])
    return parents


def crossover(parents):
    # Perform crossover using ordered crossover
    offspring = []
    for i in range(0, len(parents) - 1, 2):  # Adjust loop range to avoid accessing out-of-range indices
        parent1, parent2 = parents[i], parents[i + 1]
        if len(parent1) < 1:
            continue  # Skip crossover if the parent chromosome is empty
        crossover_point = np.random.randint(1, len(parent1))
        child1 = list(parent1[:crossover_point])
        child2 = [gene for gene in parent2 if gene not in child1]
        offspring.extend([child1 + child2, child2 + child1])
    return offspring


def mutate(offspring, mutation_rate):
    # Perform mutation by swapping two genes with a certain probability
    for individual in offspring:
        if np.random.random() < mutation_rate:
            idx1, idx2 = np.random.choice(len(individual), size=2, replace=False)
            individual[idx1], individual[idx2] = individual[idx2], individual[idx1]
    return offspring


print("Enter the number of destinations:")
num_destinations = int(input())
population_size = num_destinations + 1

print("Enter the starting city:")
starting_city = input()

print("Enter the list of cities you want to travel to (separated by commas):")
city_list = input().split(',')

# Filter city_list to remove consecutive duplicate cities
filtered_city_list = [city_list[0]]  # Add the first city
for city in city_list[1:]:
    if city != filtered_city_list[-1]:  # Check if the city is different from the preceding city
        filtered_city_list.append(city)

# Filter data to include only the selected destinations and starting city
filtered_data = data[data['Origin'].isin([starting_city] + filtered_city_list)]

# Main genetic algorithm loop
population = initialize_population(filtered_data, population_size)
for generation in range(num_generations):
    # Selection
    parents = selection(population, filtered_data)
    # Crossover
    offspring = crossover(parents)
    # Mutation
    offspring = mutate(offspring, mutation_rate)
    # Replace population with offspring
    population = offspring

# Select the best individual from the final population
best_individual = max(population, key=lambda x: calculate_fitness(x, filtered_data))
best_route = [filtered_data.iloc[city, :2].values for city in best_individual]
best_distance = sum(filtered_data.iloc[best_individual[i], 2] for i in range(len(best_individual)))

# Sort city pairs based on distance
sorted_city_pairs = sorted(zip(best_route, [best_distance] * len(best_route)), key=lambda x: x[1])

print("Optimal Sequence of Cities:")
for city_pair, distance in sorted_city_pairs:
    print(f"From {city_pair[0]} to {city_pair[1]}")

print("Total Distance:", best_distance)


