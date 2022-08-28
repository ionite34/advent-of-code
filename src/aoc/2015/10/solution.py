# advent of code 2015
# https://adventofcode.com/2015
# day 10
from itertools import groupby

from funcy import print_durations


def parse_input(lines: list[str]):
    return lines[0]


def compress(text: str):
    for a, b in groupby(text):
        yield f"{len([*b])}{a}"


@print_durations
def part1(data):
    data = '12'
    for i in range(12):
        print(f"{i=} | {len(data)} -> '{data=}'")
        if data == '3113322113':
            print(f"Found: {data=}")
            break
        data = ''.join(compress(data))
    return len(data)


@print_durations
def part2(data):
    return 0
    for i in range(50):
        print(f"{i=} | {data=}")
        data = ''.join(compress(data))
    return len(data)
