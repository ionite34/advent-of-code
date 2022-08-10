from __future__ import annotations

from itertools import islice
from typing import Any, TypeVar, Annotated, Tuple
from collections.abc import Generator, Iterable

import numpy as np

from numba import njit

T = TypeVar("T")


def windowed(seq: Iterable[T], n: int) -> Generator[tuple[T], Any, None]:
    """
    Returns a sliding window of size `n` over `seq`, as tuples of
    the form (seq[i:i+n], seq[i+1:i+n+1], ..., seq[i+n-1:i+n])

    Args:
        seq: The sequence to slide over.
        n: The size of the sliding window.

    Yields:
        The next n elements of seq.
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def inter_bin(bits: np.ndarray | Iterable) -> tuple[int, int]:
    if isinstance(bits, np.ndarray):
        norm = bits.dot(1 << np.arange(bits.size)[::-1]).flatten()[0]
        inv_bits = 1 - bits
        inv_norm = inv_bits.dot(1 << np.arange(inv_bits.size)[::-1]).flatten()[0]
        return norm, inv_norm
    else:
        return inter_bin_iter(bits)


@njit
def inter_bin_iter(bits: Iterable):
    """Interpret bits as a binary number."""
    out = 0
    inv = 0
    for bit in bits:
        out = (out << 1) | bit
        inv = (inv << 1) | (1 - bit)
    return out, inv
