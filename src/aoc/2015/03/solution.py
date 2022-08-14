# advent of code 2015
# https://adventofcode.com/2015
# day 03

def parse_input(lines):
    return lines[0]


instr = {
    '^': (0, 1),
    'v': (0, -1),
    '<': (-1, 0),
    '>': (1, 0),
}


def visits(data: str) -> set:
    cords = set()
    p = (0, 0)
    for move in data:
        p = (*map(sum, zip(p, instr[move])),)
        cords |= {p}
    return cords


def part1(data: str) -> int:
    return len(visits(data))


def part2(data: str) -> int:
    return len(visits(data[::2]) | visits(data[1::2]))
