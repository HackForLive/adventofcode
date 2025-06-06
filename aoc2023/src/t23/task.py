from __future__ import annotations
from collections import deque
from dataclasses import dataclass
import os
import pathlib

import numpy as np

from aoc.model.direction import Direction, get_next_left_dir, get_next_right_dir
from aoc.model.geometry import Point2D


@dataclass(frozen=True, init=True)
class State:
    """
    track point
    direction
    price
    """
    point: Point2D
    direction: Direction
    price: int
    visited: set[Point2D]

    def __eq__(self, obj):
        return isinstance(obj, State) and (obj.point == self.point
                                           and obj.direction == self.direction
                                           and obj.price == self.price)

    def __hash__(self):
        return hash((self.point, self.direction, self.price))
    
    def __lt__(self, other):
        return self.price < other.price

    def __repr__(self):
        return f"State(p={self.point}, dir={self.direction}, price={self.price})"

def cache_key(state: State) -> tuple[int, int, str]:
    # without price !  step.price
    return (state.point.x, state.point.y, state.direction.name)

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

    start_pos = Point2D(y=offset, x=offset + 1)
    end_pos = Point2D(y=m_offset.shape[0]-offset-1, x = m_offset.shape[1]-offset-2)

    return find_longest_path(start_pos=start_pos, end_pos=end_pos, m_offset=m_offset)


def get_dir_by_symbol(symbol: str) -> Direction | None:
    if symbol == '^':
        return Direction.NORTH
    if symbol == 'v':
        return Direction.SOUTH
    if symbol == '>':
        return Direction.EAST
    if symbol == '<':
        return Direction.WEST
    
    return None

def find_longest_path(start_pos : Point2D, end_pos: Point2D, m_offset: np.ndarray) -> int:

    s_i = State(point=start_pos, direction=Direction.SOUTH, price=0, visited=set())
    st = deque()
    st.append(s_i)

    keep_h_price = {}

    max_price = 0
    while st:
        curr: State = st.pop()

        if cache_key(state=curr) in keep_h_price:
            if keep_h_price[cache_key(state=curr)] > curr.price:
                continue
        else:
            keep_h_price[cache_key(state=curr)] = curr.price 

        if curr.point == end_pos:
            max_price = max(curr.price, max_price)
            # for i in curr.visited:
            #     m_offset[i.y, i.x] = '0'
            # for row in m_offset:
            #     print(' '.join(row))
            continue
        
        dir_s = get_dir_by_symbol(symbol=m_offset[curr.point.y, curr.point.x])
        
        dirs = [get_next_left_dir(direction=curr.direction), curr.direction, 
                get_next_right_dir(direction=curr.direction)]
        if dir_s:
            dirs = [dir_s]

        for i in dirs:
            x = curr.point.x + i.value[1]
            y = curr.point.y + i.value[0]

            if m_offset[y, x] == '#':
                continue
            
            p = Point2D(x=x, y=y)

            if p in curr.visited:
                continue
            
            vis = curr.visited.copy()
            vis.add(curr.point)
            new_s = State(point=p, direction=i, price=curr.price+1, visited=vis)
            
            st.append(new_s)

            # try all variants
            # check if possible
            # check if not slope (freeze)
    return max_price

if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__).parent.resolve()
    input_file = os.path.join(curr_dir, 'test.txt')
    test_file = os.path.join(curr_dir, 'input_test.txt')
    assert solve_1(in_file=test_file) == 94
    assert solve_1(in_file=input_file) == 2298
