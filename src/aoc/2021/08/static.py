# Static analysis
from itertools import permutations

from solution import Segment, Digit


def find_masks():
    # Get all combinations of digit pairs from (0, 1, 4, 7, 8)
    combos = (Digit.ZERO, Digit.ONE, Digit.FOUR, Digit.SEVEN, Digit.EIGHT)
    pairs = permutations(combos, 2)
    # Loop through all pairs and find subtractions that end up with 1 segment
    v1: Digit
    v2: Digit
    for v1, v2 in pairs:
        # Get subtractions
        sub = v1.value - v2.value
        # Check if one element
        if len(sub) == 1:
            print(f"{v1} - {v2} = {sub}")


find_masks()
