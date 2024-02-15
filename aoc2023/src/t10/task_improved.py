from __future__ import annotations
from collections import deque
from enum import Enum
import os
import pathlib
from typing import List, NamedTuple, Tuple

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
        return { v:k for k,v in dict(vars(cls)).items() if isinstance(v,list)}.get(val, None)


class Node(NamedTuple):
    """
    Current Node
    """
    x: int
    y: int
    direction: Direction

    def __eq__(self, obj):
        return isinstance(obj, Node) and (obj.x == self.x
                                               and obj.y == self.y
                                               and obj.direction == self.direction)

    def __hash__(self):
        return hash((self.x, self.y))


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
        return get_matrix_with_offset(matrix=matrix, val='b', offset=1)

def find_start(start: str, matrix: np.matrix):
    res = np.where(matrix == start)
    return int(res[0][0]), int(res[1][0])

def bfs(token: str, start_idx: Tuple[int, int], matrix: np.numpy) -> Tuple[
    bool, int, List[Node]]:

    is_cycle = False
    cycle_len = 0
    # paths = np.zeros(shape=matrix.shape, dtype=int)

    # paths[start_idx] = -1
    stack = deque()
    memo: List[Node] = []
    visited = set()
    for p in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
        new_dir = pipe_mapping(pipe=token, p=p)

        if new_dir:
            n = Node(y=start_idx[0], x=start_idx[1], direction=new_dir)
            stack.append(n)
            # one direction is enough
            break

    while stack and not is_cycle:
        curr: Node = stack.pop()
        memo.append(curr)

        y = curr.y + curr.direction.value[0]
        x = curr.x + curr.direction.value[1]

        pipe = matrix[y, x]

        if pipe in ['b', '.']:
            continue

        if curr in visited:
            is_cycle = True
            break
        visited.add(curr)

        k = pipe_mapping(pipe=pipe, p=curr.direction)
        if not k:
            continue
        tmp = Node(y=y, x=x, direction=k)

        stack.append(tmp)
        cycle_len = cycle_len + 1

    return is_cycle, cycle_len, memo


def pipe_mapping(pipe: str, p: Direction):
    if pipe == 'L':
        if p == Direction.SOUTH:
            return Direction.EAST
        if p == Direction.WEST:
            return Direction.NORTH
        return None

    if pipe == '|':
        if p in [Direction.SOUTH, Direction.NORTH]:
            return p
        return None

    if pipe == '7':
        if p == Direction.EAST:
            return Direction.SOUTH
        if p == Direction.NORTH:
            return Direction.WEST
        return None

    if pipe == '-':
        if p in [Direction.WEST, Direction.EAST]:
            return p
        return None

    if pipe == 'F':
        if p == Direction.NORTH:
            return Direction.EAST
        if p == Direction.WEST:
            return Direction.SOUTH
        return None

    if pipe == 'J':
        if p == Direction.SOUTH:
            return Direction.WEST
        if p == Direction.EAST:
            return Direction.NORTH
        return None
    return None


def solve_1():
    matrix = parse()
    start_idx = find_start(start='S', matrix=matrix)

    start = ['L', '|', '7', '-', 'F', 'J']

    # print(matrix)
    for s in start:
        matrix[start_idx] = s
        print(f"{s =}")
        is_cycle, length, memo = bfs(token=s, start_idx=start_idx, matrix=matrix)
        if is_cycle:
            print(length)
            print((length)/2)
            print((memo[0].y, memo[0].x))
            print((memo[-1].y, memo[-1].x))
            break


def points_inside(area: float, boarder_pts: int):
    i_pts = area - boarder_pts/2 + 1
    return i_pts


def polygon_area(nodes: List[Node]):
    # Initialize area
    area = 0.0

    polygon_pts = [(m.y, m.x) for m in nodes]
    n = len(polygon_pts)

    # Calculate value of shoelace formula
    j = n - 1
    for i in range(0,n):
        area += (polygon_pts[j][1] + polygon_pts[i][1]) * (polygon_pts[j][0] - polygon_pts[i][0])
        j = i   # j is previous vertex to i

    # Return absolute value
    return int(abs(area / 2.0))

def count_points_inside(matrix: np.matrix, nodes: List[Node]) -> int:
    x_min = min((m.x for m in nodes))
    x_max = max((m.x for m in nodes))
    y_min = min((m.y for m in nodes))
    y_max = max((m.y for m in nodes))

    board_points = set({(m.y, m.x) for m in nodes})

    # improve !!!
    def get_key(x: int, y: int):
        for i, n in enumerate(nodes):
            if n.x == x and n.y == y:
                return i

    total_points_inside = 0

    for y in range(y_min+1, y_max, 1):
        on_the_board = False
        ray_switch = 0
        for x in range(x_min, x_max+1, 1):
            # get the board
            if (y,x) in board_points:
                # if y == 8:
                #     print(f"{y} - ({y}, {x}) - {on_the_board=}")
                if not on_the_board:
                    ray_switch += 1
                    on_the_board = True
                else:
                    # are the pipes connected - with previous
                    # print((x, y))
                    # if y == 8:
                    #     print(f"{get_key(x=x-1, y=y)} - {get_key(x=x, y=y)}")
                    if abs(get_key(x=x-1, y=y)-get_key(x=x, y=y)) > 1.1:
                        ray_switch += 1

                # if y == 8:
                #     print(f"{y} - {ray_switch=}")

                continue

            on_the_board = False
            if ray_switch%2 == 1:
                # print((y, x))
                total_points_inside +=1

    return total_points_inside


def solve_2():
    matrix = parse()
    start_idx = find_start(start='S', matrix=matrix)

    start = ['L', '|', '7', '-', 'F', 'J']

    # print(matrix)
    for s in start:
        matrix[start_idx] = s
        print(f"{s =}")
        is_cycle, _, memo = bfs(token=s, start_idx=start_idx, matrix=matrix)

        if is_cycle:
            # print(count_points_inside(
            #     matrix=matrix, nodes=memo[:-1]))
            area = polygon_area(nodes=memo)
            ip = points_inside(area=area, boarder_pts=len(memo[:-1]))
            print(ip)
            break

if __name__ == '__main__':
    # solve_1()
    solve_2()
    # 1094 too high
    # 127 too low
