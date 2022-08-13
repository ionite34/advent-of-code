# advent of code 2021
# https://adventofcode.com/2021
# day 09
from __future__ import annotations

import numpy as np
import numpy.ma as ma

from scipy.ndimage import label


def parse_input(lines: list[str]):
    s = '; '.join(' '.join(line) for line in lines)
    mat = np.matrix(s, dtype=np.int8)
    return mat


def part1(data: np.matrix):
    # Expand the matrix with surrounding of 100
    padded = np.pad(data, pad_width=1, mode='constant', constant_values=100)

    result = ((padded[1:-1, 0:-2] - data > 0) &
              (padded[1:-1, 2:] - data > 0) &
              (padded[0:-2, 1:-1] - data > 0) &
              (padded[2:, 1:-1] - data > 0))

    masked = ma.masked_where(~result, data)
    # Add 1 to all values not masked
    masked += 1
    return masked.sum()


def part2(data: np.matrix) -> int:
    mask = data != 9
    labeled, num_features = label(mask)
    labeled = labeled.flatten()
    areas = np.bincount(labeled, weights=(labeled != 0))
    print(f"P2 | Areas:\n{areas}")
    # Get the 3 largest areas
    selection = np.sort(areas)[-3:]
    print(f"P2 | 3 Largest:\n{selection}")
    # Multiply areas for result
    return int(np.prod(selection))

