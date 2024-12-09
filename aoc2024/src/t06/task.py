from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc.model.direction import Direction, get_next_right_dir
from aoc.model.geometry import Point2D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np


def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int) -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def get_walk(start: Tuple[int, int], matrix: np.ndarray) -> List[Tuple[int, int, str]]:
    dir = Direction.NORTH
    pos = Point2D(x=start[1], y=start[0])

    path = []
    while matrix[pos.y, pos.x] != 'B':
        path.append((pos.y, pos.x, dir.name))

        y = pos.y + dir.value[0]
        x = pos.x + dir.value[1]
        if matrix[y, x] == '#':
            dir = get_next_right_dir(direction=dir)
        else:
            pos.y = y
            pos.x = x
    return path

def get_number_of_void_points_naive(start: Tuple[int, int], matrix: np.ndarray) -> int:
    """
    Naive way to try out only visited points => ~70 secs
    """
    res = 0
    pts = {(i[0], i[1]) for i in get_walk(start=start, matrix=matrix)}
    # print(pts)
    for pp in pts:
        yy = pp[0]
        xx = pp[1]
        if matrix[yy, yy] == '.':
            matrix[yy, xx] = '#'
            dir = Direction.NORTH
            pos = Point2D(x=start[1], y=start[0])
            visited = set()
            loop = False
            while matrix[pos.y, pos.x] != 'B':
                if (pos.y, pos.x, dir.name) in visited:
                    loop = True
                    break
                visited.add((pos.y, pos.x, dir.name))

                y = pos.y + dir.value[0]
                x = pos.x + dir.value[1]
                if matrix[y, x] == '#':
                    dir = get_next_right_dir(direction=dir)
                else:
                    pos.y = y
                    pos.x = x
            if loop:
                res += 1
            matrix[yy, xx] = '.'
    return res


def check_if_infinite_loop( 
        matrix: np.ndarray,
        s_pos: Tuple[int, int],
        d: Direction) -> bool:
    
    x_b = {}
    y_b = {}

    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == '#':
            p = (y, x)
            if x in x_b:
                x_b[x].append(p[0])
            else:
                x_b[x] = [p[0]]

            if y in y_b:
                y_b[y].append(p[1])
            else:
                y_b[y] = [p[1]]
    
    # sort
    for k in x_b.keys():
        x_b[k] = sorted(x_b[k], key=lambda x: x, reverse=False)

    for k in y_b.keys():
        y_b[k] = sorted(y_b[k], key=lambda x: x, reverse=False)



    pos = (s_pos[0], s_pos[1])
    dir = d

    visited = set()
    while matrix[pos[0], pos[1]] != 'B':
        if dir == Direction.NORTH:
            # the smallest above
            x = pos[1]
            if x not in x_b:
                return False
            # yy = np.searchsorted(x_b[x], pos[0], side='left', sorter=None)
            y = 0
            for yy in x_b[x]:
                if yy < pos[0]:
                    y = yy + 1
                    break
            
        elif dir == Direction.SOUTH:
            # the smallest above
            x = pos[1]
            # yy = np.searchsorted(x_b[x], pos[0], side='left', sorter=None)
            y = matrix.shape[0] - 1
            
            if x not in x_b:
                return False

            for yy in reversed(x_b[x]):
                if yy > pos[0]:
                    y = yy - 1
                    break
        elif dir == Direction.EAST:
            y = pos[0]
            if y not in y_b:
                return False
            x = matrix.shape[1] - 1
            for xx in y_b[y]:
                if xx > pos[0]:
                    x = xx - 1
                    break
        elif dir == Direction.WEST:
            y = pos[0]
            if y not in y_b:
                return False
            x = 0
            for xx in reversed(y_b[y]):
                if xx < pos[0]:
                    x = xx + 1
                    break
        if (y, x, dir.name) in visited:
            return True

        pos = (y, x)
        if matrix[pos[0], pos[1]] == 'B':
            break

        visited.add((y, x, dir.name))
        
        dir = get_next_right_dir(direction=dir)
    return False

def get_number_of_void_points(start: Tuple[int, int], matrix: np.ndarray) -> int:
    # get all # somehow structured to find the next # given position in log(n) or such
    # print(matrix)
    
    # pos = Point2D(x=start[1], y=start[0])
    pos = (start[0], start[1])

    res = 0
    pts = {(i[0], i[1]) for i in get_walk(start=start, matrix=matrix)}
    for yy, xx in pts:
        if matrix[yy, xx] == '.':
            matrix[yy, xx] = '#'
            if check_if_infinite_loop(matrix=matrix, s_pos=pos, d=Direction.NORTH):
                res += 1
            matrix[yy, xx] = '.'
    return res

def find_start(start: str, matrix: np.ndarray):
    res = np.where(matrix == start)
    return int(res[0][0]), int(res[1][0])

@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val="B", offset=1)
        start = find_start(start='^', matrix=matrix_with_offset)
        return len({(i[0], i[1]) for i in get_walk(start=start, matrix=matrix_with_offset)})
    

@timer_decorator
def solve_2_naive(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val="B", offset=1)
        start = find_start(start='^', matrix=matrix_with_offset)
        return get_number_of_void_points_naive(start=start, matrix=matrix_with_offset)

@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val="B", offset=1)
        start = find_start(start='^', matrix=matrix_with_offset)
        return get_number_of_void_points(start=start, matrix=matrix_with_offset)


if __name__ == '__main__':
    assert solve_1(p=t_f) == 41
    assert solve_1(p=in_f) == 4454
    assert solve_2_naive(p=t_f) == 6
    assert solve_2_naive(p=in_f) == 1503
    # print(solve_2(p=in_f))
    print("All passed!")
