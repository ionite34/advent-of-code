# advent of code 2021
# https://adventofcode.com/2021
# day 08
from __future__ import annotations

import re
from funcy import print_durations

DIGIT_RE = re.compile(r"[a-g]+")

DECODE_MAP = {
    (6, 2, 3): "0",
    (2, 2, 2): "1",
    (5, 1, 2): "2",
    (5, 2, 3): "3",
    (4, 2, 4): "4",
    (5, 1, 3): "5",
    (6, 1, 3): "6",
    (3, 2, 2): "7",
    (7, 2, 4): "8",
    (6, 2, 4): "9",
}


def decode(parsed_lines: list[list]):
    for match in parsed_lines:
        one, _, four, *_ = sorted(match[:-4], key=len)
        one = set(one)
        four = set(four)

        yield "".join(
            DECODE_MAP[
                len(digit),
                len(one.intersection(digit)),
                len(four.intersection(digit)),
            ]
            for digit in match[-4:]
        )


def parse_input(lines: list[str]) -> list[list]:
    return [
        DIGIT_RE.findall(line) for line in lines
    ]


@print_durations
def part1(parsed_lines: list[list]) -> int:
    return sum(
        digit in {"1", "4", "7", "8"}
        for result in decode(parsed_lines)
        for digit in result
    )


@print_durations
def part2(parsed_lines: list[list]) -> int:
    return sum(map(int, decode(parsed_lines)))
