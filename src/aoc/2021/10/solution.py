# advent of code 2021
# https://adventofcode.com/2021
# day 10
from collections import Counter
from statistics import median
from funcy import print_durations


def parse_input(lines: list[str]) -> list[str]:
    return lines


pairs = {'(': ')', '[': ']', '{': '}', '<': '>'}
err_score = {')': 3, ']': 57, '}': 1197, '>': 25137}
cmp_score = {')': 1, ']': 2, '}': 3, '>': 4}


@print_durations
def part1(data: list[str]) -> int:
    error_score = 0
    for line in data:
        stack = []
        for char in line:
            # If opening bracket, add the expected closing bracket to stack
            if char in pairs:
                stack.append(pairs[char])
            # If closing bracket, check if it matches the last opening bracket
            elif char in pairs.values():
                if not stack or char != stack.pop():
                    error_score += err_score[char]
                    break
    return error_score


@print_durations
def part2(data: list[str]) -> int:
    print(f"P1 | {len(data)} lines loaded")
    all_scores = []
    for line in data:
        valid = True
        stack = []
        for char in line:
            # If opening bracket, add the expected closing bracket to stack
            if char in pairs:
                stack.append(pairs[char])
            # If closing bracket, check if it matches the last opening bracket
            elif char in pairs.values():
                if not stack or char != stack.pop():
                    valid = False
                    break
        if valid:
            # Count characters in stack
            score = 0
            for char in reversed(stack):
                score *= 5
                score += cmp_score[char]
            all_scores.append(score)
    # Find the median score
    med_score = median(all_scores)
    print(f"P2 | {len(all_scores)} scores, median {med_score}")
    return int(med_score)
