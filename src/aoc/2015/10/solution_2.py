# advent of code 2015
# https://adventofcode.com/2015
# day 10
from __future__ import annotations

from itertools import groupby

from llist import dllist, dllistnode
from funcy import print_durations


def parse_input(lines: list[str]):
    return lines[0]


def compress(buffer: str | dllist) -> dllist:
    if isinstance(buffer, str):
        buffer = dllist(buffer)
    # Current node
    node: dllistnode = buffer.first
    # Stored character to compare with
    look_behind: dllistnode = node
    lb_count = 1
    while node:
        n_ref = node.next
        buffer.remove(node)
        node = n_ref
        if node is None:
            buffer.append(str(lb_count))
            buffer.append(look_behind.value)
            break
        # Increment count if current character is the same as the stored one
        if node.value == look_behind.value:
            lb_count += 1
            continue
        # Insert into buffer
        n1 = buffer.insertbefore(look_behind.value, node)
        buffer.insertbefore(str(lb_count), n1)
        # Run reset
        look_behind = node
        lb_count = 1
    # print(f"{buffer.size=} | {buffer=}")
    return buffer


@print_durations
def part1(data):
    data = "1"
    for _ in range(40):
        data = compress(data)
    return len(data)


@print_durations
def part2(data):
    for _ in range(50):
        data = compress(data)
    return len(data)


if __name__ == '__main__':
    with open('input.txt') as f:
        _data = parse_input(f.readlines())
    print(part1(_data))
    print(part2(_data))
