def parse_input(lines: list[str]) -> tuple[list[str], list[str]]:
    return lines[0], lines[1:]


def part1(data: tuple[list[str], list[str]]) -> int:
    opponent, decisions = data
    score = 0
    for round, choice in enumerate(opponent):
        c = choices[choice]
        d = decisions[round]
        score += get_round_score(c, d)
    # print("Total Score: {}".format(score))
    return score


def part2(data: tuple[list[str], list[str]]) -> int:
    opponent, decisions = data
    score = 0
    for round, choice in enumerate(opponent):
        c = choices[choice]
        d = min(decisions[round])
        score += get_round_score(c, d)
    # print("Total Score: {}".format(score))
    return score


choices = {
    'A': 1,
    'B': 2,
    'C': 3,
}


def get_round_score(c: int, d: str) -> int:
    choice = choices[d]
    if choice == c:
        score = 3
    elif choice == c + 1 % 3:
        score = 0
    else:
        score = 6
    # print("Opponent choice: {}; Your choice: {} ({}) -> Score: {}".format(c, choice, d, score))
    return score + choice
