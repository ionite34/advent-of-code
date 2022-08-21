# advent of code 2015
# https://adventofcode.com/2015
# day 07
from __future__ import annotations

import operator
import re

from aoc import log

log.setLevel("WARNING")

Match = tuple[str, str, str, str]

RE_ELEMENTS = re.compile(r"(?:(\w+)\s)?(?:(\w+)\s)?(\w+) -> (\w+)")

op_map = {
    "AND": operator.and_,
    "OR": operator.or_,
    "LSHIFT": operator.lshift,
    "RSHIFT": operator.rshift,
}

p1: int | None = None


def parse_input(lines) -> list[Match]:
    return RE_ELEMENTS.findall("\n".join(lines))


def resolve(
        signals: dict,
        all_matches: list[Match],
        match: Match,
) -> dict:
    # If assignment target exists, just return
    if match[3] in signals:
        return signals

    if match[0] == "NOT":
        match = ("", "NOT", match[2], match[3])

    a, op, b, target = match
    if not a and not op:
        # Simple numerical assignment
        if b.isdecimal():
            signals[target] = int(b)
            return signals
        # Name assignment
        signals[target] = signals[b]
        return signals

    table = [
        int(a) if a.isdecimal() else signals.get(a),
        int(b) if b.isdecimal() else signals.get(b),
    ]
    for i, (symbol, value) in enumerate(zip((a, b), table)):
        if symbol and not value:
            log.info(f"Checking value for {symbol}")
            found = [*filter(lambda x: x[3] == symbol, all_matches)]
            if not found:
                raise ValueError(f"Unknown signal {symbol} in {match}")
            log.info(f"Found {found}")
            # Recursively decode the signal
            signals = resolve(signals, all_matches, found[0])
            table[i] = signals[symbol]

    if op == "NOT":
        signals[target] = table[1] ^ 65535
    else:
        signals[target] = op_map[op](table[0], table[1])
    return signals


def part1(data: list[Match]) -> int:
    global p1
    signals: dict[str, int] = {}
    for match in data:
        signals = resolve(signals, data, match)
    p1 = signals["a"]
    return p1


def part2(data: list[Match]) -> int:
    if not p1:
        raise ValueError("Part 1 not solved yet")
    signals: dict[str, int] = {'b': p1}
    for match in data:
        signals = resolve(signals, data, match)
    return signals["a"]
