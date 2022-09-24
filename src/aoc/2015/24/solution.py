# advent of code 2015
# https://adventofcode.com/2015
# day 24
from itertools import combinations
import numpy as np


def parse_input(lines):
    return [*map(int, lines)]


def iter_weights(data: list[int], groups: int):
    target = sum(data) // groups
    for n in range(1, len(data)):
        comb = combinations(data, n)
        if res := [*filter(lambda x: sum(x) == target, comb)]:
            return res


def part1(data):
    group1 = min(iter_weights(data, 3), key=np.prod)
    return np.prod(group1)


def part2(data):
    group1 = min(iter_weights(data, 4), key=np.prod)
    return np.prod(group1)
