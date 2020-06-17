# Smallest-Increase Heuristic: 
# Insert each point into the tour where it would cause the smallest increase in the tour distance.
import sys
import math
from random import randint

from common import print_tour, read_input


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


def two_opt(cities):
    N = len(cities)
    solutions = {}
    for start_index in range(N):
        iteration = 0
        tour = solve(cities, start_index)
        while iteration < 10:
               
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
        solutions[path_length(tour, cities)] = tour
        print("Path length", path_length(tour, cities))
    print(min(solutions))
    return solutions[min(solutions)]




def solve(cities, k):
    # attempt farthest insertion
    # step 1: start with a subtour which contains arbitrary starting node
    # step 2: find the farthest node from sub tour
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    # print(dist)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    # print(dist)


    # current_city = 0
    # unvisited_cities = list(range(1, N))
    # current_city = randint(0, N-1)
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
    print(path_length(tour, cities))
    return tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    # tour = solve(cities)
    tour = two_opt(cities)
    print_tour(tour)
