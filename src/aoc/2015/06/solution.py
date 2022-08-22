# advent of code 2015
# https://adventofcode.com/2015
# day 06
import re
import numpy as np
from funcy import print_durations

from aoc import log

log.setLevel("WARNING")
RE_SEP = re.compile(r'(\w+) (\d+),(\d+) (?:\w+) (\d+),(\d+)')


def parse_input(lines: list[str]):
    return lines


def solver(lines: list[str], alt_toggle: bool = False) -> np.ndarray:
    grid = np.zeros((1000, 1000), dtype=np.uint16)

    for line in lines:
        res = RE_SEP.search(line)

        if not res:
            raise ValueError(f"Could not parse {line}")

        mode = res.group(1)
        x1, y1, x2, y2 = map(int, res.group(2, 3, 4, 5))
        view = grid[x1:x2 + 1, y1:y2 + 1]

        if not alt_toggle:
            if mode == "on":
                view[:] = np.uint8(1)
            elif mode == "off":
                view[:] = np.uint8(0)
            else:  # toggle
                view ^= np.uint8(1)
        else:
            if mode == "on":
                view += np.uint8(1)
            elif mode == "off":
                view[view > 0] -= np.uint8(1)
            else:  # toggle
                view += np.uint8(2)

    return grid


@print_durations
def part1(data: list[str]) -> int:
    return int(np.sum(solver(data)))


@print_durations
def part2(data):
    return int(np.sum(solver(data, alt_toggle=True)))
