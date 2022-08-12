# advent of code 2021
# https://adventofcode.com/2021
# day 06
import logging
from collections import Counter

import numpy as np
from numpy.typing import NDArray
from numba import njit, prange
from funcy import print_durations


def parse_input(lines):
    initial = np.fromstring(lines[0], dtype=np.int8, sep=',')
    return initial


def run(data: NDArray[np.int8], n: int) -> int:
    fishes = dict(Counter(data))
    for _ in range(1, n + 1):
        fishes = {lf: (0 if fishes.get(lf + 1) is None else fishes.get(lf + 1)) for lf in range(-1, 8)}
        # make all 8s -1 because we create new fish with 8 after it reaches 0
        fishes[8] = fishes[-1]
        # add new lives to that are exhausted
        fishes[6] += fishes[-1]
        # reset exhausted lives
        fishes[-1] = 0
    return sum(fishes.values())


@print_durations
def part1(data: NDArray[np.int8]) -> int:
    return run(data, n=80)


@print_durations
def part2(data: NDArray[np.int8]) -> int:
    return run(data, n=256)
