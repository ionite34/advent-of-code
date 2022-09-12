# advent of code 2015
# https://adventofcode.com/2015
# day 18
import numpy as np
from scipy.ndimage import convolve

MASK = np.array([[1, 1, 1], [1, 0, 1], [1, 1, 1]], dtype=np.uint8)


def parse_input(lines) -> np.ndarray:
    grid = np.fromiter(
        (1 if c == "#" else 0 for c in "".join(lines)),
        dtype=np.uint8,
    ).reshape((len(lines), -1))
    return grid


def part1(grid: np.ndarray) -> int:
    for i in range(100):
        conv = convolve(grid, MASK, mode="constant")
        r1 = np.where((conv != 2) & (conv != 3) & grid, 0, grid)
        grid = np.where((conv == 3) & ~grid, 1, r1)

    return grid.sum()


def part2(grid: np.ndarray) -> int:
    corners = [0, 0, -1, -1], [0, -1, 0, -1]
    grid[corners] = 1
    for i in range(100):
        conv = convolve(grid, MASK, mode="constant")
        r1 = np.where((conv != 2) & (conv != 3) & grid, 0, grid)
        grid = np.where((conv == 3) & ~grid, 1, r1)
        grid[corners] = 1

    return grid.sum()
