# advent of code 2022
# https://adventofcode.com/2022
# day 03

ind = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def parse_input(lines):
    return lines


def part1(data: list[str]) -> int:
    total = 0
    for line in data:
        # Split line in half
        comp1 = set(line[:len(line) // 2])
        comp2 = set(line[len(line) // 2:])
        # Find intersection
        common = comp1.intersection(comp2)
        # Find score
        total += ind.index(common.pop()) + 1
    return total


def part2(data: list[str]) -> int:
    total = 0
    # Get every 3 lines in data
    for line1, line2, line3 in zip(data[::3], data[1::3], data[2::3]):
        # Find intersection of all 3 lines
        common = set(line1).intersection(set(line2), set(line3))
        # Find score
        total += ind.index(common.pop()) + 1
    return total
