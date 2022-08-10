# advent of code 2021
# https://adventofcode.com/2021
# day 01
from aoc.tools import windowed


def parse_input(lines: list[str]) -> list[int]:
    return [*map(int, lines)]


def part1(data) -> int:
    last = None
    increased = 0
    for depth in data:
        if last is None:
            last = depth
            continue
        if depth > last:
            increased += 1
            last = depth
    return increased


def part2(data) -> int:
    last = None
    increased = 0
    for section in windowed(data, 3):
        depth = sum(section)
        if last is None:
            last = depth
            continue
        if depth > last:
            increased += 1
            last = depth
    return increased

