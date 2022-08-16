# advent of code 2021
# https://adventofcode.com/2021
# day 11
import logging

import numpy as np
import numpy.ma as ma
from funcy import print_durations
from numba import njit
from scipy.ndimage import convolve

NEIGHBORS = np.array([
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1]
])

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def parse_input(lines) -> ma.MaskedArray:
    mat = np.matrix(';'.join(' '.join(s) for s in lines), dtype=np.int16)
    return ma.masked_array(mat)


def run(data: ma.MaskedArray, cycles: int) -> tuple[int, list]:
    log.info(f"Before Steps:\n{data}")
    flashes = 0
    all_flashes = []  # Steps where all cells were zero (flashed)
    for i in range(cycles):
        data += 1
        while np.any(flashing := (data > 9 & ~data.mask)):  # Loop until no changes
            data += convolve(flashing.astype(np.int16), NEIGHBORS, mode='constant')
            data.mask |= flashing

        if data.mask.all():  # All flashed states
            all_flashes.append(i + 1)

        flashes += np.count_nonzero(data.mask)
        data.data[data.mask] = 0  # Set masked to 0
        data.mask = False  # Reset mask

        log.info(f"=-=-=\nAfter Step {i + 1}:\n{data}")
    log.info(f"All flash at: {all_flashes}")
    return flashes, all_flashes


@print_durations
def part1(data: ma.MaskedArray) -> int:
    return run(data.copy(), 100)[0]


@print_durations
def part2(data: ma.MaskedArray) -> int:
    return run(data.copy(), 370)[1][0]
