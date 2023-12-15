from __future__ import annotations
from collections import deque
import os
import pathlib
from typing import List, Tuple
from itertools import cycle

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

def get_north_move(rocks: List[Tuple[int, int]], fix_rocks: List[Tuple[int, int]], n: int):
    rocks_moved = []

    # TODO careful with sorting
    s_rocks = sorted(rocks, key=lambda x: x[0], reverse=False)
    # print(rocks)
    # print(fix_rocks)
    for rock in s_rocks:
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
    # print(rocks_moved)
    return rocks_moved

def get_south_move(rocks: List[Tuple[int, int]], fix_rocks: List[Tuple[int, int]], n: int):
    rocks_moved = []

    s_rocks = sorted(rocks, key=lambda x: x[0], reverse=True)
    # print(rocks)
    # print(fix_rocks)
    for rock in s_rocks:
        y_new = n - 1
        x_new = rock[1]
        obstacles = fix_rocks + rocks_moved
        for obstacle in obstacles:
            # same col and lower
            if obstacle[1] == rock[1] and obstacle[0] > rock[0]:
                if obstacle[0] < y_new:
                    y_new = obstacle[0]
                if obstacle[0] == y_new:
                    y_new = y_new - 1
        # print(f"{y_new}, {x_new}")
        rocks_moved.append((y_new, x_new))
    return rocks_moved

def get_east_move(rocks: List[Tuple[int, int]], fix_rocks: List[Tuple[int, int]], n: int):
    rocks_moved = []

    s_rocks = sorted(rocks, key=lambda x: x[1], reverse=True)
    # print(rocks)
    # print(fix_rocks)
    for rock in s_rocks:
        y_new = rock[0]
        x_new = n - 1
        obstacles = fix_rocks + rocks_moved
        for obstacle in obstacles:
            # same col and lower
            if obstacle[0] == rock[0] and obstacle[1] > rock[1]:
                if obstacle[1] < x_new:
                    x_new = obstacle[1]
                if obstacle[1] == x_new:
                    x_new = x_new - 1
        # print(f"{y_new}, {x_new}")
        rocks_moved.append((y_new, x_new))
    # print(rocks_moved)
    return rocks_moved

def get_west_move(rocks: List[Tuple[int, int]], fix_rocks: List[Tuple[int, int]], n: int):
    rocks_moved = []

    s_rocks = sorted(rocks, key=lambda x: x[1], reverse=False)
    # print(rocks)
    # print(fix_rocks)
    for rock in s_rocks:
        y_new = rock[0]
        x_new = 0
        obstacles = fix_rocks + rocks_moved
        for obstacle in obstacles:
            # same col and lower
            if obstacle[0] == rock[0] and obstacle[1] < rock[1]:
                if obstacle[1] > x_new:
                    x_new = obstacle[1]
                if obstacle[1] == x_new:
                    x_new = x_new + 1
        # print(f"{y_new}, {x_new}")
        rocks_moved.append((y_new, x_new))
    # print(rocks_moved)
    return rocks_moved

def _north_load(rocks: List[Tuple[int, int]], n: int):
    res = 0
    for rock in rocks:
        res += n - rock[0]
    return res

def solve_1():
    matrix = parse()
    rocks, fix_rocks = get_rocks(matrix=matrix)
    n = matrix.shape[0]
    rocks_moved = get_north_move(rocks=rocks, fix_rocks=fix_rocks, n=n)
    load = _north_load(rocks=rocks_moved, n=n)
    print(load)

def solve_2():
    matrix = parse()
    rocks, fix_rocks = get_rocks(matrix=matrix)
    rocks_moved = rocks

    for _ in range(200):
        rocks_moved = get_north_move(rocks=rocks_moved, fix_rocks=fix_rocks, n = matrix.shape[0])
        rocks_moved = get_west_move(rocks=rocks_moved, fix_rocks=fix_rocks, n = matrix.shape[1])
        rocks_moved = get_south_move(rocks=rocks_moved, fix_rocks=fix_rocks, n = matrix.shape[0])
        rocks_moved = get_east_move(rocks=rocks_moved, fix_rocks=fix_rocks, n = matrix.shape[1])
        # print(rocks_moved)
        load = _north_load(rocks=rocks_moved, n=matrix.shape[0])
        print(f"{_} {load}")

if __name__ == '__main__':
    solve_1()
    # TODO optimize and find the cycle programatically
    solve_2()
