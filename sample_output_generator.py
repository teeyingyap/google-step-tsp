#!/usr/bin/env python3

from common import format_tour, read_input

import solver_greedy
import solver_random
import permutation
import nearest_insertion

CHALLENGES = 7
BRUTE_FORCE_CHALLENGES = 2
NEAREST_INSERTION_CHALLENGES = 6

def generate_sample_output():
    for i in range(CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        for solver, name in ((solver_random, 'random'), (solver_greedy, 'greedy')):
            tour = solver.solve(cities)
            with open(f'sample/{name}_{i}.csv', 'w') as f:
                f.write(format_tour(tour) + '\n')


def generate_permutation_output():
    for i in range(BRUTE_FORCE_CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = permutation.solve(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')


def generate_nearest_insertion_output():
    for i in range(BRUTE_FORCE_CHALLENGES, NEAREST_INSERTION_CHALLENGES):
        cities = read_input(f'input_{i}.csv')
        tour = nearest_insertion.two_opt(cities)
        with open(f'output_{i}.csv', 'w') as f:
            f.write(format_tour(tour) + '\n')



if __name__ == '__main__':
    # generate_sample_output()
    # generate_permutation_output()
    # generate_nearest_insertion_output()
