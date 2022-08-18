# advent of code 2015
# https://adventofcode.com/2015
# day 06
import re
import numpy as np

from aoc import log

log.setLevel("WARNING")
RE_SEP = re.compile(r'(\w+) (\d+),(\d+) (?:\w+) (\d+),(\d+)')


def parse_input(lines: list[str]):
    return lines


def solver(lines: list[str], alt_toggle: bool = False) -> np.ndarray:
    # Make a 1000x1000 grid
    grid = np.zeros((1000, 1000), dtype=int)
    log.info(f"Grid size: {grid.shape}")
    # Parse input with regex)
    for idx, line in enumerate(lines):
        res = RE_SEP.search(line)

        if not res:
            log.warning(f"[{idx}] Could not parse line: {line}")
            continue

        mode = res.group(1)
        x1, y1, x2, y2 = map(int, res.group(2, 3, 4, 5))
        log.info(f"[{idx}] ({mode}) {x1},{y1} to {x2},{y2}")
        if not alt_toggle:
            if mode == "on":
                grid[x1:x2 + 1, y1:y2 + 1] = 1
            elif mode == "off":
                grid[x1:x2 + 1, y1:y2 + 1] = 0
            else:  # toggle
                grid[x1:x2 + 1, y1:y2 + 1] = 1 - grid[x1:x2 + 1, y1:y2 + 1]
        else:
            if mode == "on":
                grid[x1:x2 + 1, y1:y2 + 1] += 1
            elif mode == "off":
                grid[x1:x2 + 1, y1:y2 + 1] -= 1
                grid = np.maximum(grid, 0)
            else:  # toggle
                grid[x1:x2 + 1, y1:y2 + 1] += 2

        log.info(f"[{idx}] Grid: {np.sum(grid)}")
    return grid


def part1(data: list[str]) -> int:
    return int(np.sum(solver(data)))


def part2(data):
    return int(np.sum(solver(data, alt_toggle=True)))
