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
        return get_matrix_with_offset(matrix=matrix, val='b', offset=1)

def find_start(start: str, matrix: np.matrix):
    res = np.where(matrix == start)
    return int(res[0][0]), int(res[1][0])

def bfs(token: str, start_idx: Tuple[int, int], matrix: np.numpy) -> Tuple[bool, int]:
    is_cycle = False
    cycle_len = 0
    paths = np.zeros(shape=matrix.shape, dtype=int)
    # print(f"{start_idx =}, {token =}")

    paths[start_idx] = -1
    stack = deque()
    for p in pipe_mapping(pipe=token):
        # print(f"{p =}")
        stack.append((p[0] + start_idx[0], p[1] + start_idx[1]))
        paths[(p[0] + start_idx[0], p[1] + start_idx[1])] = 1
        # first one
        break

    while stack and not is_cycle:
        curr = stack.pop()
        pipe = matrix[curr[0], curr[1]]
        # print(f"{curr =}, {pipe =}")

        if pipe == 'b' or pipe == '.':
            continue
        if pipe == 'S':
            is_cycle = True
            break

        for k in pipe_mapping(pipe=pipe):
            tmp = (k[0] + curr[0], k[1] + curr[1])
            if cycle_len < 3 and paths[tmp] == -1:
                continue
            if paths[tmp] == -1:
                is_cycle = True
            if paths[tmp] != 0:
                continue
            stack.append(tmp)
            paths[tmp] = paths[curr] + 1
        cycle_len = cycle_len + 1

    print(paths)
    return is_cycle, cycle_len

def pipe_mapping(pipe: str) -> List[Tuple[int, int]]:
    pipe_dic = {
        'L' : [(-1, 0), (0, 1)], 
        '|' : [(1, 0), (-1, 0)],
        '7': [(1, 0), (0, -1)],
        '-': [(0, 1), (0, -1)],
        'F': [(1, 0), (0, 1)],
        'J': [(-1, 0), (0, -1)]
    }

    return pipe_dic[pipe]


def solve_1():
    matrix = parse()
    start_idx = find_start(start='S', matrix=matrix)

    # cycle length
    # + find cycle

    start = ['L', '|', '7', '-', 'F', 'J']

    for s in start:
        is_cycle, length = bfs(token=s, start_idx=start_idx, matrix=matrix)
        if is_cycle:
            print(length)
            print((length+1)/2)
            break

if __name__ == '__main__':
    solve_1()
