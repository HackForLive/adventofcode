from pathlib import Path
from typing import Dict, List, Tuple
import copy

from aoc.model.direction import Direction, get_next_right_dir
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
    pos = (start[0], start[1])

    path = []
    while matrix[pos[0], pos[1]] != 'B':
        path.append((pos[0], pos[1], dir.name))

        y = pos[0] + dir.value[0]
        x = pos[1] + dir.value[1]
        if matrix[y, x] == '#':
            dir = get_next_right_dir(direction=dir)
        else:
            pos = (y, x)
    return path

def check_if_infinite_loop(
        y_b: Dict[int, List[int]],
        x_b: Dict[int, List[int]],
        s_pos: Tuple[int, int],
        d: Direction) -> bool:
    
    pos = (s_pos[0], s_pos[1])
    dir = d
    visited = set()
    while True:
        changed = False
        if dir == Direction.NORTH:
            if pos[1] not in x_b:
                return False
            for yy in reversed(x_b[pos[1]]):
                if yy < pos[0]:
                    pos = (yy + 1, pos[1])
                    changed = True
                    break
        elif dir == Direction.SOUTH:
            if pos[1] not in x_b:
                return False
            for yy in x_b[pos[1]]:
                if yy > pos[0]:
                    changed = True
                    pos = (yy - 1, pos[1])
                    break
        elif dir == Direction.EAST:
            if pos[0] not in y_b:
                return False
            for xx in y_b[pos[0]]:
                if xx > pos[1]:
                    changed = True
                    pos = (pos[0], xx - 1)
                    break
        elif dir == Direction.WEST:
            if pos[0] not in y_b:
                return False
            for xx in reversed(y_b[pos[0]]):
                if xx < pos[1]:
                    changed = True
                    pos = (pos[0], xx + 1)
                    break

        if not changed:
            return False
        if (pos[0], pos[1], dir.name) in visited:
            return True
        
        visited.add((pos[0], pos[1], dir.name))
        dir = get_next_right_dir(direction=dir)

def get_number_of_void_points(start: Tuple[int, int], matrix: np.ndarray) -> int:
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

    x_b = {k:sorted(x_b[k], key=lambda x: x, reverse=False) for k in x_b.keys()}
    y_b = {k:sorted(y_b[k], key=lambda x: x, reverse=False) for k in y_b.keys()}

    res = 0
    pts = {(i[0], i[1]) for i in get_walk(start=start, matrix=matrix)}
    for yy, xx in pts:
        if xx in x_b:
            xxx = copy.deepcopy(x_b[xx])
            x_b[xx] = sorted(x_b[xx] + [yy], key=lambda x: x, reverse=False)
        else:
            xxx = []
            x_b[xx] = [yy]

        if yy in y_b:
            yyy = copy.deepcopy(y_b[yy])
            y_b[yy] = sorted(y_b[yy] + [xx], key=lambda x: x, reverse=False)
        else:
            yyy = []
            y_b[yy] = [xx]

        if check_if_infinite_loop(x_b=x_b, y_b=y_b, s_pos=start, d=Direction.NORTH):
            res += 1
        
        x_b[xx] = xxx
        y_b[yy] = yyy
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
    assert solve_2(p=t_f) == 6
    assert solve_2(p=in_f) == 1503
    print("All passed!")
