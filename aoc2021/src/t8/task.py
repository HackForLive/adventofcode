import time
import os
import functools
import pathlib

from line_profiler import LineProfiler
import numpy as np


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def timer_decorator(func):
    functools.wraps(func)
    def with_timer(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        elapsed = t1 - t0

        print(f"@timer: {func.__name__} took {elapsed:0.4f} seconds")
        return result
    return with_timer


def get_spot_value_with_conditionals(matrix: np.matrix, iy: int, ix: int):
    """
    not very effective
    """
    is_spot = True
    # top check
    if iy > 0:
        is_spot &= matrix[iy-1, ix] > matrix[iy, ix]
    # bottom check
    if iy + 1 < matrix.shape[0]:
        is_spot &= matrix[iy+1, ix] > matrix[iy, ix]
    # left check
    if ix > 0:
        is_spot &= matrix[iy, ix-1] > matrix[iy, ix]
    # right check
    if ix + 1 < matrix.shape[1]:
        is_spot &= matrix[iy, ix+1] > matrix[iy, ix]
    if is_spot:
        return matrix[iy, ix] + 1
    else:
        return 0


def get_spot_value(matrix: np.matrix, iy: int, ix: int):
    is_spot = (
        matrix[iy-1, ix] > matrix[iy, ix] and
        matrix[iy+1, ix] > matrix[iy, ix] and
        matrix[iy, ix-1] > matrix[iy, ix] and
        matrix[iy, ix+1] > matrix[iy, ix]
    )
    return matrix[iy, ix] + 1 if is_spot else 0


def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, dtype=int)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

# @timer_decorator
def solve_1():
    offset = 1
    val = 9
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=val, offset=offset)
        res = sum([get_spot_value(matrix_with_offset, iy=iy+offset, ix=ix+offset) for iy, ix in np.ndindex(matrix.shape)])
        print(res)


if __name__ == '__main__':
    # solve_1()
    lp = LineProfiler()
    lp_wrapper = lp(solve_1)
    lp_wrapper()
    lp.print_stats()
