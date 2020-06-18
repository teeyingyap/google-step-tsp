#!/usr/bin/env python3

import sys
import math
import two_opt

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i - 1]]) 
               for i in range(len(tour)))


def try_all_possible_starting_city(cities):
    N = len(cities)
    numOfCities = N
    isTryAll = input("Run the algorithm with each possible starting city? (y/n) ")

    if isTryAll.lower() != "y":
        numOfCities = 1

    dist = [[0] * N for i in range(N)]
    # print(dist)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    solutions = {}
    for start_index in range(numOfCities):
        tour = solve(cities, start_index, dist)
        solutions[path_length(tour, cities)] = tour
        print("Path length", path_length(tour, cities))
    print(min(solutions))
    return solutions[min(solutions)]



def solve(cities, k, dist):
    N = len(cities)

    current_city = k
    unvisited_cities = []
    for i in range(N):
        if i != k:
            unvisited_cities.append(i)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    # print(tour)
    return two_opt.two_opt(cities, tour)




if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = try_all_possible_starting_city(cities)
    print_tour(tour)
