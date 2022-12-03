# advent of code 2021
# https://adventofcode.com/2021
# day 15
import numpy as np
import networkx as nx


def parse_input(lines: list[str]) -> np.ndarray:
    data = np.array([[*map(int, line)] for line in lines], dtype=np.uint8)
    return data


def solve(grid: np.ndarray) -> int:
    w, h = grid.shape
    graph: nx.DiGraph = nx.grid_2d_graph(*grid.shape, create_using=nx.DiGraph)

    edges = {edge: grid[edge[1][0], edge[1][1]] for edge in graph.edges}

    nx.set_edge_attributes(graph, edges, name="risk")

    res = nx.dijkstra_path_length(
        graph,
        source=(0, 0),
        target=(w - 1, h - 1),
        weight="risk",
    )
    return res


def part1(data: np.ndarray) -> int:
    return solve(data)


def part2(data: np.ndarray) -> int:
    size = 5, 5
    h_exp = np.hstack([(data + i - 1) % 9 + 1 for i in range(size[0])])
    expanded = np.vstack([(h_exp + i - 1) % 9 + 1 for i in range(size[1])])
    return solve(expanded)
