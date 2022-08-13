# advent of code 2021
# https://adventofcode.com/2021
# day 08
from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property


class Segment(Enum):
    """LED Segment"""
    TOP = 'a'
    TOP_LEFT = 'b'
    TOP_RIGHT = 'c'
    MIDDLE = 'd'
    BOTTOM_LEFT = 'e'
    BOTTOM_RIGHT = 'f'
    BOTTOM = 'g'

    @classmethod
    def from_str(cls, s: str) -> set[Segment]:
        return {
            cls(char) for char in s
        }


class Digit(Enum):
    """7-Segment LED Digits"""
    ZERO = {Segment.TOP, Segment.TOP_LEFT, Segment.TOP_RIGHT, Segment.BOTTOM_LEFT, Segment.BOTTOM_RIGHT, Segment.BOTTOM}
    ONE = {Segment.TOP_RIGHT, Segment.BOTTOM_RIGHT}
    TWO = {Segment.TOP, Segment.TOP_RIGHT, Segment.MIDDLE, Segment.BOTTOM_LEFT, Segment.BOTTOM}
    THREE = {Segment.TOP, Segment.TOP_RIGHT, Segment.MIDDLE, Segment.BOTTOM_RIGHT, Segment.BOTTOM}
    FOUR = {Segment.TOP_LEFT, Segment.TOP_RIGHT, Segment.MIDDLE, Segment.BOTTOM_RIGHT}
    FIVE = {Segment.TOP, Segment.TOP_LEFT, Segment.MIDDLE, Segment.BOTTOM_RIGHT, Segment.BOTTOM}
    SIX = {Segment.TOP, Segment.TOP_LEFT, Segment.MIDDLE, Segment.BOTTOM_LEFT, Segment.BOTTOM}
    SEVEN = {Segment.TOP, Segment.TOP_RIGHT, Segment.BOTTOM_RIGHT}
    EIGHT = {Segment.TOP, Segment.TOP_LEFT, Segment.TOP_RIGHT, Segment.MIDDLE, Segment.BOTTOM_LEFT,
             Segment.BOTTOM_RIGHT, Segment.BOTTOM}
    NINE = {Segment.TOP, Segment.TOP_LEFT, Segment.MIDDLE, Segment.BOTTOM_RIGHT, Segment.BOTTOM}

    @classmethod
    def as_list(cls) -> list[Digit]:
        return [item for item in cls]

    @classmethod
    def from_segments(cls, segments: set[Segment]) -> Digit | None:
        """Returns Digit from set of Segments, or None if not found."""
        try:
            return cls(segments)
        except ValueError:
            return None

    def __int__(self):
        return self.as_list().index(self)


