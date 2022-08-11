# advent of code 2021
# https://adventofcode.com/2021
# day 04
from __future__ import annotations

import re
from itertools import groupby, product

import numpy as np
from funcy import print_durations


def parse_input(lines: list[str]) -> tuple[np.ndarray, list[np.ma.masked_array]]:
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
    boards = [*map(
        # Remove multiple spaces
        lambda x: np.ma.masked_array(np.mat(
            re.sub(' +', ' ', ';'.join(x)),
            dtype=int,
        )),
        split_boards,
    )]

    return turns, boards


@print_durations
def part1(turns: np.ndarray, boards: list[np.ma.masked_array]) -> int:
    # Play bingo!
    draw: int
    board: np.matrix
    for draw, board in product(turns, boards):
        board.mask |= board.data == draw
        if np.any(board.mask.sum(0) == 5) or np.any(board.mask.sum(1) == 5):
            # For win
            result = board.sum() * draw
            return result


@print_durations
def part2(turns: np.ndarray, boards: list[np.ma.masked_array]) -> int:
    # We want to find the board that will win last
    wins = set()  # indexes of boards that already won
    last_win_score = None
    draw: int
    board: np.matrix
    for draw, (i, board) in product(turns, enumerate(boards)):
        if i in wins:
            continue
        board.mask |= board.data == draw
        if np.any(board.mask.sum(0) == 5) or np.any(board.mask.sum(1) == 5):
            # For win, set last win
            result = board.sum() * draw
            last_win_score = result
            # Add to wins
            wins.add(i)

    return last_win_score
