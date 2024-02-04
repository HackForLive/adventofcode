from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
import os
import pathlib
import heapq

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


class Direction(Enum):
    """
    N/S/E/W
    """
    NORTH = [-1, 0]
    EAST = [0, 1]
    SOUTH = [1, 0]
    WEST = [0, -1]

    @classmethod
    def get_name_by_value(cls,val):
        return { v:k for k,v in dict(vars(cls)).items() if isinstance(v,list)}.get(val,None)


@dataclass
class Step:
    """
    Current step identified by
    position (x,y)
    current direction
    current heat loss
    current steps (incremented by same direction)
    """
    x: int
    y: int
    direction: Direction
    heat_loss: int
    steps: int

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


def cache_key(step: Step) -> int:
    x, y, direction, steps = step.x, step.y, get_number_from_direction(step.direction), step.steps

    # return (x << (8 + 3 + 4)) | (y << (3 + 4)) | (dir << 4) | steps; // bit shift is safer
    c_key = (((x + 1) * 37 + (y + 1) * 17) * 5 + direction) * 9 + steps
    return c_key


def get_number_from_direction(d: Direction):
    if d == Direction.EAST:
        return 1
    if d == Direction.NORTH:
        return 2
    if d == Direction.WEST:
        return 3
    if d == Direction.SOUTH:
        return 4
    raise ValueError('Unexpected')


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

def get_directions(d: Direction):
    return [d, get_next_left_dir(d), get_next_right_dir(d)]

def shortest_path(m: np.matrix, min_steps: int, max_steps: int, offset: int):
    start_east = Step(offset, offset, Direction.EAST, 0, 0)
    start_south = Step(offset, offset, Direction.SOUTH, 0, 0)
    pq = []
    heapq.heappush(pq, start_south)
    heapq.heappush(pq, start_east)

    # visited
    visited = set()

    visited.add(cache_key(start_east))
    visited.add(cache_key(start_south))

    while pq:
        u = heapq.heappop(pq)

        # get the right bottom element
        if u.x == m.shape[1] - offset*2 and u.y == m.shape[1] - offset*2:
            return u.heat_loss

        for c_dir in get_directions(u.direction):
            ny = u.y + c_dir.value[0]
            nx = u.x + c_dir.value[1]
            weight = m[ny, nx]

            # border case
            if weight == -1:
                continue

            # handle minimum steps to turn
            if u.steps < min_steps and c_dir != u.direction:
                continue

            # handle too many steps in the same direction
            if u.steps > max_steps - 1 and c_dir == u.direction:
                continue

            next_step: Step = Step(
                nx,
                ny,
                c_dir,
                (u.heat_loss + weight),
                (u.steps + 1 if u.direction == c_dir else 1)
            )
            if not cache_key(next_step) in visited:
                heapq.heappush(pq, next_step)
                visited.add(cache_key(next_step))
    return -1


def solve_1():
    matrix = parse()
    offset = 1
    border = -1
    matrix = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    # print(matrix)
    print(shortest_path(m=matrix, min_steps=1, max_steps=3, offset=1))


if __name__ == '__main__':
    solve_1()
    # solve_2()