@dataclass
class Entry:
    """Holds information for one entry line."""
    signals_str: str
    digits_str: str
    # Map of translation rules
    decode_map: dict[str, str] = field(default_factory=dict)

    @cached_property
    def digits(self) -> list[str]:
        return list(self.digits_str.split())

    @cached_property
    def signals(self) -> list[str]:
        return list(self.signals_str.split())

    def translate(self) -> list[Digit]:
        """Translate using decode map."""
        # Check if translatable
        chars = set(self.digits_str.replace(' ', ''))
        if not chars.issubset(self.decode_map.keys()):
            raise ValueError(
                f'Cannot translate {self.digits_str}!\n'
                f'Current keys: {self.decode_map.keys()}\n'
                f'Missing keys: {chars.difference(self.decode_map.keys())}'
            )
        # Use maketrans
        table = str.maketrans(self.decode_map)
        translated = self.digits_str.translate(table)
        # Get segments
        digits = [Digit.from_segments(Segment.from_str(*dg)) for dg in translated.split()]
        if None in digits:
            raise ValueError(f'Translation result not parsable {self.digits_str}')
        return digits

    def trans_signals(self):
        # Map of Segment | {possibilities}, start with all
        cases = {seg: set('abcdef') for seg in Segment}
        # Map of Digit | set(str)
        det_signals = {
            COUNT_TO_DIGIT[len(d)]: set(d) for d in self.signals if deterministic(len(d))
        }

        # (0 - 8) -> Middle
        middle = det_signals[Digit.ZERO] - det_signals[Digit.EIGHT]
        self.decode_map[middle] = Segment.MIDDLE.value
        # (1 - 7) -> Top
        top = det_signals[Digit.ONE] - det_signals[Digit.SEVEN]
        self.decode_map[top] = Segment.TOP.value

        for digit in det_signals:
            for seg in cases:
                if seg in digit.value:
                    cases[seg] = cases[seg].intersection(det_signals[digit])
                else:
                    cases[seg] = cases[seg] - det_signals[digit]
        print(f"Cases: {cases}")

    def try_trans(self):
        # Dict of int -> set of chars for deterministic digits
        # Map has (0, 1, 4, 7, 8)
        det_map = {
            int(COUNT_TO_DIGIT[len(d)]): set(d) for d in self.get_deterministic()
        }
        # Update dict with Digits in signals we are able to translate
        current_trans = str.maketrans(self.decode_map)
        trans_records = set(self.decode_map.keys())

        print(f"Pre: {det_map=}")

        for encoded_digit in self.signals:
            # Skip known values
            if set(encoded_digit) in det_map.values():
                continue
            # Translatable
            if set(encoded_digit).issubset(trans_records):
                res = encoded_digit.translate(current_trans)
                # Build digit
                res_d = Digit.from_segments(Segment.from_str(str(''.join(res))))
                # Add to det_map
                det_map[int(res_d)] = set(encoded_digit)

        # Set of non-deterministic (2, 3, 5, 6)
        # non_det = [set(d) for d in self.signals if not deterministic(len(d))]

        print(f"Post additional: {det_map=}")

        # (0 - 8) -> Middle
        middle = det_map[8] - det_map[0]
        self.decode_map[middle] = Segment.MIDDLE.value
        # (1 - 7) -> Top
        top = det_map[7] - det_map[1]
        self.decode_map[top] = Segment.TOP.value

    def get_count(self, length: int) -> Iterator[str]:
        """Returns signal strs matching count length."""
        for signal in self.signals:
            if len(signal) == length:
                yield signal

    def get_deterministic(self) -> list[str]:
        """Returns deterministic digits."""
        return [
            dg for dg in self.digits if deterministic(len(dg))
        ]


def deterministic(count: int) -> bool:
    """If true, count of segments can map to a digit."""
    return count in (2, 3, 4, 6, 7)


# Mapping of segment count to possible digits
DIGITS_5 = {Digit.TWO, Digit.THREE, Digit.FIVE, Digit.SIX}
COUNT_TO_DIGIT = {
    2: Digit.ONE,
    3: Digit.SEVEN,
    4: Digit.FOUR,
    6: Digit.ZERO,
    7: Digit.EIGHT,
}


def parse_input(lines: list[str]) -> list[Entry]:
    result = []
    for line in lines:
        signals, digits = line.split(' | ')
        result.append(Entry(signals.strip(), digits.strip()))
    return result


@print_durations
def part1(data: list[Entry]) -> int:
    total = 0  # Appearances of 1, 4, 7, 8
    for entry in data:
        # Get deterministic digits
        digits = entry.get_deterministic()
        for digit in digits:
            decoded = COUNT_TO_DIGIT[len(digit)]
            if decoded in (Digit.ONE, Digit.FOUR, Digit.SEVEN, Digit.EIGHT):
                total += 1
    return total


def part2(data: list[Entry]) -> int:
    for entry in data:
        # Get deterministic digits
        digits = entry.get_deterministic()
        for digit in digits:
            size = len(digit)
            decoded: Digit = COUNT_TO_DIGIT[size]
            # Get the same digit in the signal
            signal_digit = [*filter(lambda s: len(s) == size, entry.signals)][0]
            # Add translation rules of signal -> output
            for a, b in zip(digit, signal_digit):
                entry.decode_map[b] = a
        print(entry.decode_map)
        entry.trans_signals()
        result = entry.translate()
        print(result)
        return
