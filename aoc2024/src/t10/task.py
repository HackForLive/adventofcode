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


def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int) -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=int)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def find_start(start: int, matrix: np.ndarray) -> List[Tuple[int, int]]:
    return [(int(i[0]), int(i[1])) for i in zip(*np.where(matrix == start))]


def get_hiking_trail_score(s_pos: List[Tuple[int, int]], matrix: np.ndarray) -> int:
    t_res = 0
    # print(s_pos)
    for s in s_pos:
        stack = deque()
        stack.append(s)

        res = set()
        while stack:
            curr = stack.popleft()
            val = matrix[curr[0], curr[1]]
            if val == -1:
                continue

            if val == 9:
                res.add(curr)
                continue

            for p in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
                y = curr[0] + p.value[0]
                x = curr[1] + p.value[1]
                if matrix[y, x] == val + 1:
                    stack.append((y, x))
        t_res += len(res)
    return t_res


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[int(c) for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=-1, offset=1)
        start_pos = find_start(start=0, matrix=matrix_with_offset)
        return get_hiking_trail_score(s_pos = start_pos, matrix=matrix_with_offset)
    
if __name__ == '__main__':
    assert solve_1(p=t_f) == 36
    assert solve_1(p=in_f) == 510
    # assert solve_2_naive(p=t_f) == 6
    # assert solve_2_naive(p=in_f) == 1503
    # print(solve_2(p=in_f))
    print("All passed!")
