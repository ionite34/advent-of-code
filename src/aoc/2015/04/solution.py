# advent of code 2015
# https://adventofcode.com/2015
# day 04
from __future__ import annotations

from hashlib import md5
from concurrent.futures import ProcessPoolExecutor


def parse_input(lines):
    return lines[0]


# noinspection InsecureHash
def is_valid(data: str, prefix: str, chunk: range) -> int | None:
    for i in chunk:
        digest = md5(f"{data}{i}".encode()).hexdigest()
        if digest.startswith(prefix):
            return i
    return None


def check_valid(data: str, prefix: str, limit: int) -> int | None:
    n_workers = 10
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        for thread in range(n_workers):
            futures.append(
                executor.submit(
                    is_valid, data, prefix,
                    range(1 + thread, limit + thread, n_workers)
                )
            )
        return min(t for f in futures if (t := f.result()))


def part1(data: str):
    return check_valid(data, "0" * 5, 7)


def part2(data: str):
    return check_valid(data, "0" * 6, 7)
