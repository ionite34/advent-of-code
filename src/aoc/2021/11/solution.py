# advent of code 2021
# https://adventofcode.com/2021
# day 11

import numpy as np
from scipy.ndimage import convolve

NEIGHBORS = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])


def parse_input(lines) -> np.matrix:
    mat = np.matrix(';'.join(' '.join(s) for s in lines), dtype=np.int16)
    return mat


def run(data: np.matrix, cycles: int) -> tuple[int, list]:
    print(f"Before Steps:\n{data}")
    flashes = 0
    all_flashes = []  # Steps where all cells were zero (flashed)
    for i in range(cycles):
        # First add 1 to all cells
        data += 1
        while np.any(data > 9):  # Loop until no more changes
            # For all cells that are 10, these are 'flashing' cells
            # Do convolution to raise all adjacent cells by 1
            flashing = (data > 9)
            data += convolve(
                flashing.astype(np.int16),
                NEIGHBORS,
                mode='constant',
            )
            # print(f"Flashing {i}:\n{data}")
            # Set all flashed cells to -100
            data[flashing] = -100

        # Set all flashed cells (<0) to 0
        flashes += np.sum(data < 0)
        data[data < 0] = 0

        # Detect all flashes
        if np.all(data == 0):
            all_flashes.append(i+1)

        print(f"=-=-=\nAfter Step {i+1}:\n{data}")
    print(f"All flash at: {all_flashes}")
    return flashes, all_flashes


def part1(data: np.matrix) -> int:
    return run(data.copy(), 100)[0]


def part2(data: np.matrix) -> int:
    return run(data.copy(), 370)[1][0]
