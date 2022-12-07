# advent of code 2022
# https://adventofcode.com/2022
# day 04
from parse import search


def parse_input(lines):
    ls = []
    for line in lines:
        ls.append(tuple(search("{:d}-{:d},{:d}-{:d}", line)))
    return ls


def part1(data):
    total = 0
    for a, b, x, y in data:
        r1 = {*range(a, b + 1)}
        r2 = {*range(x, y + 1)}
        if r1.issubset(r2) or r2.issubset(r1):
            total += 1
    return total


def part2(data):
    total = 0
    for a, b, x, y in data:
        r1 = {*range(a, b + 1)}
        r2 = {*range(x, y + 1)}
        if r1 & r2:
            total += 1
    return total
