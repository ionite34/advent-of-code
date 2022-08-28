# advent of code 2015
# https://adventofcode.com/2015
# day 10
from __future__ import annotations

import numpy as np
import pandas as pd
from funcy import print_durations


def load_data():
    table = pd.read_csv('table.csv', header=0, index_col=0, dtype=str)
    print(table.head())
    # Add column with length of string of column "sequence"
    table['length'] = table['sequence'].apply(len)
    print(table.head())
    # Build the matrix
    matrix = np.zeros((92, 92), dtype=np.int64)
    # Fill the matrix
    lookup = table['element'].to_list()
    lengths = np.array(table['length'].to_list())
    for i, row in table.iterrows():
        expands = row['expands_into'].split('|')
        for element in expands:
            pos = lookup.index(element)
            matrix[pos, i-1] = 1
    return matrix, table, lookup, lengths


def compress(buffer: str):
    ...


@print_durations
def part1(data):
    # M^40 = (M^20)^2, M^50 = M^40*M^10
    matrix, table, lookup, lengths = load_data()
    idx = table[table['sequence'] == data].index[0]
    print(matrix)
    m20 = np.linalg.matrix_power(matrix, 20)
    m40 = np.linalg.matrix_power(m20, 2)
    m50 = m40 @ m20
    p1 = m40[:, idx-1] * lengths
    print(p1)
    print(p1.sum())
    p2 = m50[:, idx-1] * lengths
    print(p2)
    print(p2.sum())
    return None


@print_durations
def part2(data):
    return 0


if __name__ == '__main__':
    # 83,Bi,Pm|Pb,3113322113
    with open('input.txt') as f:
        _data = f.read().strip()
    print(part1(_data))
    print(part2(_data))
