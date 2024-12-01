from __future__ import annotations
from collections import deque
import os
import pathlib

import numpy as np

from aoc.model.direction import Direction
from aoc.model.geometry import Point2D



class Instruction:
    def __init__(self, point: Point2D, direction: Direction) -> None:
        self.point = point
        self.direction = direction

    def __eq__(self, obj):
        return isinstance(obj, Instruction) and (obj.point == self.point
                                                 and obj.direction == self.direction)

    def __hash__(self):
        return hash((self.point, self.direction))

    def __repr__(self):
        return f"Instruction(p={self.point}, dir={self.direction})"


def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int)  -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val,
                             dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def parse(in_f: str):
    with open(in_f, 'r', encoding='utf8') as f:
        arr_2d = np.array([list(line.strip()) for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix


def solve_1(in_file: str) -> int:
    matrix = parse(in_f=in_file)
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    # print(m_offset)
    start_pos = Point2D(y=offset + 0, x=offset + 1)
    s_i = Instruction(point=start_pos, direction=Direction.SOUTH)
    return find_longest_path(start_i=s_i, m_offset=m_offset)

def find_longest_path(start_i : Instruction, m_offset: np.ndarray) -> int:
    st = deque()
    st.append(start_i)

    # try all variants
    # check if possible
    # check if not slope (freeze)

    while st:

    return 0

if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__).parent.resolve()
    input_file = os.path.join(curr_dir, 'test.txt')
    test_file = os.path.join(curr_dir, 'input_test.txt')
    solve_1(in_file=test_file)
    # solve_2()
