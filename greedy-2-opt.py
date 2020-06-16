#!/usr/bin/env python3

import sys
import math
import solver_greedy

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i - 1]]) 
               for i in range(len(tour)))


def two_opt_swap(tour, i, j):
    new_tour = tour[0:i]
    new_tour.extend(tour[j-1:i-1:-1])
    new_tour.extend(tour[j:])
    print(new_tour)
    return new_tour


def two_opt(tour, cities):
    N = len(cities)


    current_path_length = path_length(tour, cities)
    for i in range(1, N - 1):
        for j in range(i + 1, N):
            if j - 1 == i:
                continue
            new_tour = two_opt_swap(tour, i, j)
            new_path_length = path_length(new_tour, cities)
            if new_path_length < current_path_length:
                tour = new_tour
                current_path_length = new_path_length

    print(path_length(tour, cities))
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solver_greedy.solve(cities)
    optimized_tour = two_opt(tour, cities)
    print_tour(tour)
