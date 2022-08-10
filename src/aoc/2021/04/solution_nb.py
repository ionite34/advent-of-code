# advent of code 2021
# https://adventofcode.com/2021
# day 04
from __future__ import annotations

import time
from itertools import groupby, product
from functools import partial

import numpy as np
import re

from numba import njit


def parse_input(lines: list[str]) -> tuple[np.ndarray, np.ndarray]:
    turns = np.fromstring(lines[0], sep=',', dtype=int)

    # Split boards
    lines = lines[2:]
    split_boards = [
        list(y)
        for x, y in groupby(
            lines,
            lambda d: d in ('', '\n'),
        ) if not x
    ]
    # Join with ; to get matrix
    boards = np.array([*map(
        # Remove multiple spaces
        lambda x: np.mat(
            re.sub(' +', ' ', ';'.join(x)),
            dtype=int,
        ),
        split_boards,
    )])

    # print(boards)

    return turns, boards


@njit(parallel=True)
def part1_nb(turns: np.ndarray, boards: np.ndarray) -> int:
    # Play bingo!
    draw: int
    board: np.matrix
    for draw in turns:
        for board in boards:
            # Check for win
            rows = board.shape[0]
            cols = board.shape[1]
            for row in range(rows):
                for item in range(cols):
                    if board[row, item] == draw:
                        # Replace with -1 if match
                        board[row, item] = -1

            # Get a mask where there is a win
            mask = board == -1
            if np.any(mask.sum(0) == 5) or np.any(mask.sum(1) == 5):
                result = board.sum() * draw
                return result


def part1(turns: np.ndarray, boards: np.ndarray) -> int | None:
    s = time.perf_counter()
    result = part1_nb(turns, boards)
    e = time.perf_counter() - s
    print(f"Part 1: {result} in {e * 1000:.4f}ms")
    return result


def part2(turns: np.ndarray, boards: np.ndarray):
    pass
