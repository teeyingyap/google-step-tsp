# Smallest-Increase Heuristic: 
# Insert each point into the tour where it would cause the smallest increase in the tour distance.
import sys
import math

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)


def path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i - 1]]) 
               for i in range(len(tour)))

def new_path_length(tour, cities):
    return sum(distance(cities[tour[i]], cities[tour[i + 1]]) 
               for i in range(len(tour) - 1))



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




def solve(cities):
    # attempt farthest insertion
    # step 1: start with a sub tour which contains arbitrary starting node
    # step 2: find the farthest node from sub tour

    print(cities)
    N = len(cities)

    dist = [[0] * N for i in range(N)]
    print(dist)
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    print(dist)


    current_city = 0
    sub_tour = [current_city]
    unvisited_cities = list(range(1, N))
    next_city = max(unvisited_cities,
                        key=lambda city: dist[current_city][city])
    print(next_city)
    sub_tour.append(next_city)
    unvisited_cities.remove(next_city)
    sub_tour.append(current_city)
    print(sub_tour)
    # here, sub_tour = [A, B, A]
    # find node r not in the sub-tour farthest from any node in the sub-tour; i.e. with maximal crj
    while len(sub_tour) < N + 1:
        # selection step
        curr_node_r = max(unvisited_cities, key=lambda city: dist[city][sub_tour[0]])
        for i in range(1, len(sub_tour)):
            new_node_r = max(unvisited_cities, key=lambda city: dist[city][i])
            if new_node_r > curr_node_r:
                curr_node_r = new_node_r
        print(curr_node_r)
        # insertion step
        # Find the edge (i, j) in the subtour which minimizes cir + crj - cij
        f = distance(cities[sub_tour[0]], cities[curr_node_r]) 
        + distance(cities[curr_node_r], cities[sub_tour[0 + 1]]) 
        - distance(cities[sub_tour[0]], cities[sub_tour[0 + 1]])
        insert_index = 0
        for i in range(0, len(sub_tour) - 1):
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
        print(sub_tour)

    print(sub_tour)


    print(new_path_length(sub_tour, cities))
    return sub_tour


if __name__ == '__main__':
    assert len(sys.argv) > 1
    cities = read_input(sys.argv[1])
    tour = two_opt(cities)
    print_tour(tour)
