# advent of code 2015
# https://adventofcode.com/2015
# day 02
import numpy as np
from numpy.typing import NDArray


def parse_input(lines) -> np.ndarray:
    form = ';'.join(lines).replace('x', ' ')
    mat = np.matrix(form)
    return np.asarray(mat)


def part1(data: NDArray) -> int:
    # Area (wl + hl + wh) * 2
    areas = np.array([data[:, 0] * data[:, 1], data[:, 0] * data[:, 2], data[:, 1] * data[:, 2]])
    # Extra wrappers: lowest area of each box
    min_face = np.min(areas.T, axis=1)

    return int(np.sum(2 * areas) + min_face.sum())


def part2(data: NDArray) -> int:
    perimeter = 2 * np.array([data[:, 0] + data[:, 1], data[:, 0] + data[:, 2], data[:, 1] + data[:, 2]])
    volume = np.prod(data, axis=1)
    return int(np.min(perimeter.T, axis=1).sum() + volume.sum())

