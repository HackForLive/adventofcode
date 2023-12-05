import os
import pathlib

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


# @timer_decorator
def solve_1():
    res = 0
    with open(input_file, 'r', encoding='utf8') as f:
        for line in f:
            l = line.strip()
            parts = l.split(':')

if __name__ == '__main__':
    solve_1()
