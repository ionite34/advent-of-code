# advent of code 2021
# https://adventofcode.com/2021
# day 10
import numpy as np
from funcy import print_durations
from numba import prange, njit
from numpy.typing import NDArray


def parse_input(lines: list[str]) -> NDArray[np.uint8]:
    # Map each line to a ndarray of char codes as ints
    max_chars = max(len(line) for line in lines)

    temp = [np.pad(
                arr := np.array([ord(c) for c in line], dtype=np.uint8),
                (0, max_chars - len(arr)),
                'constant'
            ) for line in lines]

    arr = np.vstack(temp)
    return arr


@njit
def count_errors(arr: NDArray[np.uint8]) -> NDArray[np.int64]:
    # Lookup table for open to close pairs
    pairs = {
        40: 41,
        91: 93,
        123: 125,
        60: 62,
    }
    index_map = {
        41: 0,
        93: 1,
        125: 2,
        62: 3,
    }
    # Count the number of errors in the array
    total_errors = np.zeros(4, dtype=np.int64)
    for i in range(len(arr)):
        errors = np.zeros(4, dtype=np.int64)

        # Bracket depth
        # 0 | () 40, 41
        # 1 | [] 91, 93
        # 2 | {} 123, 125
        # 3 | <> 60, 62
        depth = np.zeros(4, dtype=np.int64)

        # Record first character
        first = arr[i][0]
        first_pair = pairs[first]
        depth[index_map[first_pair]] += 1
        # Remember the last opened brackets
        bracket_tree = [first]
        for idx, char in enumerate(arr[i][1:]):
            # If bracket is open, add to bracket_tree
            if char in pairs:
                bracket_tree.append(pairs[char])
            else:
                # If bracket is closed, pop from bracket_tree and check
                last_open = bracket_tree.pop()
                if char != last_open:
                    errors[index_map[last_open]] += 1
                    break
            # If closing first char, require all depth to be 0
            if char == first_pair and depth[index_map[char]] == 1:
                # print("closing", idx, char, '<-', arr[i])
                depth[index_map[char]] -= 1
                if np.any(depth > 0):
                    errors[index_map[char]] += 1
                break
            if char == 40:
                depth[0] += 1
            elif char == 41:
                if depth[0] == 0:
                    errors[0] += 1
                    break
                else:
                    depth[0] -= 1
            elif char == 91:
                depth[1] += 1
            elif char == 93:
                if depth[1] == 0:
                    errors[1] += 1
                    break
                else:
                    depth[1] -= 1
            elif char == 123:
                depth[2] += 1
            elif char == 125:
                if depth[2] == 0:
                    errors[2] += 1
                    break
                else:
                    depth[2] -= 1
            elif char == 60:
                depth[3] += 1
            elif char == 62:
                if depth[3] == 0:
                    errors[3] += 1
                    break
                else:
                    depth[3] -= 1
        print(i, errors)
        total_errors += errors
    return total_errors


@print_durations
def part1(data: NDArray):
    print(f"P1 | {len(data)} lines loaded")
    results = count_errors(data)
    print("P1 |  ) ] } >")
    print(f"P1 | {results}")
    # print(line.view(f'S{line.shape[0]}').flatten()[0])
    return


def part2(data):
    pass
