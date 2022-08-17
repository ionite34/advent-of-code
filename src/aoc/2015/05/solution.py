# advent of code 2015
# https://adventofcode.com/2015
# day 05
import re

from funcy import print_durations

re_bad = re.compile(r'(ab|cd|pq|xy)')
re_dup = re.compile(r'([a-z])(\1)')
re_vowel = re.compile(r'[aeiou]')

re_dup_middle = re.compile(r'([a-z])[a-z](\1)')
re_dup_pair = re.compile(r'([a-z])([a-z]).*(\1)(\2)')


def parse_input(lines):
    return lines


def is_nice(text: str) -> bool:
    return bool(
        not re_bad.search(text) and
        re_dup.search(text) and
        len(re_vowel.findall(text)) >= 3
    )


def is_nice_2(text: str) -> bool:
    return bool(
        re_dup_middle.search(text) and
        re_dup_pair.search(text)
    )


@print_durations
def part1(data: list[str]):
    return sum(map(is_nice, data))


@print_durations
def part2(data):
    return sum(map(is_nice_2, data))
