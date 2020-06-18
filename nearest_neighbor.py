# Insert each point into the tour after the closest point that is already in the tour.
# not yet tried with each possible starting city
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


def solve(cities):
    N = len(cities)
    dist = [[0] * N for i in range(N)]

    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    # print(dist)


    current_city = 0
    unvisited_cities = list(range(1, N))

    # always starting with the zero-th city
    tour = [current_city]

    # compare current node with each node in the tour
    # pick the node which is closest to current node
    # connect it to the closest node
    while unvisited_cities:
        # print(unvisited_cities)
        if len(tour) == 1:
            next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
            unvisited_cities.remove(next_city)
            tour.append(next_city)
        else:
            current_node = unvisited_cities[0]
            closest_node = min(tour, key=lambda city: dist[current_node][city])
            tour.insert((tour.index(closest_node))+1, current_node)
            unvisited_cities.remove(current_node)

    # print(path_length(tour, cities))

    # print(tour)
    return two_opt.two_opt(cities, tour)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)
