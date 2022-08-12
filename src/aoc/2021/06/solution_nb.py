# advent of code 2021
# https://adventofcode.com/2021
# day 06
import numpy as np
from numpy.typing import NDArray
from numba import njit, prange
from funcy import print_durations


@njit(cache=True, fastmath=True, parallel=True)
def iteration(fishes: NDArray[np.int8]):
    new_fishes = 0
    for i in prange(fishes.shape[0]):
        # If at 0, reset to 6, log new fish
        if fishes[i] == 0:
            fishes[i] = 6
            new_fishes += 1
        # Other cases, just decrement
        else:
            fishes[i] -= 1
    # Create and concat new fishes, start with timer of 8
    if new_fishes > 0:
        new_fishes = np.full(new_fishes, 8, dtype=np.int8)
        return np.concatenate((fishes, new_fishes))
    else:
        return fishes


def parse_input(lines):
    initial = np.fromstring(lines[0], dtype=np.int8, sep=',')
    return initial


@print_durations
def part1(data: NDArray[np.int8]) -> int:
    n = 80
    for _ in range(n):
        data = iteration(data)
    return data.shape[0]


@print_durations
def part2(data: NDArray[np.int8]) -> int:
    n = 256
    for _ in range(n):
        data = iteration(data)
    return data.shape[0]
