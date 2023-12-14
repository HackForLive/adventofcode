from __future__ import annotations
from collections import deque
import os
import pathlib
from typing import List, Tuple

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val,
                             dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([list(line.strip()) for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        # return get_matrix_with_offset(matrix=matrix, val='b', offset=1)
        return matrix

def get_rocks(matrix: np.matrix):
    rocks = []
    fix_rocks = []
    for row in range(matrix.shape[0]):
        for col in range(matrix.shape[1]):
            if matrix[row, col] == 'O':
                rocks.append((row, col))
            elif matrix[row, col] == '#':
                fix_rocks.append((row, col))
    # print(rocks)
    # print(fix_rocks)
    return rocks, fix_rocks

def get_load(rocks: List[Tuple[int, int]], fix_rocks: List[Tuple[int, int]], n: int):
    rocks_moved = []

    # print(rocks)
    # print(fix_rocks)
    for rock in rocks:
        y_new = 0
        x_new = rock[1]
        obstacles = fix_rocks + rocks_moved
        for obstacle in obstacles:
            # same col and lower
            if obstacle[1] == rock[1] and obstacle[0] < rock[0]:
                if obstacle[0] > y_new:
                    y_new = obstacle[0]
                if obstacle[0] == y_new:
                    y_new = y_new + 1
        # print(f"{y_new}, {x_new}")
        rocks_moved.append((y_new, x_new))
    print(rocks_moved)

    res = 0
    for rock in rocks_moved:
        res += n - rock[0]
    return res

def solve_1():
    matrix = parse()
    rocks, fix_rocks = get_rocks(matrix=matrix)
    load = get_load(rocks=rocks, fix_rocks=fix_rocks, n = matrix.shape[0])
    print(load)

if __name__ == '__main__':
    solve_1()
    # solve_2()
