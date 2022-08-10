from collections.abc import Generator

import pytest

from aoc import tools


@pytest.mark.parametrize("data, expected", [
    (([1, 2, 3, 4, 5], 2), [(1, 2), (2, 3), (3, 4), (4, 5)]),
    ((range(1, 6), 3), [(1, 2, 3), (2, 3, 4), (3, 4, 5)]),
])
def test_windowed(data, expected) -> None:
    result = tools.windowed(*data)
    assert isinstance(result, Generator)
    assert list(result) == expected
