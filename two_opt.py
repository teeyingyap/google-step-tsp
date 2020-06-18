#!/usr/bin/env python3

import math

def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i - 1]]) 
               for i in range(len(tour)))
    

def two_opt_swap(tour, i, j):
    # print(i, j)
    while j - i > 0:
        temp = tour[i]
        tour[i] = tour[j]
        tour[j] = temp
        i += 1
        j -= 1
    # print(tour)
    return tour


def hasShorterPath(cities, tour, a, b, c, d):
    if (distance(cities[tour[a]], cities[tour[b]]) + distance(cities[tour[c]], cities[tour[d]])) > (distance(cities[tour[a]], cities[tour[c]]) + distance(cities[tour[b]], cities[tour[d]])):
        return True
    return False


def two_opt(cities, tour):
    N = len(cities)
    iteration = 0
    while iteration < 100:
           
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
    # print(iteration)
    print(path_length(tour, cities))
    return tour
