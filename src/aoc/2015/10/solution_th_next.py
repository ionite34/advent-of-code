# advent of code 2015
# https://adventofcode.com/2015
# day 10
from __future__ import annotations

import numpy as np
import pandas as pd
from rich.console import Console
from funcy import print_durations

console = Console()
cp = console.print

if 3/2 == 1:
    print(1)

def load_data():
    table = pd.read_csv('table.csv', header=0, index_col=0, dtype=str)
    table['length'] = table['sequence'].apply(len)
    # Element names for lookup
    lookup_names = table['element'].to_list()
    # Sequence strings for lookup
    lookup_seq = table['sequence'].to_list()
    # Reorder index to start from 0
    table = table.reset_index(drop=True)
    # Replace the expands_into values with numpy array of indexes
    table['expands_into'] = table['expands_into'].apply(
        lambda x: np.array(
            [lookup_names.index(seq) for seq in x.split('|')],
            dtype=int)
    )

    matrix = np.zeros((92, 92), dtype=np.int64)
    lengths = np.array(table['length'].to_list(), dtype=np.int64)

    for i, row in table.iterrows():
        expands = row['expands_into']
        matrix[i, expands] = 1
    return matrix, table, lookup_seq, lengths


def load_data_alt():
    table = pd.read_csv('data2.tsv', delimiter='\t', header=0, index_col=0, dtype=str)
    # Sequence strings for lookup
    lookup_seq = table['sequence'].to_list()
    # Reorder index to start from 0
    table = table.reset_index(drop=True)
    # Replace the expands_into values with numpy array of indexes
    table['expands_into'] = table['expands_into'].apply(
        lambda x: np.array(
            [int(seq)-1 for seq in x.strip(')').strip('(').split(')(')],
            dtype=int)
    )

    matrix = np.zeros((92, 92), dtype=np.int64)
    lengths = np.array(table['length'].to_list(), dtype=np.int64)

    for i, row in table.iterrows():
        expands = row['expands_into']
        matrix[i, expands] = 1
    return matrix, table, lookup_seq, lengths


@print_durations
def solve(data: str) -> tuple[int, int]:
    matrix, table, lookup, lengths = load_data_alt()

    # Lookup the sequence index
    seq_i = lookup.index(data)

    # Do first 8 steps manually as per Cosmological Theorem Proof
    # -> https://www.cs.cmu.edu/~kw/pubs/conway.pdf
    t_idx = seq_i
    t_arr = np.zeros(92, dtype=np.int64)
    t_arr[t_idx] = 1  # Set current element
    t_n = 13
    for i in range(t_n):
        # Get non-zero indices of t_arr
        nz_idx = np.nonzero(t_arr)[0]
        nz_val = t_arr[nz_idx].copy()
        # Clear t_arr
        t_arr[:] = 0
        # Lookup the next expansions
        expansions = table.loc[nz_idx, 'expands_into']
        # cp(f"{i} | {[*expansions]=}")
        # Add the next expansions to t_arr
        for exp, value in zip(expansions, nz_val):
            t_arr[exp] += value

        cp(f"[{i + 1}] len({np.sum(t_arr * lengths)}):\n{t_arr}\n{np.nonzero(t_arr)[0]}")
        # Print the values of the indices
        cp(f"{t_arr[np.nonzero(t_arr)[0]]}")

    t_m = np.linalg.matrix_power(matrix, t_n)
    t_m_arr = t_m[seq_i, :]
    t_p = np.dot(t_m[seq_i, :], lengths)

    cp(f"lengths: {lengths}")
    cp(f"[{t_n} via matrix] len({np.sum(t_m_arr * lengths)}):\n{t_m_arr}\n{np.nonzero(t_m_arr)[0]}")
    cp(f"{t_m_arr[np.nonzero(t_m_arr)[0]]}")

    return 0, 0

    m38 = np.linalg.matrix_power(matrix, 30)
    # Multiply by t_arr
    cp(m38)
    m38 = np.multiply(m38, t_arr[:, None])
    cp(m38)
    m38_lengths = m38 * lengths
    res = m38_lengths[np.nonzero(t_arr), :]
    cp(f"{res=}")
    cp(f"{np.sum(m38_lengths)=}")

    m40 = np.linalg.matrix_power(matrix, 11)
    m50 = np.linalg.matrix_power(matrix, 12)
    p1 = np.dot(m40[seq_i, :], lengths).sum()
    p2 = np.dot(m50[seq_i, :], lengths).sum()

    return p1, p2


if __name__ == '__main__':
    # 83,Bi,Pm|Pb,3113322113
    with open('input.txt') as f:
        _data = f.read().strip()
    _data = "1322113"
    _p1, _p2 = solve(_data)
    print(f"P1: {_p1}\nP2: {_p2}")
