from __future__ import annotations
import os
import pathlib
from typing import List, Tuple
import itertools
import copy

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input_test.txt')

def parse() -> Tuple[List[str], List[int]]:
    with open(input_file, 'r', encoding='utf8') as f:
        nums = []
        records = []
        for line in f:
            l, r = line.strip().split(' ')

            records.append(list(l))
            nums.append([int(n) for n in r.strip().split(',')])
        return records, nums

def get_q_mark_positions(records: List[str]) -> List[str]:
    return [idx for idx, i in enumerate(records) if i == '?']


def is_valid_arrangement(record: List[str], q_pos: List[str], q_val: List[int],
                         control_s: List[int]) -> bool:
    record = copy.deepcopy(record)

    for i, pos in enumerate(q_pos):
        record[pos] = '#' if q_val[i] else '.'

    # print(record)
    actual = []
    last = record[0]
    is_seq = last == '#'
    count = 1 if is_seq else 0
    for i in record:
        if i == '#':
            if is_seq:
                count += 1
            else:
                count = 1
            is_seq = True
        else:
            if is_seq:
                actual.append(count)
            is_seq = False

    # print(control_s)
    # print(actual)
    return control_s == actual
            
def get_valid_arrangements(record: List[str], q_pos: List[str], control_s: List[int]) -> int:
    obj_iter = itertools.product([0,1], repeat=len(q_pos))
    res = 0
    for j in obj_iter:
        if is_valid_arrangement(record=record, q_pos=q_pos, q_val=list(j), control_s=control_s):
            res = res + 1

    return res

def solve_1():
    records, nums = parse()
    res = 0
    for i, record in enumerate(records):
        q_pos = get_q_mark_positions(records=record)
        res += get_valid_arrangements(record=record, q_pos=q_pos, control_s=nums[i])
    print(res)
        # nums[i]
        # print(len(q_pos))
        # a = max(a, len(q_pos))
        # print()
    # print(a)
    #

if __name__ == '__main__':
    solve_1()
