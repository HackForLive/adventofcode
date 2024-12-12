from collections import deque
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc.model.direction import Direction, get_next_right_dir
from aoc.model.geometry import Point2D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'

import numpy as np


def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int) -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix


def bfs(s_pos: Tuple[int, int], matrix: np.ndarray, visited: Set[Tuple[int, int]]) -> int:
    stack = deque()
    stack.append(s_pos)

    region_char = matrix[s_pos[0], s_pos[1]]
    area = 0
    fence = 0

    while stack:
        curr = stack.popleft()
        val = matrix[curr[0], curr[1]]
        if val != region_char:
            continue
        if (curr[0], curr[1]) in visited:
            continue

        for p in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            y = curr[0] + p.value[0]
            x = curr[1] + p.value[1]
            if matrix[y, x] == region_char:
                stack.append((y, x))
            else:
                fence += 1
        visited.add(curr)
        area += 1
    # print(f"{region_char =}")
    # print(f"{area =}")
    # print(f"{fence =}")
    return area * fence


def get_price_of_fencing_all_regions(matrix: np.ndarray) -> int:
    res = 0
    visited = set()
    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == '1':
            continue
        if (y, x) in visited:
            continue
        res += bfs(s_pos=(y, x), matrix=matrix, visited=visited)
    return res


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val='1', offset=1)
        return get_price_of_fencing_all_regions(matrix=matrix_with_offset)
    

# @timer_decorator
# def solve_2(p: Path) -> int:
#     with open(p, encoding='utf-8', mode='r') as f:
#         arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
#         matrix = np.asmatrix(arr_2d)
#         matrix_with_offset = get_matrix_with_offset(matrix=matrix, val='1', offset=1)
#         return get_price_of_fencing_all_regions(matrix=matrix_with_offset)

if __name__ == '__main__':
    # solve_1(p=t2_f)
    assert solve_1(p=t_f) == 1930
    assert solve_1(p=t2_f) == 140
    assert solve_1(p=in_f) == 1361494
    print("All passed!")
