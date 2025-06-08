from __future__ import annotations
from collections import deque
import os
import pathlib

import numpy as np

from aoc.model.direction import Direction
from aoc.model.geometry import Point2D
from aoc.performance import timer_decorator


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

@timer_decorator
def solve(in_file: str, slippery: bool) -> int:
    matrix = parse(in_f=in_file)
    
    offset = 1
    border = 'b'
    m_offset = get_matrix_with_offset(matrix=matrix, val=border, offset=offset)

    start_pos = Point2D(y=offset, x=offset + 1)
    end_pos = Point2D(y=m_offset.shape[0]-offset-1, x = m_offset.shape[1]-offset-2)

    nodes: list[Point2D] = get_nodes(start_pos=start_pos, end_pos=end_pos, m_offset=m_offset)

    dist = get_distances(nodes=nodes, m_offset=m_offset, slippery=slippery)

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

def print_matrix(visited: set[Point2D], m_offset: np.ndarray):
    cc = m_offset.copy()
    for i in visited:
        cc[i.y, i.x] = '0'
    for row in cc:
        print(' '.join(row))

def get_longest(
    start_pos: Point2D, end_pos: Point2D, d: dict[Point2D, list[tuple[int, Point2D]]]) -> int:

    q = deque()
    q.append((start_pos, 0, frozenset([start_pos])))
    res = -1

    while q:
        curr = q.pop()

        if curr[0] == end_pos:
            res = max(res, curr[1])
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

@timer_decorator
def get_distances(nodes: list[Point2D], m_offset: np.ndarray, slippery: bool
                  ) -> dict[Point2D, list[tuple[int, Point2D]]]:
    return {node: bfs(start_p=node, nodes=nodes, m_offset=m_offset, slippery=slippery) 
            for node in nodes}

def bfs(start_p: Point2D, nodes: list[Point2D], m_offset: np.ndarray, slippery: bool):
    
    q = deque()
    q.append((start_p, 0))

    visited = set()
    res = []

    directions = [Direction.EAST, Direction.WEST, Direction.NORTH, Direction.SOUTH]

    while q:
        curr: tuple[Point2D, int] = q.popleft()
        if curr[0] in visited:
            continue
        visited.add(curr[0])

        if curr[0] in nodes and curr[0] != start_p:
            res.append((curr[1], curr[0]))
            continue

        dirs = directions
        if slippery:
            dir_s = get_dir_by_symbol(symbol=m_offset[curr[0].y, curr[0].x])
            dirs = [dir_s] if dir_s else dirs
        
        for i in dirs:
            x = i.value[1] + curr[0].x
            y = i.value[0] + curr[0].y

            if m_offset[y, x] in ['#', 'b']:
                continue

            q.append((Point2D(x=x, y=y), curr[1] + 1))
    return res

if __name__ == '__main__':
    curr_dir = pathlib.Path(__file__).parent.resolve()
    input_file = os.path.join(curr_dir, 'test.txt')
    test_file = os.path.join(curr_dir, 'input_test.txt')
    assert solve(in_file=test_file, slippery=True) == 94
    assert solve(in_file=input_file, slippery=True) == 2298
    assert solve(in_file=test_file, slippery=False) == 154
    assert solve(in_file=input_file, slippery=False) == 6602
