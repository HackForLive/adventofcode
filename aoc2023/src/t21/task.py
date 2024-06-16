
from dataclasses import dataclass, field
from enum import Enum
import os
from typing import List, Tuple
from collections import deque

import numpy as np


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

def parse(input_file: str):
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([list(line.strip()) for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return get_matrix_with_offset(matrix=matrix, val=ItemTypeEnum.BORDER.value, offset=1)

def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val,
                             dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return np.asmatrix(offset_matrix)

def get_start_point(matrix: np.matrix, start: str = ItemTypeEnum.START.value) -> Tuple[int, int]:
    rows, cols = np.where(matrix == start)
    assert len(rows) == 1
    assert len(cols) == 1
    return rows[0], cols[0]

def get_eligible_points(p: QueuedItem, matrix: np.matrix) -> List[QueuedItem]:
    res = []
    for y in [-1, 1]:
        if ((matrix[p.y + y, p.x] == ItemTypeEnum.PLOT.value) |
            (matrix[p.y + y, p.x] == ItemTypeEnum.START.value)):
            res.append(QueuedItem(y=p.y + y, x=p.x, time_step=p.time_step + 1))
    for x in [-1, 1]:
        if ((matrix[p.y, p.x + x] == ItemTypeEnum.PLOT.value) |
            (matrix[p.y, p.x + x] == ItemTypeEnum.START.value)):
            res.append(QueuedItem(y=p.y, x=p.x + x, time_step=p.time_step + 1))
    return res


def get_number_of_plot_visited(start: Tuple[int, int], steps: int, matrix: np.matrix) -> int:
    q = deque()
    s = QueuedItem(x=start[1], y=start[0], time_step=0)
    accessed = set()
    q.append(s)
    # accessed.add(s)
    res = set()
    while q:
        curr = q.popleft()
        if curr in accessed:
            continue

        accessed.add(curr)

        if curr.time_step == steps:
            res.add(curr)
            continue
       
        nodes = get_eligible_points(p=curr, matrix=matrix)
        for n in nodes:
            q.append(n)
        # q = deque(sorted(set(q)))
        # print(q)
        # q = deque(set(q))
        # print(q)
    # print(q)
    # print(set([o for o in q if o.time_step  == steps]))
    print(res)
    return len(res)


def solve_1(in_f: str):
    matrix = parse(input_file=in_f)
    print(matrix)
    r, c = get_start_point(matrix=matrix)
    print(r, c)
    return get_number_of_plot_visited(start=(r, c), steps=64, matrix=matrix)

if __name__ == '__main__':
    infile = os.path.join(curr_dir, 'input.txt')
    res = solve_1(in_f=infile)
    print(res)
    # answer is too low 3819
