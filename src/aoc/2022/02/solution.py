# advent of code 2022
# https://adventofcode.com/2022
# day 02

WIN = 6
DRAW = 3
LOSE = 0

TURN_A = "ABC"
TURN_B = "XYZ"


def outcome(a: str, b: str) -> int:
    a, b = TURN_A.index(a), TURN_B.index(b)
    if a == b:
        return DRAW

    return WIN if (a + 1) % 3 == b else LOSE


def outcome_2(a: str, b: str) -> int:
    # Draw
    if b == "Y":
        return TURN_A.index(a) + 1 + DRAW
    # Lose
    if b == "X":
        turn = (TURN_A.index(a) + 2) % 3
        return turn + 1 + LOSE
    # Win
    if b == "Z":
        turn = (TURN_A.index(a) + 1) % 3
        return turn + 1 + WIN


def parse_input(lines):
    return [line.split() for line in lines]


def part1(data):
    total = 0
    for a, b in data:
        s1 = TURN_A.index(a) + 1
        s2 = outcome(a, b)
        total += s1 + s2
    return total


def part2(data):
    return sum(map(outcome_2, data))
