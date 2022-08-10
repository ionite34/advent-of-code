# advent of code 2021
# https://adventofcode.com/2021
# day 02
from dataclasses import dataclass


@dataclass
class Pos:
    x: int = 0
    y: int = 0
    z: int = 0
    aim: int = 0


def parse_input(lines: list[str]) -> list[tuple[str, int]]:
    def gen():
        for line in lines:
            res = line.split(' ')
            yield res[0], int(res[1])

    return [*gen()]


def part1(data: list[tuple[str, int]]) -> int:
    sub = Pos()
    for instr, factor in data:
        if instr == "forward":
            sub.x += factor
        elif instr == "down":
            sub.z += factor
        elif instr == "up":
            sub.z -= factor

    return sub.x * sub.z


def part2(data: list[tuple[str, int]]) -> int:
    sub = Pos()
    for instr, factor in data:
        if instr == "down":
            sub.aim += factor
        elif instr == "up":
            sub.aim -= factor
        elif instr == "forward":
            sub.x += factor
            sub.z += (sub.aim * factor)

    return sub.x * sub.z
