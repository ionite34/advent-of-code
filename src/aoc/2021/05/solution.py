# advent of code 2021
# https://adventofcode.com/2021
# day 05
from __future__ import annotations

import time
from pathlib import Path
from dataclasses import dataclass
from typing import Iterable

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt

# Get the parent folder of this file
from funcy import print_durations
from numba import njit

PARENT_DIR = Path(__file__).resolve().parent

# Plotting mode
PLOT = False


@dataclass
class Line:
    origin_x: int
    origin_y: int
    dest_x: int
    dest_y: int

    def __str__(self):
        return f"{self.origin_x},{self.origin_y} -> {self.dest_x},{self.dest_y}"

    @property
    def is_parallel(self) -> bool:
        return self.dest_x == self.origin_x or self.dest_y == self.origin_y

    @property
    def range_x(self) -> tuple[int, int]:
        x_start = min(self.origin_x, self.dest_x)
        x_end = max(self.origin_x, self.dest_x)
        return x_start, x_end + 1

    @property
    def range_y(self) -> tuple[int, int]:
        y_start = min(self.origin_y, self.dest_y)
        y_end = max(self.origin_y, self.dest_y)
        return y_start, y_end + 1

    @property
    def all_cords(self) -> tuple[np.ndarray, np.ndarray]:
        x_pos = self.dest_x >= self.origin_x
        x_stride = 1 if x_pos else -1
        x_dest = self.dest_x + x_stride
        x_cords = range(self.origin_x, x_dest, x_stride)

        y_pos = self.dest_y >= self.origin_y
        y_stride = 1 if y_pos else -1
        y_dest = self.dest_y + y_stride
        y_cords = range(self.origin_y, y_dest, y_stride)

        result = (
            np.fromiter(x_cords, dtype=np.int32),
            np.fromiter(y_cords, dtype=np.int32),
        )
        # print(f"{self} | {list(zip(x_cords, y_cords))}")
        return result


def parse_input(lines: list[str]) -> tuple[list[str], int]:
    # Record maximums for building board
    max_cord = 0
    for line in lines:
        for x in line.split(' -> '):
            max_cord = max(max_cord, *{*map(int, x.split(','))})
    # Add 1 to max for index
    max_cord += 1
    # Return lines and max
    return lines, max_cord


@print_durations
def part1(data: list[str], max_cord: int) -> int:
    # Build board of max size matrix
    board = np.zeros((max_cord, max_cord), dtype=np.int8)
    for line in data:
        origin, dest = line.split(' -> ')
        line = Line(
            *map(int, origin.split(',')),
            *map(int, dest.split(',')),
        )
        # We require only vertical or horizontal lines
        if not line.is_parallel:
            continue
        # Update board
        y_s, y_e = line.range_y
        x_s, x_e = line.range_x
        board[y_s:y_e, x_s:x_e] += 1

    # Plot heatmap
    if PLOT:
        _ = sns.heatmap(board)
        plt.savefig(PARENT_DIR.joinpath('part1.png'))

    # Count values larger or equal to 2
    return np.count_nonzero(board >= 2)


@print_durations
def part2(data: list[str], max_cord: int) -> int:
    # Build board of max size matrix
    board = np.zeros((max_cord, max_cord), dtype=np.int8)
    x_cords: None | np.ndarray = None
    y_cords: None | np.ndarray = None
    for line in data:
        origin, dest = line.split(' -> ')
        line = Line(
            *map(int, origin.split(',')),
            *map(int, dest.split(',')),
        )
        if line.is_parallel:
            # Update board
            y_s, y_e = line.range_y
            x_s, x_e = line.range_x
            board[y_s:y_e, x_s:x_e] += 1
        else:
            # Get all cords, and update board
            a, b = line.all_cords
            x_cords = a if x_cords is None else np.concatenate((x_cords, a))
            y_cords = b if y_cords is None else np.concatenate((y_cords, b))

    cnt = np.bincount(x_cords * max_cord + y_cords)
    cnt.resize((max_cord, max_cord))
    board += cnt

    # Plot heatmap
    if PLOT:
        _ = sns.heatmap(board)
        plt.savefig(PARENT_DIR.joinpath('part2.png'))

    # Count values larger or equal to 2
    return np.count_nonzero(board >= 2)
