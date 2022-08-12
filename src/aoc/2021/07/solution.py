# advent of code 2021
# https://adventofcode.com/2021
# day 07
import numpy as np
from numpy.typing import NDArray


def parse_input(lines: list[str]) -> NDArray[int]:
    nums = map(int, lines[0].split(','))
    return np.fromiter(nums, dtype=int)


def part1(data: NDArray) -> int:
    # Find median
    median = np.median(data)
    print(f'P1 | Median: {median}')
    # Calculate fuel use
    fuel = np.sum(np.abs(data - median))
    return int(fuel)


def part2(data: NDArray) -> int:
    # Find mean, get floor int
    np_mean = float(np.mean(data))
    mean = int(np_mean)
    print(f'P2 | Mean: ({np_mean}) -> {mean}')
    # Calculate fuel use
    diffs = np.abs(data - mean)
    sums = (diffs * (diffs + 1)) // 2
    fuel = int(np.sum(sums))
    return int(fuel)
