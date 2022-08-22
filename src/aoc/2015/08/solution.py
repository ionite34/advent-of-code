# advent of code 2015
# https://adventofcode.com/2015
# day 08


def parse_input(lines: list[str]):
    return lines


def part1(data: list[str]) -> int:
    chars = 0
    literals = 0
    for line in data:
        literals += len(line)
        chars += len(eval(line))
    return literals - chars


def part2(data: list[str]) -> int:
    literals = 0
    encoded = 0
    for line in data:
        literals += len(line)
        encoded += (
                2 +
                len(line) +
                line.count('"') +
                line.count('\\')
        )
    return encoded - literals
