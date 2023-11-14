import os
import pathlib
from line_profiler import LineProfiler

import numpy as np


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=int)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix


def simulate_step(matrix: np.matrix, offset: int, shape):
    flashed = set()
    one_bump = set()
    # bump by 1
    while True:
        start_size = len(flashed)
        for y, x in np.ndindex(shape):
            iy = y + offset
            ix = x + offset
            if (iy, ix) not in one_bump and (iy, ix) not in flashed:
                matrix[iy, ix] = matrix[iy, ix] + 1
                one_bump.add((iy, ix))
            if matrix[iy, ix] > 9 and (iy, ix) not in flashed:
                matrix[iy, ix] = 0
                flashed.add((iy, ix))
                for i in range(-1,2,1):
                    for l in range(-1,2,1):
                        if (iy+i, ix+l) not in flashed:
                            matrix[iy+i, ix+l] = matrix[iy+i, ix+l] + 1
        if start_size == len(flashed):
            break
    return len(flashed)

def simulate_step_with_check(matrix: np.matrix, offset: int, shape):
    flash_n = simulate_step(matrix=matrix, offset=offset, shape=shape)
    return flash_n == shape[0]*shape[1]


def solve_2():
    n_step: int = 1000
    res: int = 0
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=-100, offset=1)
        while (not simulate_step_with_check(matrix_with_offset, offset=1, shape=matrix.shape) and
               res < n_step):
            res += 1
        print(res + 1)


def get_improved_result_2(matrix: np.matrix, shape):
    max_step = 300
    step = 0

    while step < max_step:
        # track flashed
        flashed = set()
        # bump
        matrix = matrix + 1
        while True:
            start_size = len(flashed)
            for y, x in np.argwhere(matrix > 9):
                if (y, x) not in flashed:
                    matrix[y, x] = 0
                    flashed.add((y, x))
                    for i in range(-1,2,1):
                        for l in range(-1,2,1):
                            if (y+i, x+l) not in flashed:
                                matrix[y+i, x+l] = matrix[y+i, x+l] + 1
            if start_size == len(flashed):
                break
        if np.count_nonzero(matrix == 0) == shape[0]*shape[1]:
            break
        step = step + 1

    return step



def solve_2_improved():
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=-1000, offset=1)
        res = get_improved_result_2(matrix_with_offset, shape=matrix.shape)
        print(res + 1)


def solve_1():
    n_step: int = 100
    res: int = 0
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=-100, offset=1)
        res = sum(simulate_step(matrix_with_offset, offset=1, shape=matrix.shape)
                   for step in range(n_step))
        print(res)


if __name__ == '__main__':
    # solve_2()
    lp = LineProfiler()
    # lp.add_function(simulate_step_with_check)
    lp.add_function(get_improved_result_2)
    lp_wrapper = lp(solve_2_improved)
    # lp_wrapper = lp(solve_2)
    lp_wrapper()
    lp.print_stats()
