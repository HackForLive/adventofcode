from collections import deque
import functools
import itertools
from pathlib import Path
from typing import Dict, List, Set, Tuple

from aoc.model.direction import Direction, get_next_right_dir
from aoc.model.geometry import Point2D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'

import numpy as np

def get_start_point(c: str, array: np.matrix) -> Tuple[int, int]:
    rows, cols = np.where(array == c)
    assert len(rows) == 1
    assert len(cols) == 1
    return int(rows[0]), int(cols[0])

def get_gps_coordinates(s_p: Tuple[int, int], matrix: np.matrix, ins: List[Direction]
                        ) -> List[Tuple[int, int]]:
    curr_p = (s_p[0], s_p[1])
    for i in ins:
        prev_p = (curr_p[0], curr_p[1])
        curr_p = (curr_p[0] + i.value[0], curr_p[1] + i.value[1])
        map_c = matrix[curr_p[0], curr_p[1]]
        if map_c == '.':
            matrix[prev_p[0], prev_p[1]] = '.'
            matrix[curr_p[0], curr_p[1]] = '@'
        elif map_c == '#':
            curr_p = (prev_p[0] , prev_p[1])
        elif map_c == 'O':
            tmp = (curr_p[0], curr_p[1])
            tmp_l = []
            while matrix[tmp[0], tmp[1]] == 'O':
                tmp_l.append((tmp[0], tmp[1]))
                tmp = (tmp[0] + i.value[0], tmp[1] + i.value[1])
            if matrix[tmp[0], tmp[1]] == '.':
                matrix[prev_p[0], prev_p[1]] = '.'
                matrix[curr_p[0], curr_p[1]] = '@'
                for t in tmp_l:
                    matrix[t[0] + i.value[0], t[1] + i.value[1]] = 'O'
            else:
                curr_p = (prev_p[0] , prev_p[1])
    
    return [(int(i[0]), int(i[1])) for i in zip(*np.where(matrix == 'O'))]

def sum_gps_coordinates(boxes: List[Tuple[int, int]]) -> int:
    return functools.reduce(
            lambda a, b: a + b, [b[0]*100 + b[1] for b in boxes], 0)

def get_direction_from_c(c: str) -> Direction:
    return {
        '^': Direction.NORTH,
        'v': Direction.SOUTH,
        '>': Direction.EAST,
        '<': Direction.WEST
    }[c]

def is_horizontal_move_applied(s_p: Tuple[int, int], d: Direction, matrix: np.matrix) -> bool:
    tmp = (s_p[0], s_p[1])
    tmp_l = []
    while matrix[tmp[0], tmp[1]] == '[' or matrix[tmp[0], tmp[1]] == ']':
        tmp_l.append((tmp[0], tmp[1]))
        tmp = (tmp[0] + d.value[0], tmp[1] + d.value[1])
    if matrix[tmp[0], tmp[1]] == '.':
        for t in reversed(tmp_l):
            matrix[t[0] + d.value[0], t[1] + d.value[1]] = matrix[t[0], t[1]]
        return True
    return False

def is_vertical_move_applied(
    open_b: Tuple[int, int], close_b: Tuple[int, int], d: Direction, matrix: np.matrix) -> bool:

    # print(f"{open_b =}")
    # print(f"{close_b =}")
    q = deque()
    q.append(open_b)
    q.append(close_b)

    q_f = deque()
    visited = set()
    while q:
        curr = q.popleft()
        if curr in visited:
            continue
        next_c = (curr[0] + d.value[0], curr[1] + d.value[1])
        m_c = matrix[next_c[0], next_c[1]]

        
        if m_c == '#':
            return False
        elif m_c == '[':
            q.append(next_c)
            q.append((next_c[0], next_c[1]+1))
        elif m_c == ']':
            q.append(next_c)
            q.append((next_c[0], next_c[1]-1))
        
        q_f.append(curr)
        visited.add(curr)


    empty_b = []
    occupied_b = []
    while q_f:
        c = q_f.popleft()
        # print(f"{c =}")
        empty_b.append((c[0], c[1], '.'))
        occupied_b.append((c[0] + d.value[0], c[1] + d.value[1], matrix[c[0], c[1]]))
    
    for r in empty_b:
        matrix[r[0], r[1]] = r[2]
    for r in occupied_b:
        matrix[r[0], r[1]] = r[2]
    
    # print(matrix)
    # exit(0)
    # matrix[open_b[0], open_b[1]] = '.'
    # matrix[close_b[0], close_b[1]] = '.'
    return True


