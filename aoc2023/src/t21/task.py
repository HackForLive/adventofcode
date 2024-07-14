
from dataclasses import dataclass, field
from enum import Enum
import os
from typing import List, Tuple
from collections import deque

import numpy as np
import pandas as pd # pylint: disable=unused-import


@dataclass(frozen=True, eq=True, kw_only=True)
class QueuedItem:
    """
    Queued item
    """
    x: int = field(default=-1)
    y: int = field(default=-1)
    time_step: int = field(default=0)

    def __eq__(self, other):
        return isinstance(other, QueuedItem) and (self.x == other.x and
                                                  self.y == other.y and
                                                  self.time_step == other.time_step)

    def __lt__(self, other):
        return self.time_step < other.time_step


class ItemTypeEnum(Enum):
    """
    Item type on the map
    """
    BORDER = '@'
    PLOT = '.'
    ROCK = '#'
    START = 'S'

curr_dir = os.path.dirname(os.path.realpath(__file__))

def parse(input_file: str, extend: int = 0) -> Tuple[int, np.matrix]:
    if extend < 0:
        raise ValueError(f"Value must be greater than 0, got {extend}.")

    total_side_len = 1 + extend*2
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([list(line.strip()) for line in f.readlines()])
        # remove start point
        row, col = remove_start_point(array=arr_2d)

        matrix = np.asmatrix(np.tile(arr_2d, (total_side_len, total_side_len)))

        # readd start point
        add_start_point(matrix=matrix, row=row + extend*len(arr_2d), col=col + extend*len(arr_2d))

        return (len(arr_2d), 
                get_matrix_with_offset(matrix=matrix, val=ItemTypeEnum.BORDER.value, offset=1))

def get_start_point(array: np.ndarray | np.matrix) -> Tuple[int, int]:
    rows, cols = np.where(array == ItemTypeEnum.START.value)
    assert len(rows) == 1
    assert len(cols) == 1
    return rows[0], cols[0]

def remove_start_point(array: np.ndarray | np.matrix) -> Tuple[int, int]:
    row, col = get_start_point(array=array)
    array[row,col]=ItemTypeEnum.PLOT.value
    return row, col

def add_start_point(matrix: np.matrix, row: int, col: int) -> None:
    matrix[row, col] = ItemTypeEnum.START.value

def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val,
                             dtype=np.dtype('U10'))
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return np.asmatrix(offset_matrix)

def get_eligible_points(p: QueuedItem, matrix: np.matrix) -> List[QueuedItem]:
    res = []
    for y in [-1, 1]:
        if matrix[p.y + y, p.x] == ItemTypeEnum.PLOT.value:
            res.append(QueuedItem(y=p.y + y, x=p.x, time_step=p.time_step + 1))
    for x in [-1, 1]:
        if matrix[p.y, p.x + x] == ItemTypeEnum.PLOT.value:
            res.append(QueuedItem(y=p.y, x=p.x + x, time_step=p.time_step + 1))
    return res


def get_visited_plot_count(start: Tuple[int, int], steps: int, matrix: np.matrix) -> int:
    q = deque()
    s = QueuedItem(x=start[1], y=start[0], time_step=0)
    accessed = set()
    res = 0
    # res = []
    q.append(s)
    while q:
        curr = q.popleft()
        if (curr.y, curr.x) in accessed:
            continue

        accessed.add((curr.y, curr.x))

        if curr.time_step % 2 == steps % 2:
            res += 1
            # res.append(curr)

        if curr.time_step == steps:
            continue

        nodes = get_eligible_points(p=curr, matrix=matrix)
        for node in nodes:
            q.append(node)
    # for r in res:
    #     matrix[r.y,r.x] = str(r.time_step)
    # return len(res)
    return res


def solve_1(in_f: str, steps: int):
    _, matrix = parse(input_file=in_f)
    # print(matrix)
    r, c = get_start_point(array=matrix)
    # print(r,c)
    return get_visited_plot_count(start=(r, c), steps=steps, matrix=matrix)


def solve_2(in_f: str, steps: int, extend: int):
    """
    @param extend: extended size in one direction; 
    example extend by 0: so the desk will remain 1x1, original
    example extend by 1: so the desk will 3x3
    example extend by 2: so the desk will 5x5
    """
    if extend < 0:
        raise ValueError(f"Value must be greater than 0, got {extend}.")

    m_len, matrix = parse(input_file=in_f, extend=extend)
    r, c = get_start_point(array=matrix)

    # prepare cycling sequences
    sts = [steps % m_len + m_len*i for i in range(5)]
    rr = []
    for st in sts:
        res = get_visited_plot_count(start=(r, c), steps=st, matrix=matrix)
        rr.append(res)

    f_diffs = list(map(lambda x : x[1] - rr[x[0] - 1] if x[0] > 0  else x[1], enumerate(rr)))[1:]
    s_diffs = list(map(lambda x : x[1] - f_diffs[x[0] - 1] if x[0] > 0  else x[1],
                       enumerate(f_diffs)))[1:]

    # n = steps // extend
    a_1 = f_diffs[0]
    a_n = lambda n: f_diffs[0]-s_diffs[0] + s_diffs[0]*n
    s_n = lambda n: n*(a_1 + a_n(n)) // 2

    # print(f'{rr = }')
    # print(f'{f_diffs = }')
    # print(f'{s_diffs = }')
    # print(a_1)
    # print(a_n)
    # print(s_n)
    return s_n(steps // m_len) + rr[0]
    # print(rr)
    # 1st and 2nd differences


def solve_using_oeis():
    steps = 26501365
    n = (steps // 131) + 1
    # https://oeis.org/
    # sequence
    # from 65 -> + 131
    # 
    # [3917, 34920, 96829, 189644, 313365, 467992]
    return 3820-15356*n + 15453*n*n


if __name__ == '__main__':
    test_infile = os.path.join(curr_dir, 'input.txt')
    infile = os.path.join(curr_dir, 'input.txt')
    n = 64
    res_1 = solve_1(in_f=infile, steps=n)
    if res_1 == 3820:
        print(f"Correct answer: {res_1}, steps: {n}")
    else:
        print(f'Wrong answer: {res_1}, steps: {n}')

    n = 26501365
    res_2 = solve_2(in_f=test_infile, steps=n, extend=6)

    # res_2 = solve_using_oeis()
    if res_2 == 632421652138917:
        # n = 1 => 65
        # n = 2 => 65 + (n-1)*131
        print(f"Correct answer: {res_2}, steps: {n}")
    else:
        print(f'Wrong answer: {res_2}, steps: {n}')
