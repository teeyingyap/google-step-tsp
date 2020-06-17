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
    print(i, j)
    while j - i > 0:
        temp = tour[i]
        tour[i] = tour[j]
        tour[j] = temp
        i += 1
        j -= 1
    print(tour)
    return tour


def hasShorterPath(cities, tour, a, b, c, d):
    if (distance(cities[tour[a]], cities[tour[b]]) + distance(cities[tour[c]], cities[tour[d]])) > (distance(cities[tour[a]], cities[tour[c]]) + distance(cities[tour[b]], cities[tour[d]])):
        return True
    return False


def two_opt(cities):
    N = len(cities)

    iteration = 0
    tour = solve(cities)
    while iteration < 500:
           
        for i in range(0, N):
            # a-b is the edge to compare
            a = i
            b = (i + 1) % N # can be zero so we mod by N
            for j in range(i + 2, N):
                if (j + 1) % N == i:
                    # no point swapping connecting edges
                    continue

                # c-d is the edge we want to check
                c = j % N # can be zero so we mod by N
                d = (j + 1) % N
                if hasShorterPath(cities, tour, a, b, c, d):
                    tour = two_opt_swap(tour, i + 1, j)
        iteration += 1
    print(iteration)
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
