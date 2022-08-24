# advent of code 2015
# https://adventofcode.com/2015
# day 09
from itertools import permutations

import parse
from funcy import print_durations

Nodes = dict[str, dict[str, int]]


def parse_input(lines) -> Nodes:
    nodes: dict[str, dict[str, int]] = {}
    for line in lines:
        r = tuple(parse.parse('{} to {} = {:d}', line))
        nodes.setdefault(r[0], {})[r[1]] = r[2]
        nodes.setdefault(r[1], {})[r[0]] = r[2]
    return nodes


@print_durations
def part1(nodes: Nodes):
    return min(
        sum(nodes[p[i]][p[i + 1]] for i in range(len(p) - 1))
        for p in permutations(nodes)
    )


@print_durations
def part2(nodes: Nodes):
    return max(
        sum(nodes[p[i]][p[i + 1]] for i in range(len(p) - 1))
        for p in permutations(nodes)
    )
