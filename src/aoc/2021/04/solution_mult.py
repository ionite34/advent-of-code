# advent of code 2021
# https://adventofcode.com/2021
# day 04
from __future__ import annotations

import time
from concurrent.futures import ThreadPoolExecutor
from itertools import groupby, product
from functools import partial

import numpy as np
import re


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
    boards = np.ndarray([*map(
        # Remove multiple spaces
        lambda x: np.ma.masked_array(np.mat(
            re.sub(' +', ' ', ';'.join(x)),
            dtype=int,
        )),
        split_boards,
    )])

    return turns, boards


def solve_bingo(board: np.ma.masked_array, turn: int) -> np.ma.masked_array | None:
    board.mask |= board.data == turn
    if np.any(board.mask.sum(0) == 5) or np.any(board.mask.sum(1) == 5):
        # Return masked_array if win
        return board
    # Otherwise return None
    return None


def part1(turns: np.ndarray, boards: np.ndarray) -> int | None:
    # Play bingo!
    s = time.perf_counter()
    draw: int
    board: np.matrix
    with ThreadPoolExecutor() as executor:
        for turn in turns:
            solve_turn = partial(solve_bingo, turn=turn)
            futures = executor.map(solve_turn, boards)
            for future in futures:
                if future is not None:
                    # If win
                    e = time.perf_counter() - s
                    print(f"in {e * 1000:.4f}ms")
                    return future.sum() * turn


def part2(turns: np.ndarray, boards: np.ndarray):
    pass
