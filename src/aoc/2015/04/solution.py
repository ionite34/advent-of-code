# advent of code 2015
# https://adventofcode.com/2015
# day 04
from __future__ import annotations

import os
from hashlib import md5
from concurrent.futures import ProcessPoolExecutor, ALL_COMPLETED, wait, as_completed
from functools import partial, cache
from itertools import count

from funcy import print_durations
from functools import cache

def parse_input(lines):
    return lines[0]


KEY = "ckczppom"


# noinspection InsecureHash
def s_suffix(prefix):
    for i in count():
        if (
                md5(f"{KEY}{i}".encode())
                        .hexdigest()
                        .startswith(prefix)
        ):
            return i


# noinspection InsecureHash
def is_valid(data: str, prefix: str, chunk) -> int | None:
    for i in chunk:
        digest = md5(f"{data}{i}".encode()).hexdigest()
        if digest.startswith(prefix):
            return i


def check_valid(data: str, prefix: str, limit: int, start: int = 0) -> int | None:
    n_workers = os.cpu_count()
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = []
        for thread in range(n_workers):
            futures.append(
                executor.submit(
                    is_valid, data, prefix,
                    range(1 + thread + start, 10 ** limit + thread + start, n_workers)
                )
            )
        return min(t for f in futures if (t := f.result()))


def check_valid_alt(text: str, leading_zeros: int) -> int | None:
    suffix = str(z := leading_zeros) * z
    validator = partial(is_valid, text, suffix)
    start = 0
    chunk = 120_000
    with ProcessPoolExecutor(max_workers=6) as executor:
        while True:
            results = executor.map(validator, [*range(start, start + chunk)])
            for result in results:
                if result is not None:
                    executor.shutdown(wait=False, cancel_futures=True)
                    return result
            start += chunk


@print_durations
@cache
def part1(data: str):
    return check_valid(data, "0"*5, 7)


@print_durations
def part2(data: str):
    return check_valid(data, "0"*6, 7, start=117946)
