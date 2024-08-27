from __future__ import annotations
from collections import deque
from enum import Enum
import os
import pathlib
from typing import Tuple

import numpy as np
from pydantic import BaseModel


class Point2D(BaseModel):
    """
    Represents point using cartesian coordinates of two-dimensional space
    """
    x: int
    y: int

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )

    def __add__(self, o):
        return Point2D(x=self.x+o.x, y=self.y + o.y)


class Direction(Enum):
    NORTH = [-1, 0]
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]

    @classmethod
    def get_name_by_value(cls,val):
        return { v:k for k,v in dict(vars(cls)).items() if isinstance(v,list)}.get(val,None)

def get_next_left_dir(direction: Direction):
    """
    Turn 90 degrees in counter clockwise manner 
    """
    directions = {
        Direction.NORTH: Direction.WEST,
        Direction.WEST: Direction.SOUTH,
        Direction.SOUTH: Direction.EAST,
        Direction.EAST: Direction.NORTH
    }
    return directions[direction]

def get_next_right_dir(direction: Direction):
    """
    Turn 90 degrees in clockwise manner 
    """
    directions = {
        Direction.NORTH: Direction.EAST,
        Direction.EAST: Direction.SOUTH,
        Direction.SOUTH: Direction.WEST,
        Direction.WEST: Direction.NORTH
    }
    return directions[direction]


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
    s_i =Instruction(point=start_pos, direction=Direction.SOUTH)
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
