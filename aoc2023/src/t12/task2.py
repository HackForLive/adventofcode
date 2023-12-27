import os
import pathlib
from typing import List

import numpy as np

records = []
numbs = []

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')

with open(input_file, mode='r', encoding='utf-8') as f:
    recs = [line.strip().split(' ') for line in f]
    records = [p[0] for p in recs]
    numbs = [[int(o) for o in p[1].split(',')] for p in recs]

memo = np.zeros(shape=(1000,1000))

def recurse(idx, idn, record, nums):
    if idn == len(nums):
        if idx <= len(record):
            for i in range(idx, len(record)):
                if record[i]=='#':
                    return 0
            return 1
        return 0

    if idx >= len(record):
        return 0

    take_n = 0
    dont_take = 0

    # take
    if idx + nums[idn] - 1 < len(record):
        is_valid = True
        for i in range(idx, idx + nums[idn]):
            if record[i] == '.':
                is_valid = False
                break
        if is_valid:
            if idn == len(nums) - 1:
                take_n = recurse(idx + nums[idn], idn + 1, record, nums)

            if idx + nums[idn] < len(record) and record[idx + nums[idn]] != '#':
                take_n = recurse(idx + nums[idn] + 1, idn + 1, record, nums)

    # do not take
    if idx < len(record) and record[idx] != '#':
        dont_take = recurse(idx+1, idn, record, nums)
    return take_n + dont_take

def solve_2():
    res = 0
    for idr, r in enumerate(records):
        print(r)
        print(numbs[idr])
        curr = recurse(0, 0, r,  numbs[idr])
        print(curr)
        res += curr
    print(res)

solve_2()
