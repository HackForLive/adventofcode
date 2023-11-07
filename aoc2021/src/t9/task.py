import time
import os
import functools
import pathlib
from typing import Tuple

from collections import deque
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


def get_spot_value(matrix: np.matrix, iy: int, ix: int) -> int:
    is_spot = (
        matrix[iy-1, ix] > matrix[iy, ix] and
        matrix[iy+1, ix] > matrix[iy, ix] and
        matrix[iy, ix-1] > matrix[iy, ix] and
        matrix[iy, ix+1] > matrix[iy, ix]
    )
    return matrix[iy, ix] + 1 if is_spot else 0


def get_hole_value(matrix: np.matrix, iy: int, ix: int) -> int:
    if not get_spot_value(matrix=matrix, iy=iy, ix=ix):
        return 0
    visited: set[Tuple[int, int]] = set()
    queue = deque()
    queue.append((iy, ix))

    while len(queue) > 0:
        curr = queue.popleft()
        if curr not in visited:
            y = curr[0]
            x = curr[1]
            if matrix[y, x] > 8:
                continue
            visited.add(curr)
            for step in range(-1, 3, 2):
                if matrix[y+step, x] > matrix[y, x]:
                    queue.append((y+step, x))
                if matrix[y, x+step] > matrix[y, x]:
                    queue.append((y, x+step))
    return len(visited)


def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=int)
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
        res = sum((get_spot_value(matrix_with_offset, iy=iy+offset, ix=ix+offset) for iy, ix in
                   np.ndindex(matrix.shape)))
        print(res)


def solve_2():
    offset = 1
    val = 15
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=val, offset=offset)
        res = sorted((get_hole_value(matrix_with_offset, iy=iy+offset, ix=ix+offset) for iy, ix in
                   np.ndindex(matrix.shape)), reverse=True)
        # print(res)
        print(res[0] * res[1] * res[2])


if __name__ == '__main__':
    solve_1()
    # solve_2()
    lp = LineProfiler()
    lp.add_function(get_hole_value)
    lp_wrapper = lp(solve_2)
    lp_wrapper()
    lp.print_stats()
