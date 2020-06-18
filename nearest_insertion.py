# Insert each node into the tour where it would cause the smallest increase in the tour distance.

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
    # attempt farthest insertion
    # step 1: start with a subtour which contains arbitrary starting node
    # step 2: find the farthest node from sub tour


    current_city = k
    unvisited_cities = []
    for i in range(N):
        if i != k:
            unvisited_cities.append(i)


    sub_tour = [current_city]
    
    next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
    # print(next_city)
    sub_tour.append(next_city)
    unvisited_cities.remove(next_city)
    sub_tour.append(current_city)
    # print(sub_tour)
    # here, sub_tour = [A, B, A]
    # find node k not in the subtour which is farthest from any node in the sub-tour
    while unvisited_cities:
        # selection step
        curr_node_r = min(unvisited_cities, key=lambda city: dist[city][sub_tour[0]])
        for i in range(1, len(sub_tour)):
            new_node_r = min(unvisited_cities, key=lambda city: dist[city][i])
            if new_node_r < curr_node_r:
                curr_node_r = new_node_r
        # print(curr_node_r)
        # insertion step
        # Find the edge (i, j) in the subtour which minimizes cir + crj - cij

        f = distance(cities[sub_tour[0]], cities[curr_node_r]) 
        + distance(cities[curr_node_r], cities[sub_tour[0 + 1]]) 
        - distance(cities[sub_tour[0]], cities[sub_tour[0 + 1]])
        insert_index = 0
        for i in range(len(sub_tour) - 1):
            if i == N - i - 1:
                continue
            new_f = distance(cities[sub_tour[i]], cities[curr_node_r]) 
            + distance(cities[curr_node_r], cities[sub_tour[i + 1]]) 
            - distance(cities[sub_tour[i]], cities[sub_tour[i + 1]])
            if new_f < f:
                f = new_f
                insert_index = i

        unvisited_cities.remove(curr_node_r)
        sub_tour.insert(insert_index + 1, curr_node_r)
        # print(sub_tour)

    tour = sub_tour[:-1]
    return two_opt.two_opt(cities, tour)


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = try_all_possible_starting_city(cities)
    print_tour(tour)
