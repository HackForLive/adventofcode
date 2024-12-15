from collections import deque
import functools
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

def bfs(s_pos: Tuple[int, int], matrix: np.ndarray, visited: Set[Tuple[int, int]]) -> int:
    stack = deque()
    stack.append(s_pos)

    region_char = matrix[s_pos[0], s_pos[1]]
    area = 0
    fence = 0

    while stack:
        curr = stack.popleft()
        val = matrix[curr[0], curr[1]]
        if val != region_char:
            continue
        if (curr[0], curr[1]) in visited:
            continue

        for p in (Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST):
            y = curr[0] + p.value[0]
            x = curr[1] + p.value[1]
            if matrix[y, x] == region_char:
                stack.append((y, x))
            else:
                fence += 1
        visited.add(curr)
        area += 1
    # print(f"{region_char =}")
    # print(f"{area =}")
    # print(f"{fence =}")
    return area * fence

def get_start_point(c: str, array: np.matrix) -> Tuple[int, int]:
    rows, cols = np.where(array == c)
    assert len(rows) == 1
    assert len(cols) == 1
    return int(rows[0]), int(cols[0])

def get_gps_coordinates(s_p: Tuple[int, int], matrix: np.matrix, ins: List[Direction]
                        ) -> List[Tuple[int, int]]:
    # for instructions
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

if __name__ == '__main__':
    assert solve_1(p=t2_f) == 2028
    assert solve_1(p=t_f) == 10092
    assert solve_1(p=in_f) == 1456590
    print("All passed!")
