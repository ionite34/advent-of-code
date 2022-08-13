from __future__ import annotations

import numpy as np
import numpy.ma as ma

DATA = """
2199943210
3987894921
9856789892
8767896789
9899965678
"""


def parse_input() -> np.matrix:
    s = '; '.join(' '.join(line) for line in DATA.strip().split())
    mat = np.matrix(s, dtype=np.int8)
    return mat


def part1(data: np.matrix):
    # Expand the matrix with surrounding of 100
    padded = np.pad(data, pad_width=1, mode='constant', constant_values=100)

    print(padded)
    return


if __name__ == "__main__":
    print(part1(parse_input()))
