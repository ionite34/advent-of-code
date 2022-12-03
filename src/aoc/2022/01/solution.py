# advent of code 2022
# https://adventofcode.com/2022
# day 01

def parse_input(lines):
    return lines


def part1(data: list[str]):
    bags = []
    total = 0
    for line in data:
        if not line:
            if total:
                bags.append(total)
                total = 0
            continue
        total += int(line)
    return sum(bags)


def part2(data):
    bags = []
    total = 0
    for line in data:
        if not line:
            if total:
                bags.append(total)
                total = 0
            continue
        total += int(line)
    # Top 3 bags
    top3 = sorted(bags, reverse=True)[:3]
    return sum(top3)
