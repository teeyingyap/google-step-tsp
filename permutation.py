#!/usr/bin/env python3

# find minimum path length within all permutations 
# can only be used for small number of cities
# MemoryError when used with input_2.csv and above

import sys
import math
from itertools import permutations
from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i - 1]]) 
               for i in range(len(tour)))


def solve(cities):
    N = len(cities)
    all_tours = list(permutations(range(N)))
    num_of_perm = len(all_tours)
    all_path_length = [0] * num_of_perm

    for i in range(num_of_perm):
        all_path_length[i] = path_length(list(all_tours[i]), cities)

    perm_index = set(range(num_of_perm))
    min_perm_index = min(perm_index, key=lambda path:all_path_length[path])
    print(all_path_length[min_perm_index])
    return all_tours[min_perm_index]



if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
