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

def cache_key(state: State) -> tuple[int, int, str, int]:
    # without price !  step.price
    return (state.point.x, state.point.y, state.direction.name, state.price)

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

    return find_longest_path(start_pos=start_pos, end_pos=end_pos, m_offset=m_offset, slope=True)

def solve_2(in_file: str) -> int:
    matrix = parse(in_f=in_file)
    
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)

    start_pos = Point2D(y=offset, x=offset + 1)
    end_pos = Point2D(y=m_offset.shape[0]-offset-1, x = m_offset.shape[1]-offset-2)

    nodes: list[Point2D] = get_nodes(start_pos=start_pos, end_pos=end_pos, m_offset=m_offset)

    dist = get_distances(nodes=nodes, m_offset=m_offset)

    return get_longest(start_pos=start_pos, end_pos=end_pos, d=dist)


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

def print_matrix(s: State, m_offset: np.ndarray):
    cc = m_offset.copy()
    for i in s.visited:
        cc[i.y, i.x] = '0'
    for row in cc:
        print(' '.join(row))

def find_longest_path(start_pos : Point2D, end_pos: Point2D, m_offset: np.ndarray, slope: bool) -> int:

    s_i = State(point=start_pos, direction=Direction.SOUTH, price=0, visited=set())
    st = deque()
    st.append(s_i)

    h_price = {}

    max_price = 0
    while st:
        curr: State = st.pop()

        # print(curr)

        if curr.point == end_pos:
            max_price = max(curr.price, max_price)
            # print_matrix(s=curr, m_offset=m_offset)
            # print(max_price)
            continue

        # if cache_key(state=curr) in h_price:
        #     if h_price[cache_key(state=curr)] > curr.price:
        #         continue
        #     else:
        #         h_price[cache_key(state=curr)] = curr.price
        # else:
        #     h_price[cache_key(state=curr)] = curr.price
        h_price[cache_key(state=curr)] = h_price.get(cache_key(state=curr), 0) + 1 
        if h_price[cache_key(state=curr)] > 4:
            continue
        
        dir_s = get_dir_by_symbol(symbol=m_offset[curr.point.y, curr.point.x])
        
        dirs = [get_next_left_dir(direction=curr.direction), curr.direction, 
                get_next_right_dir(direction=curr.direction)]
        if dir_s and slope:
            dirs = [dir_s]

        for i in dirs:
            x = curr.point.x + i.value[1]
            y = curr.point.y + i.value[0]

            if m_offset[y, x] == '#':
                continue
            
            p = Point2D(x=x, y=y)

            if p in curr.visited:
                # print_matrix(s=curr, m_offset=m_offset)
                continue
            
            vis = curr.visited.copy()
            vis.add(curr.point)
            new_s = State(point=p, direction=i, price=curr.price+1, visited=vis)
            
            st.append(new_s)

            # try all variants
            # check if possible
            # check if not slope (freeze)
    return max_price


def get_longest(
    start_pos: Point2D, end_pos: Point2D, d: dict[Point2D, list[tuple[int, Point2D]]]) -> int:

    q = deque()
    q.append((start_pos, 0, frozenset([start_pos])))

    res = -1

    while q:
        curr = q.pop()

        if curr[0] == end_pos:
            res = max(res, curr[1])
            # print(res)
            continue

        for i in d[curr[0]]:

            price = i[0]
            p = i[1]
            
            if p in curr[2]:
                continue

            q.append((p, curr[1] + price, curr[2].union([p])))

    
    return res
    

def get_nodes(start_pos : Point2D, end_pos: Point2D, m_offset: np.ndarray) -> list[Point2D]:
    nodes: list[Point2D] = [start_pos, end_pos]
    for idx, x in np.ndenumerate(m_offset):
        if x not in ['#','b']:
            c = 0
            for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
                xx = idx[1] + d.value[1]
                yy = idx[0] + d.value[0]
                if m_offset[yy,xx] not in ['#','b']:
                    c += 1
            if c > 2:
                nodes.append(Point2D(x=idx[1], y=idx[0]))
    return nodes


def get_distances(nodes: list[Point2D], m_offset: np.ndarray) -> dict[Point2D, list[tuple[int, Point2D]]]:
    res = dict()
    for node in nodes:
        print(node)
        tmp = bfs(start_p=node, nodes=nodes, m_offset=m_offset)
        res[node] = tmp
    return res

def bfs(start_p: Point2D, nodes: list[Point2D], m_offset: np.ndarray):
    
    q = deque()
    q.append((start_p, 0))

    visited = set()

    res = []

    while q:
        curr: tuple[Point2D, int] = q.popleft()
        if curr[0] in visited:
            continue
        visited.add(curr[0])

        if curr[0] in nodes and curr[0] != start_p:
            res.append((curr[1], curr[0]))
            continue
        
        for i in [Direction.EAST, Direction.WEST, Direction.NORTH, Direction.SOUTH]:
            x = i.value[1] + curr[0].x
            y = i.value[0] + curr[0].y
            p = Point2D(x=x, y=y)

            if m_offset[y, x] == '#' or m_offset[y, x] == 'b':
                continue

            q.append((p, curr[1] + 1))
    return res


def cc(in_file: str):
    matrix = parse(in_f=in_file)
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)
    # for y, x in m_offset.shape:
    #     pass
    n = 0
    bl = 0
    for idx, x in np.ndenumerate(m_offset):
        # print(idx, x)
        if x not in ['#','b']:
            c = 0
            for d in [Direction.NORTH, Direction.SOUTH, Direction.EAST, Direction.WEST]:
                xx = idx[1] + d.value[1]
                yy = idx[0] + d.value[0]
                if m_offset[yy,xx] not in ['#','b']:
                    c += 1
            if c > 2:
                n +=1
            if c == 1:
                bl +=1
                print(idx, x)
    print(n)
    print(bl)
    # print(idx, x)

if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__).parent.resolve()
    input_file = os.path.join(curr_dir, 'test.txt')
    test_file = os.path.join(curr_dir, 'input_test.txt')
    assert solve_1(in_file=test_file) == 94
    assert solve_1(in_file=input_file) == 2298
    assert solve_2(in_file=test_file) == 154
    assert solve_2(in_file=input_file) == 6602
