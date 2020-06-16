#!/usr/bin/env python3

# greedy algorithm with random starting point

import sys
import math
from random import randint

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def solve(cities):
    print(cities)
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    print(dist)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    print(dist)


    current_city = randint(0, N-1)
    unvisited_cities = []
    for i in range(N):
        if i != current_city:
            unvisited_cities.append(i)

    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    print(tour)
    return tour