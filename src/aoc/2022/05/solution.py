# advent of code 2022
# https://adventofcode.com/2022
# day 05
from rich.traceback import install
from parse import search

install(show_locals=True)


def get_stacks(data: list[str]):
    result = [[] for _ in range(len(data[0]) // 4 + 1)]
    for line in data[:data.index("") - 1]:
        cts = [line[i].strip() for i in range(1, len(line), 4)]
        for i, crate in enumerate(cts):
            if crate:
                result[i].insert(0, crate)
    print(result, len(result))
    return result


def parse_input(lines):
    return get_stacks(lines), [
        tuple(search(r"move {:d} from {:d} to {:d}", line))
        for line in lines[lines.index("") + 1:]
    ]


def part1(stacks, moves, reverse=False):
    for n, src, dst in moves:
        # shift for index
        src -= 1
        dst -= 1
        # Move quantity from src list end to dst end
        to_move = [stacks[src].pop() for _ in range(n)]
        stacks[dst].extend(reversed(to_move) if reverse else to_move)
    # Get all strings at end of each list
    return "".join(stack[-1] for stack in stacks)


def part2(stacks, moves):
    return part1(stacks, moves, reverse=True)
