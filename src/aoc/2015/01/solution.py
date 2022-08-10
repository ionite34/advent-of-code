# advent of code 2015
# https://adventofcode.com/2015
# day 01

def parse_input(lines: list[str]):
    return lines[0]


def part1(data: str) -> int:
    return len(data) - 2 * data.count(')')


def part2(data: str) -> int:
    # Calculate index at which character enters basement
    # Or when the sum equals -1
    floor = 0
    for i, c in enumerate(data):
        floor += 1 if c == '(' else -1
        if floor == -1:
            return i + 1
