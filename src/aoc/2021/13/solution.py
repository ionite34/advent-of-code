# advent of code 2021
# https://adventofcode.com/2021
# day 13
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import seaborn as sns
from funcy import print_durations
from matplotlib import pyplot as plt
from numpy import ma
from rich.console import Console

here = Path(__file__).parent

console = Console()

verbose = False


def mat_print(matrix: np.ndarray, title: str | None = None) -> None:
    if not verbose:
        return
    matrix = matrix.astype(np.uint8)
    mask = ma.masked_where(matrix == 0, matrix)
    if title:
        console.print(f"|> {title}:")
    console.print(str(mask).replace('1', '01'))


def find_max(lines: str) -> tuple[int, int]:
    max_x = max(map(int, re.findall(r"(\d+),", lines))) + 1
    max_y = max(map(int, re.findall(r",(\d+)", lines))) + 1
    console.print(f"Max X: {max_x}, Max Y: {max_y}")
    return max_x, max_y


def parse_input(lines: list[str]) -> tuple[np.ndarray, list[tuple[int, int]]]:
    max_x, max_y = find_max("\n".join(lines))
    matrix = np.zeros((max_y, max_x), dtype=bool)
    folds: list[tuple[int, int]] = []
    for line in lines:
        if 'fold' in line:
            match = re.search(r'(\w+)=(\d+)', line)
            sym, val = match.group(1), int(match.group(2))  # type: ignore
            folds.append((0, val) if sym == 'y' else (1, val))
        elif line:
            x, y = map(int, line.split(','))
            matrix[y, x] = 1
    return matrix, folds


def fold(matrix: np.ndarray, axis: int, cord: int) -> np.ndarray:
    side_a = matrix[:, :cord] if axis else matrix[:cord, :]
    side_b = matrix[:, cord + 1:] if axis else matrix[cord + 1:, :]

    mat_print(side_a, "Upper")
    mat_print(side_b, "Lower")

    # Flip the lower view
    side_b = np.flip(side_b, axis=axis)
    mat_print(side_b, "Flipped Lower")

    # Merge the upper and lower views
    result = side_a | side_b
    mat_print(result, "Merged")

    return result


@print_durations
def part1(matrix: np.ndarray, folds: list[tuple[int, int]]) -> int:
    matrix = matrix.copy()
    mat_print(matrix)
    # Get first fold
    axis, scale = folds[0]
    matrix = fold(matrix, axis=axis, cord=scale)

    return np.count_nonzero(matrix)


@print_durations
def part2(matrix: np.ndarray, folds: list[tuple[int, int]]) -> int:
    matrix = matrix.copy()
    mat_print(matrix)
    # Iterate folds
    for axis, scale in folds:
        matrix = fold(matrix, axis=axis, cord=scale)

    if verbose:
        _ = sns.heatmap(matrix, cmap="YlGnBu")
        plt.savefig(here / "part2.png")

    return np.count_nonzero(matrix)
