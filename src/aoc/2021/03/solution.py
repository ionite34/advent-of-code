# advent of code 2021
# https://adventofcode.com/2021
# day 03
from collections.abc import Iterator

import numpy as np
from scipy import stats

from aoc.tools import inter_bin


def parse_input(lines: list[str]) -> np.ndarray:
    total = None
    for line in lines:
        # Get a map of ints per line [0, 0, 1, 0, 0]
        ls = map(int, list(line))
        # Convert to numpy array
        arr = np.fromiter(ls, dtype=np.int8)
        # Stack arrays
        total = np.vstack([total, arr]) if total is not None else arr

    return total


def part1(data: np.ndarray) -> int:
    # Get the most common value in columns
    col_modes = stats.mode(data, axis=0, keepdims=True)
    # Interpret as int
    gamma, epsilon = inter_bin(col_modes[0])
    return gamma * epsilon


def common_find(data: np.ndarray, tie: int, least: bool = False) -> np.ndarray | None:
    """
    Find row using most / least common value in each column

    Args:
        data: 2D array
        tie: Int to use if there is a tie in frequency
        least: If true, find least common value
    """
    columns = data.shape[1]
    # Loop columns
    for i in range(columns):
        # Get most common value in column
        col_mode_result = stats.mode(data[:, i], axis=0, keepdims=True)
        mode = col_mode_result[0][0]
        freq = col_mode_result[1][0]
        # Count lengths
        rows = data.shape[0]
        # If least, find least common value
        if least:
            mode = 1 - mode
        # If equal, use tie value
        if freq == rows // 2:
            mode = tie
        # Make mask
        mask = data[:, i] == mode
        # Set data using mask
        data = data[mask]
        # If only one row, return it
        if data.shape[0] == 1:
            return data[0].astype(np.int64)


def part2(data: np.ndarray) -> int:
    rows = data.shape[0]
    columns = data.shape[1]
    print(f"{rows=}, {columns=}")

    # Find oxygen generator rating
    oxygen = common_find(data, 1)
    print(f"{oxygen=}")
    # Convert to decimal
    oxygen = inter_bin(oxygen)[0]
    print(f"Decimal: {oxygen=}")

    # Find CO2 scrubber rating
    scrubber = common_find(data, 0, least=True)
    print(f"{scrubber=}")
    # Convert to decimal
    scrubber = inter_bin(scrubber)[0]
    print(f"Decimal: {scrubber=}")

    # Result is product of oxygen and scrubber
    return oxygen * scrubber