def get_gps_coordinates_2(s_p: Tuple[int, int], matrix: np.matrix, ins: List[Direction]
                        ) -> List[Tuple[int, int]]:
    # for instructions
    # print(matrix)
    curr_p = (s_p[0], s_p[1])
    for i in ins:
        # print(i)
        # print(matrix)
        prev_p = (curr_p[0], curr_p[1])
        curr_p = (curr_p[0] + i.value[0], curr_p[1] + i.value[1])
        map_c = matrix[curr_p[0], curr_p[1]]
        if map_c == '.':
            # the same as in first part
            matrix[prev_p[0], prev_p[1]] = '.'
            matrix[curr_p[0], curr_p[1]] = '@'
        elif map_c == '#':
            # the same as in first part
            curr_p = (prev_p[0] , prev_p[1])
        elif map_c == '[':
            if i == Direction.WEST:
                raise ValueError('Not defined behaviour')
            elif i == Direction.EAST:
                if is_horizontal_move_applied(s_p=curr_p, d=i, matrix=matrix):
                    matrix[prev_p[0], prev_p[1]] = '.'
                    matrix[curr_p[0], curr_p[1]] = '@'
                else:
                    curr_p = (prev_p[0] , prev_p[1])
            elif i == Direction.NORTH or i == Direction.SOUTH:
                if is_vertical_move_applied(open_b=curr_p, close_b=(curr_p[0], curr_p[1]+1), d=i, 
                                            matrix=matrix):
                    matrix[prev_p[0], prev_p[1]] = '.'
                    matrix[curr_p[0], curr_p[1]] = '@'
                else:
                    curr_p = (prev_p[0] , prev_p[1])
        elif map_c == ']':
            if i == Direction.EAST:
                raise ValueError('Not defined behaviour')
            elif i == Direction.WEST:
                if is_horizontal_move_applied(s_p=curr_p, d=i, matrix=matrix):
                    matrix[prev_p[0], prev_p[1]] = '.'
                    matrix[curr_p[0], curr_p[1]] = '@'
                else:
                    curr_p = (prev_p[0] , prev_p[1])
            elif i == Direction.NORTH or i == Direction.SOUTH:
                if is_vertical_move_applied(open_b=(curr_p[0], curr_p[1]-1), close_b=curr_p, d=i, 
                                            matrix=matrix):
                    matrix[prev_p[0], prev_p[1]] = '.'
                    matrix[curr_p[0], curr_p[1]] = '@'
                else:
                    curr_p = (prev_p[0] , prev_p[1])
        # print(matrix)
    
    return [(int(i[0]), int(i[1])) for i in zip(*np.where(matrix == '['))]

@timer_decorator
def solve_1(p: Path) -> int:
    w_map = []
    instrs = []
    instr = False
    start = '@'
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            l = line.strip()
            if l:
                if not instr:
                    w_map.append([c for c in l])
                else:
                    for c in l:
                        instrs.append(get_direction_from_c(c=c))
            else:
                instr = True

        matrix = np.asmatrix(w_map)
        s_p = get_start_point(c=start, array=matrix)
        boxes = get_gps_coordinates(s_p=s_p, matrix=matrix, ins=instrs)
        return sum_gps_coordinates(boxes=boxes)


def get_doubled_tile(tile: str):
    return {
        '#': '##',
        'O': '[]',
        '.': '..',
        '@': '@.'
    }[tile]

@timer_decorator
def solve_2(p: Path) -> int:
    w_map = []
    instrs = []
    instr = False
    start = '@'
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            l = line.strip()
            if l:
                if not instr:
                    w_map.append(list(itertools.chain(*[get_doubled_tile(c) for c in l])))
                else:
                    for c in l:
                        instrs.append(get_direction_from_c(c=c))
            else:
                instr = True

        matrix = np.asmatrix(w_map)
        s_p = get_start_point(c=start, array=matrix)
        boxes = get_gps_coordinates_2(s_p=s_p, matrix=matrix, ins=instrs)
        return sum_gps_coordinates(boxes=boxes)
    


if __name__ == '__main__':
    assert solve_1(p=t2_f) == 2028
    assert solve_1(p=t_f) == 10092
    assert solve_1(p=in_f) == 1456590
    assert solve_2(p=t_f) == 9021
    print(solve_2(p=in_f))
    print("All passed!")
