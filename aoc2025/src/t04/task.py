from collections import deque
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc.model.direction import Direction, get_next_right_dir
from aoc.model.geometry import Point2D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np


def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int) -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def get_rolls(s_pos: Tuple[int, int], matrix: np.ndarray) -> int:
    res = 0
    stack = deque()
    stack.append(s_pos)

    vis = set()

    while stack:
        curr = stack.popleft()
        val = matrix[curr[0], curr[1]]
        if val == '#':
            continue

        if (curr[0], curr[1]) in vis:
            continue

        if val == '@':
            cc = 0
            for i in [-1,0,1]:
                for j in [-1,0,1]:
                    if (i + curr[0] == curr[0]) and (j + curr[1] == curr[1]):
                        continue
                    if matrix[i + curr[0], j + curr[1]] == '@':
                        cc = cc + 1
            
            if cc < 4:
                res += 1

        for p in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            y = curr[0] + p.value[0]
            x = curr[1] + p.value[1]
            stack.append((y, x))
        
        vis.add((curr[0], curr[1]))
    return res


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val='#', offset=1)
        start_pos = (1,1)
        # print(matrix_with_offset)
        return get_rolls(s_pos = start_pos, matrix=matrix_with_offset)
    

@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val='#', offset=1)
        start_pos = (1,1)
        # print(matrix_with_offset)
        return get_rolls(s_pos = start_pos, matrix=matrix_with_offset)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 13
    print(solve_1(p=in_f)) # 1457
    assert solve_2(p=t_f) == 43 # can be removed
    # assert solve_2(p=in_f) == 1058
    print("All passed!")
