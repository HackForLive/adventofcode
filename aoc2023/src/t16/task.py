from __future__ import annotations
from collections import deque
from enum import Enum
import os
import pathlib
from typing import Tuple

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

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
    def __init__(self, point: Tuple[int, int], direction: Direction) -> None:
        self.point = point
        self.direction = direction

    def __eq__(self, obj):
        return isinstance(obj, Instruction) and (obj.point == self.point
                                                 and obj.direction == self.direction)

    def __hash__(self):
        return hash((self.point, self.direction))

    def __repr__(self):
        return f"Instruction(p={self.point}, dir={self.direction})"


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
        return matrix


def simulate(start_instr: Instruction, matrix: np.matrix, border: str):
    q = deque()
    q.append(start_instr)

    visited_map = np.zeros(matrix.shape, dtype=int)
    visited = set()
    # print(visited)
    while q:
        curr: Instruction = q.pop()
        if curr in visited:
            continue

        next_p = (curr.point[0] + curr.direction.value[0], curr.point[1] + curr.direction.value[1])

        if matrix[next_p] == '/':
            if curr.direction == Direction.WEST:
                q.append(Instruction(point=next_p, direction=Direction.SOUTH))
            elif curr.direction == Direction.SOUTH:
                q.append(Instruction(point=next_p, direction=Direction.WEST))
            elif curr.direction == Direction.EAST:
                q.append(Instruction(point=next_p, direction=Direction.NORTH))
            elif curr.direction == Direction.NORTH:
                q.append(Instruction(point=next_p, direction=Direction.EAST))
        elif matrix[next_p] == "\\":
            if curr.direction == Direction.WEST:
                q.append(Instruction(point=next_p, direction=Direction.NORTH))
            elif curr.direction == Direction.NORTH:
                q.append(Instruction(point=next_p, direction=Direction.WEST))
            elif curr.direction == Direction.EAST:
                q.append(Instruction(point=next_p, direction=Direction.SOUTH))
            elif curr.direction == Direction.SOUTH:
                q.append(Instruction(point=next_p, direction=Direction.EAST))
        elif matrix[next_p] == '-':
            if curr.direction in [Direction.WEST, Direction.EAST]:
                q.append(Instruction(point=next_p, direction=curr.direction))
            elif curr.direction in [Direction.SOUTH, Direction.NORTH]:
                q.append(Instruction(point=next_p, direction=Direction.EAST))
                q.append(Instruction(point=next_p, direction=Direction.WEST))
        elif matrix[next_p] == '|':
            if curr.direction in [Direction.SOUTH, Direction.NORTH]:
                q.append(Instruction(point=next_p, direction=curr.direction))
            elif curr.direction in [Direction.WEST, Direction.EAST]:
                q.append(Instruction(point=next_p, direction=Direction.NORTH))
                q.append(Instruction(point=next_p, direction=Direction.SOUTH))
        elif matrix[next_p] == '.':
            q.append(Instruction(point=next_p, direction=curr.direction))
        elif matrix[next_p] == border:
            pass
        else:
            raise ValueError('erroor')
        visited_map[curr.point] = 1
        # print(visited)
        visited.add(curr)
    # print(visited)
    indeces = np.where(visited_map == 1)
    # print(visited)

    # start from (1,0)
    return len(indeces[0]) - 1

def solve_1():
    matrix = parse()
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    start_pos = (1,0)
    s_i =Instruction(point=start_pos, direction=Direction.EAST)
    print(simulate(start_instr=s_i, matrix=m_offset, border=border))


def solve_2():
    matrix = parse()
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    res = 0
    for tp in range(offset, matrix.shape[1]):
        start_pos = (0,tp)
        s_i =Instruction(point=start_pos, direction=Direction.SOUTH)
        tmp = simulate(start_instr=s_i, matrix=m_offset, border=border)
        res = max(tmp, res)
        start_pos = (m_offset.shape[0]-1,tp)
        s_i =Instruction(point=start_pos, direction=Direction.NORTH)
        tmp = simulate(start_instr=s_i, matrix=m_offset, border=border)
        res = max(tmp, res)

    for tp in range(offset, matrix.shape[0]):
        start_pos = (tp,0)
        s_i =Instruction(point=start_pos, direction=Direction.EAST)
        tmp = simulate(start_instr=s_i, matrix=m_offset, border=border)
        res = max(tmp, res)
        start_pos = (tp,m_offset.shape[1]-1)
        s_i =Instruction(point=start_pos, direction=Direction.WEST)
        tmp = simulate(start_instr=s_i, matrix=m_offset, border=border)
        res = max(tmp, res)
    print(res)

if __name__ == '__main__':
    solve_1()
    solve_2()
