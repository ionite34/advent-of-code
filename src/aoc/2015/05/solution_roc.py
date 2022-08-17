import re


def part1(data: list[str]) -> int:
    return sum(bool(
        not re.search(r'(ab|cd|pq|xy)', x) and
        re.search(r'([a-z])(\1)', x) and
        len(re.findall(r'[aeiou]', x)) >= 3
    ) for x in data)


def part2(data: list[str]) -> int:
    return sum(bool(
        re.search(r'([a-z])[a-z](\1)', x) and
        re.search(r'([a-z])([a-z]).*(\1)(\2)', x)
    ) for x in data)
