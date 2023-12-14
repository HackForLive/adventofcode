from __future__ import annotations
import os
import pathlib

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

def parse():
    matrices = []
    with open(input_file, 'r', encoding='utf8') as f:
        arr = []
        for line in f:
            if line.strip() == '':
                arr_2d = np.array(arr)
                matrix = np.asmatrix(arr_2d)
                matrices.append(matrix)
                arr = []
            else:
                arr.append(list(line.strip()))

        if arr:
            arr_2d = np.array(arr)
            matrix = np.asmatrix(arr_2d)
            matrices.append(matrix)
        return matrices

def get_horizontal(m: np.matrix, ignore_row: int = -1):
    rows = m.shape[0]

    for row in range(1, rows):
        if ignore_row == row:
            continue
        if (m[row-1,:] == m[row,:]).all():
            step = 2
            is_ref = True
            while row-step >= 0 and row + step <= rows:
                if not (m[row-step,:] == m[row+step-1,:]).all():
                    is_ref = False
                    break
                step += 1

            if is_ref:
                return row
    return 0

def get_vertical(m: np.matrix, ignore_col: int = -1):
    cols = m.shape[1]

    for col in range(1, cols):
        if ignore_col == col:
            continue
        if (m[:, col-1] == m[:, col]).all():
            step = 2
            is_ref = True
            while col-step >= 0 and col + step <= cols:
                if not (m[:, col-step] == m[:, col+step-1]).all():
                    is_ref = False
                    break
                step += 1

            if is_ref:
                return col
    return 0

def get_reflection(m: np.matrix):
    h = get_horizontal(m=m)
    v = get_vertical(m=m)
    return h*100 + v

def get_reflection_with_correction(m: np.matrix):
    h = get_horizontal(m=m)
    v = get_vertical(m=m)
    prev=(h , v)

    for row in range(m.shape[0]):
        for col in range(m.shape[1]):
            tmp = m[row, col]
            if tmp == '.':
                m[row, col] = '#'
            elif tmp == '#':
                m[row, col] = '.'
            else:
                raise ValueError(f'unexpected char {tmp}')
            h = get_horizontal(m=m, ignore_row=prev[0])
            v = get_vertical(m=m, ignore_col=prev[1])
            m[row, col] = tmp
            if prev[0] != h and h > 0:
                return h*100
            if prev[1] != v and v > 0:
                return v
    return prev[0]*100 + prev[1]

def solve_1():
    matrices = parse()
    res = 0
    for m in matrices:
        tmp = get_reflection(m=m)
        res += tmp
    print(res)

def solve_2():
    matrices = parse()
    res = 0
    for m in matrices:
        tmp = get_reflection_with_correction(m=m)
        print(f"{tmp =}")
        res += tmp
    print(res)

if __name__ == '__main__':
    solve_1()
    solve_2()

    # too low
    # --> 5126, 6000
