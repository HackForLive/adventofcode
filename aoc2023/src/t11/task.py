from __future__ import annotations
import os
import pathlib
from typing import Tuple

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([list(line.strip()) for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix

def find_stars(star_token: str, matrix: np.matrix):
    res = np.where(matrix == star_token)
    return [(int(pos[0]), int(pos[1])) for pos in zip(res[0], res[1])]

def solve_1(expansion: int):
    matrix = parse()
    stars = find_stars(star_token='#', matrix=matrix)
    # print(matrix.shape)
    # print(matrix)
    # print(stars)

    x_s = [x[1] for x in stars]
    y_s = [y[0] for y in stars]
    a_x = []
    a_y = []
    for i in range(1, matrix.shape[0]):
        if i not in x_s:
            a_x.append(i)
        if i not in y_s:
            a_y.append(i)
    # print(a_x)
    # print(a_y)

    # rearrange
    star_rear = []
    for star in stars:
        y = star[0]
        x = star[1]
        for ys in a_y:
            if ys < star[0]:
                y = y + expansion
        for xs in a_x:
            if xs < star[1]:
                x = x + expansion
        star_rear.append((y,x))

    # print(star_rear)

    # compute dist
    res = []
    for a in range(0, len(star_rear), 1):
        for b in range(a, len(star_rear), 1):
            if a != b:
                res.append(dist(a=star_rear[a], b=star_rear[b]))

    print(sum(res))

def dist(a: Tuple[int,int], b: Tuple[int,int]) -> int:
    return int(abs(a[0]-b[0])) + int(abs(a[1]-b[1]))

if __name__ == '__main__':
    solve_1(expansion=1)
    solve_1(expansion=9)
    solve_1(expansion=99)
    solve_1(expansion=999999)
    # too high 363293870229