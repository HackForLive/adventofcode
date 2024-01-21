from __future__ import annotations
from enum import Enum
import os
import pathlib
import heapq
from typing import List, Tuple
from copy import deepcopy

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')

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


class Node:
    prev: Direction
    count: int
    def __init__(self, point: Tuple[int, int], direction: Direction, prev: Node) -> None:
        self.point = point
        self.direction = direction
        self.prev = prev


    # def __eq__(self, obj):
    #     return isinstance(obj, Node) and (obj.point == self.point
    #                                              and obj.direction == self.direction
    #                                              and obj.value == self.value)

    # def __hash__(self):
    #     return hash((self.point, self.direction.name, self.value))

    # def __lt__(self, other):
    #     return self.value < other.value


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


def get_number_from_direction(d: Direction):
    if d == Direction.EAST:
        return 0
    if d == Direction.NORTH:
        return 1
    if d == Direction.WEST:
        return 2
    if d == Direction.SOUTH:
        return 3
    raise ValueError('Unexpected')


def get_label(n: int, node: Node, offset: int):
    return (node.point[0]-offset)*n + (node.point[1]-offset)


def shortest_path(m: np.matrix, src: Node):
    # Create a priority queue to store vertices that
    # are being preprocessed
    pq = []
    heapq.heappush(pq, (0, src))

    # distance map
    dist = np.ones(shape=m.shape, dtype=float) * float('inf')

    # distances as infinite (INF)
    # dist = [float('inf')] * n
    # previous node
    # prev = [float('inf')] * n

    dist[src.point] = 0

    while pq:
        # The first vertex in pair is the minimum distance
        # vertex, extract it from priority queue.
        # vertex label is stored in second of pair
        d, u = heapq.heappop(pq)

        # 'i' is used to get all adjacent vertices of a
        # vertex
        for c_dir in [u.direction, get_next_left_dir(u.direction),
                          get_next_right_dir(u.direction)]:

            y = u.point[0] + c_dir.value[0]
            x = u.point[1] + c_dir.value[1]
            p = (y, x)
            weight = m[p]
            # border
            if weight == -1:
                continue

            # If there is shorted path to v through u.
            if dist[p] > dist[u.point] + weight:
                # Updating distance of v
                dist[p] = dist[u.point] + weight
                # prev[p] = u
                heapq.heappush(pq, (dist[p], Node(point=p, direction=c_dir, prev=u)))

    # Print shortest distances stored in dist[]
    print(dist)
    print(dist[-2,-2])



def solve_1():
    matrix = parse()
    offset = 1
    border = -1
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    start_pos = (offset, offset)
    print(start_pos)
    src_node = Node(point=start_pos, direction=Direction.EAST, prev=None)
    shortest_path(m=m_offset, src=src_node)


if __name__ == '__main__':
    solve_1()
    # solve_2()
