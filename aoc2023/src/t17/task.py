from __future__ import annotations
from enum import Enum
import os
import pathlib
import heapq
from typing import List, Tuple

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')

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
    def __init__(self, point: Tuple[int, int], direction: Direction, value: int) -> None:
        self.point = point
        self.direction = direction
        self.value = value
        self.path_history: List[Instruction] = []

    def __eq__(self, obj):
        return isinstance(obj, Instruction) and (obj.point == self.point
                                                 and obj.direction == self.direction)

    def __hash__(self):
        return hash((self.point, self.direction))

    def __lt__(self, other):
        return self.value < other.value

    def __repr__(self):
        return f"Instruction(p={self.point}, dir={self.direction})"


def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val,
                             dtype=int)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix

def bfs_with_weights(matrix: np.matrix, start_instr: Instruction, shape):
    # TODO: improve with Dijkstra algo
    q = []
    heapq.heappush(q, start_instr)

    n_max = 10000

    closest_m = np.zeros(shape=matrix.shape, dtype=int) + n_max
    closest_m[start_instr.point] = 0

    while q:
        curr: Instruction = heapq.heappop(q)

        if curr.point[0] == matrix.shape[0] and curr.point[1] == shape[1]:
            n_max = closest_m[shape[0], shape[1]]

        for direction in (curr.direction, get_next_left_dir(curr.direction),
                          get_next_right_dir(curr.direction)):
            if len(curr.path_history) >= 3 and (
                curr.path_history[-1].direction == curr.path_history[-2].direction) and (
                    curr.path_history[-2].direction == curr.path_history[-3].direction
                ):
                if direction == curr.direction:
                    continue

            x = curr.point[1] + direction.value[1]
            y = curr.point[0] + direction.value[0]
            val = matrix[y, x]

            new_instr = Instruction(point=(y,x), direction=direction, value=val)
            new_instr.path_history = curr.path_history
            new_instr.path_history.append(curr)

            # border
            if val == -1 or (closest_m[y, x] <= val + closest_m[curr.point[0], curr.point[1]]):
                continue
            closest_m[y, x] = val + closest_m[curr.point[0], curr.point[1]]
            # q.append(Node(x=x, y=y, value=val, path=curr.path + [(y,x)]))
            heapq.heappush(q, new_instr)

    print(closest_m)
    return closest_m[shape[0], shape[1]]

def solve_1():
    matrix = parse()
    offset = 1
    border = -1
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    start_pos = (offset,offset)
    start_instr = Instruction(point=start_pos, direction=Direction.EAST, value=m_offset[start_pos])
    start_instr.path_history.append(start_instr)
    print(bfs_with_weights(matrix=m_offset, start_instr=start_instr, shape=matrix.shape))


if __name__ == '__main__':
    solve_1()
    # solve_2()
