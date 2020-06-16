#!/usr/bin/env python3

import sys
import math
import random

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


def two_opt(cities):
    N = len(cities)

    iteration = 0
    while iteration < 1000:
        tour = solve(cities)
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
        iteration += 1
        if path_length(tour, cities) < 4500:
            print(path_length(tour, cities))
            return tour
    print(path_length(tour, cities))
    return tour


def choose_a_random_neighbor(dist, cities, current_city, unvisited_cities):
    sorted_cities = sorted(unvisited_cities, key=lambda city: dist[current_city][city])
    next_cities = sorted_cities[:3] # nearest n items
    return random.choice(next_cities)


def solve(cities):
    print(cities)
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    print(dist)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    print(dist)


    # current_city = random.randint(0, N-1)
    # unvisited_cities = []
    # for i in range(N):
    #     if i != current_city:
    #         unvisited_cities.append(i)

    current_city = 0
    unvisited_cities = set(range(1, N))
    # always starting with the zero-th city
    tour = [current_city]

    while unvisited_cities:
        next_city = choose_a_random_neighbor(dist, cities, current_city, unvisited_cities)
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    print(tour)
    return tour



if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = two_opt(cities)
    print_tour(tour)
