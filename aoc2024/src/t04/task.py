import itertools
from pathlib import Path
import functools
import re
from typing import Any, Generator, Iterator, List, Tuple

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np


def get_matrix_with_offset(matrix: np.matrix, val: str, offset: int)  -> np.ndarray:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=str)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix


def get_directions() -> List[Any]:
    return [i for i in itertools.product([-1,0,1], [-1,0,1]) if i != (0,0)]
    


def get_number_of_pattern(pattern: str, matrix: np.ndarray, x: int, y: int) -> int:
    # try up
    res = 0
    for dir in get_directions():
        matching = True
        for i, m in enumerate(pattern):
            p = (y + i*dir[0], x + i*dir[1])
            if matrix[p[0], p[1]] != m:
                matching = False
                break
        if matching:
            res += 1
                    
    return res


def traverse_matrix(pattern: str, matrix: np.ndarray) -> int:
    res = 0
    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == pattern[0]:
            res += get_number_of_pattern(pattern=pattern, matrix=matrix, x=x, y=y)

    return res

@timer_decorator
def solve_1(p: Path):
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val="BB", offset=1)
        return traverse_matrix(pattern='XMAS', matrix=matrix_with_offset)


def get_number_of_x_pattern(x_pattern: str, matrix: np.ndarray, x: int, y: int) -> int:
    dd = {}
    for i in ((1, -1), (-1, 1)):
        ii = (y + i[0], x + i[1])
        dd[matrix[ii]] = dd.get(matrix[ii], 0) + 1

    if not (dd.get(x_pattern[0], -1) == dd.get(x_pattern[1], -2) and len(dd) == 2):
        return 0

    dd = {}
    for i in ((-1,-1), (1, 1)):

        ii = (y + i[0], x + i[1])
        dd[matrix[ii]] = dd.get(matrix[ii], 0) + 1

    if not (dd.get(x_pattern[0], -1) == dd.get(x_pattern[1], -2) and len(dd) == 2):
        return 0
    return 1


def traverse_matrix_for_x_pattern(middle: str, x_pattern: str, matrix: np.ndarray) -> int:
    res = 0
    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == middle:
            res += get_number_of_x_pattern(x_pattern=x_pattern, matrix=matrix, x=x, y=y)
    return res


@timer_decorator
def solve_2(p: Path):
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val="BB", offset=1)
        return traverse_matrix_for_x_pattern(middle='A', x_pattern='MS', matrix=matrix_with_offset)


if __name__ == '__main__':
    test_o = solve_1(p=t_f)

    if test_o != 18:
        raise ValueError('Test failed!')
    
    f_o = solve_1(p=in_f)
    if f_o != 2378:
        raise ValueError('The first task failed!')
    
    test_o = solve_2(p=t_f)
    if test_o != 9:
        raise ValueError('Test failed!')
    
    s_o = solve_2(p=in_f)
    if s_o != 1796:
        raise ValueError('Test failed!')

    print("All passed!")
