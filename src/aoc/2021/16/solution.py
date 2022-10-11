# advent of code 2021
# https://adventofcode.com/2021
# day 16
from __future__ import annotations

from collections.abc import Generator
from dataclasses import dataclass
from math import prod
from operator import gt, lt, eq
from functools import cached_property
from typing import NamedTuple

from rich import print as cp


class ReadResult(NamedTuple):
    value: str | int
    remainder: int
    stop_index: int
    message: Message


def from_hex(s: str) -> int:
    """Converts a hex string to int."""
    return int(s, base=16)


def from_bin(s: str) -> int:
    """Converts a binary string to int."""
    return int(s, base=2)


def to_bin(n: int) -> str:
    """Converts an integer to a string of binary bits."""
    # Pads to 4 length with leading zeros
    return f"{n:04b}"


@dataclass
class PacketB5:
    """5-bit packet."""

    _data: str

    @property
    def data(self) -> str:
        """Return data as a string of bits (last 4 bits)."""
        return self._data[1:]

    @property
    def is_last(self) -> bool:
        """Is last packet if starts with 0."""
        return self._data.startswith("0")

    @classmethod
    def from_bits(
            cls, bits: str, start_index: int = 6
    ) -> Generator[PacketB5, None, None]:
        """Yields packets from a string of bits."""
        bits = bits[start_index:]
        while bits:
            packet = cls(bits[:5])
            yield packet
            if packet.is_last:
                break
            bits = bits[5:]


class MessageGroup(list):
    """A group of messages."""

    OPS = {
        0: sum,
        1: prod,
        2: min,
        3: max,
        5: lambda x: gt(*x),
        6: lambda x: lt(*x),
        7: lambda x: eq(*x),
    }

    def __init__(self, *args, msg: Message, group_bits: int):
        super().__init__(*args)
        self.version = msg.version
        self.type_id = msg.type_id
        self.group_bits = group_bits

    def __repr__(self):
        return f"MessageGroup(v={self.version}, {super().__repr__()})"

    def evaluate(self) -> int:
        """Evaluates the group."""
        op = self.OPS[self.type_id]
        return int(op(m.evaluate() if isinstance(m, MessageGroup) else m.literal for m in self))

    @cached_property
    def total_bits(self):
        """Returns the total number of bits in the group, plus the group header."""
        return sum(m.total_bits for m in self) + self.group_bits

    @cached_property
    def version_sum(self) -> int:
        """Returns the sum of the version numbers."""
        return sum(
            m.version if isinstance(m, Message) else m.version_sum for m in self
        ) + self.version


class Message:
    """BITS Transmission Message."""

    IDX_V = slice(0, 3)  # Packet Version
    IDX_T = slice(3, 6)  # Packet Type ID
    IDX_I = 6  # Length Type ID
    IDX_OP = 7  # Operator Sub-Packets

    def __init__(self, bits: str):
        self.bits = bits

    def __len__(self) -> int:
        return len(self.bits)

    @property
    def total_bits(self) -> int:
        return len(self.bits)

    def __str__(self) -> str:
        s = (
            f"Message({self.bits})\n"
            f"|- size: {len(self.bits)} bits\n"
            f"|- version: {self.version}\n"
            f"|- type_id: {self.type_id}\n"
        )
        if self.literal is not None:
            s += f"|- literal: {self.literal}\n"
        return s

    def __repr__(self) -> str:
        return (
            f"Message(bits[{self.total_bits}]={self.bits}, version={self.version}, "
            f"type_id={self.type_id}, literal={self.literal})"
        )

    @cached_property
    def version(self) -> int:
        """Returns the message version."""
        return int(self.bits[self.IDX_V], 2)

    @cached_property
    def type_id(self) -> int:
        """Returns the message type id."""
        return from_bin(self.bits[self.IDX_T])

    @cached_property
    def type_length_id(self) -> int:
        """Returns the type length id bit."""
        # 0: next 15 bits are a number that represents the total
        # length in bits of the sub-packets contained by this packet.
        # 1: next 11 bits are a number that represents the number
        # of sub-packets immediately contained by this packet.
        return from_bin(self.bits[6])

    def take_bits(self, start: int, length: int):
        to_read = slice(start, start + length)
        return self.bits[to_read]

    def read_v4(self) -> ReadResult:
        """Reads a v4 message (literal)."""
        packets = [p.data for p in PacketB5.from_bits(self.bits)]
        result = "".join(packets)
        remainder = len(self.bits) - (5 * len(packets)) - 6
        stop_index = len(self.bits) - remainder
        cp(f">> read_v4: {result}[{from_bin(result)}] (rem={remainder}, stop={stop_index})")
        return ReadResult(from_bin(result), remainder, stop_index, Message(self.bits[:stop_index]))

    @cached_property
    def literal(self) -> int | None:
        """Returns the literal value if type_id is 4."""
        if self.type_id == 4:
            return self.read_v4().value

    def read(self) -> Message | MessageGroup:
        """Reads the message."""
        # Literal
        if self.type_id == 4:
            return self.read_v4().message

        # Operators
        if self.type_length_id == 0:
            # Next 15 bits => bit length of sub-packets
            max_bits = from_bin(tb := self.take_bits(self.IDX_OP, 15))
            cp("max_bits:", max_bits, "bits ->", tb)
            if not max_bits:
                raise ValueError("max_bits is 0")
            results = self.take_while(
                self.bits[self.IDX_OP + 15:],
                max_bits=max_bits
            )
            return MessageGroup(results, msg=self, group_bits=self.IDX_OP + 15)

        elif self.type_length_id == 1:
            # Next 11 bits => n sub-packets
            max_packets = from_bin(self.take_bits(self.IDX_OP, 11))
            cp("max_packets:", max_packets)
            if not max_packets:
                raise ValueError("max_packets is 0")
            results = self.take_while(
                self.bits[self.IDX_OP + 11:],
                max_packets=max_packets
            )
            return MessageGroup(results, msg=self, group_bits=self.IDX_OP + 11)

        raise ValueError(f"Unknown message: {self.type_id=}, {self.type_length_id=}")

    @classmethod
    def from_data(cls, data: str) -> Message:
        """Creates a message from a string of bits."""
        decoded = "".join(map(to_bin, map(from_hex, data)))
        return cls(decoded)

    @classmethod
    def take_while(
            cls, bits: str, max_bits: int | None = None, max_packets: int | None = None
    ) -> Generator[Message | MessageGroup, None, None]:
        """Generate packets from a string of bits."""
        read_bits = 0
        read_packets = 0
        while True:
            msg = cls(bits)
            res = msg.read()
            yield res

            # Increment counters
            read_packets += 1
            instance_bits = res.total_bits
            read_bits += res.total_bits

            if max_packets is not None and read_packets >= max_packets:
                break
            if max_bits is not None and read_bits >= max_bits:
                break

            # Increment read bits
            bits = bits[res.total_bits:]


def parse_input(lines) -> str:
    return lines[0]


def part1(data: str):
    m = Message.from_data(data)
    res = m.read()
    return res.version_sum


def part2(data: str):
    m = Message.from_data(data)
    res = m.read()
    return res.evaluate()
