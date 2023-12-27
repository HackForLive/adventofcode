from __future__ import annotations
import os
import pathlib
from typing import List, Tuple
import itertools
import copy
from copy import deepcopy

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
# input_file = os.path.join(curr_dir, 'test.txt')
input_file = os.path.join(curr_dir, 'input_test.txt')

def parse() -> Tuple[List[List[str]], List[List[int]]]:
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
    for idx, i in enumerate(record):
        if idx == 0:
            continue
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

    if is_seq and count > 0:
        actual.append(count)

    # print(control_s)
    # print(actual)
    return control_s == actual
            
def get_valid_arrangements(record: List[str], q_pos: List[str], control_s: List[int]) -> int:
    obj_iter = itertools.product([0,1], repeat=len(q_pos))
    res = 0
    for j in obj_iter:
        if is_valid_arrangement(record=record, q_pos=q_pos, q_val=list(j), control_s=control_s):
            res = res + 1
    # print(f"{res} {record}")
    # print(f"{control_s =}")
    # print(f"{q_pos =}")
    return res

def solve_1():
    records, nums = parse()
    res = 0
    for i, record in enumerate(records):
        q_pos = get_q_mark_positions(records=record)
        res += get_valid_arrangements(record=record, q_pos=q_pos, control_s=nums[i])
        print(i)
    print(res)
        # nums[i]
        # print(len(q_pos))
        # a = max(a, len(q_pos))
        # print()
    # print(a)
    #

def is_position_valid(record: str, start: int, length: int):
    # print(f"{start =}, {length = }")
    for i in range(start, start+length, 1):
        # print(i)
        # print(f"{i =}")
        if record[i] == '.':
            return False
    if start > 0 and record[start - 1] == '#':
        return False
    if start + length < len(record) - 1 and record[start + length] == '#':
        return False
    return True
    # in position all chars must be # or ? and on the edges .

def get_valid_positions(record: str, ranges: List[range], nums: List[int]) -> List[List[int]]:
    res = []
    for idx, n in enumerate(nums):
        r = ranges[idx]
        tmp = []
        # print(f"{r.start =}, {r.stop+1 =}")
        for j in range(r.start, r.stop+1, 1):
            if r.stop +1 - j < nums[idx]:
                break
            # print(f"{j =}")
            if is_position_valid(record=record, start=j, length=nums[idx]):
                tmp.append((j, j + nums[idx]-1))
        res.append(tmp)
    return res

def get_valid_ranges(record: List[str], nums: List[int]) -> List[range]:
    res = []
    start_n = []
    end_n = []

    prefix: int = 0
    suffix: int = len(record) - 1
    for i in range(0, len(nums), 1):
        # print(f"{prefix =}, {suffix =}")
        start_n.append(prefix)
        end_n.append(suffix)
        prefix += nums[i] + 1
        suffix -= nums[len(nums) - 1 - i] + 1
    end_n = list(reversed(end_n))

    for i in range(0, len(nums), 1):
        res.append(range(start_n[i], end_n[i]))
    return res

def validate_final_form(record: List[str], form: List[Tuple[int, int]]):
    # print(record)
    for i in range(form[0][0]):
        if record[i] == '#':
            return False

    for j, f in enumerate(form):
        if j > 0:
            for k in range(form[j-1][1]+1, form[j][0]):
                if record[k] == '#':
                    return False
                
    for i in range(form[-1][1]+1, len(record)):
        if record[i] == '#':
            # print(f"{i =}, {form =} {form[-1][1] =} {len(record) =}")
            return False
    return True



def check_how_many_var(record: List[str], nums: List[int]):
    res = 0
    # smart way - not ranges arrays as some values may not be valid (use only valid ones)
    ranges = get_valid_ranges(record=record, nums=nums)
    # print(ranges)

    valid_pos = get_valid_positions(record=record, ranges=ranges, nums=nums)
    # print(valid_pos)
    # exit(0)
    # print(list(itertools.product(*ranges)))
    print(record)
    for l in itertools.product(*valid_pos):
        # print(l)
        # print('-------')
        is_valid = True
        for idx, i in enumerate(l):
            if idx > 0 and l[idx][0] - 1 <= l[idx - 1][1]:
                is_valid = False
        if is_valid and validate_final_form(record=record, form=l):
            # print(l)
            res += 1

    # exit(0)
    print(res)
    if record == ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?']:
        # exit(0)
        pass
    print('-------')
    return res

def solve_2():
    records, nums = parse()

    # records = [record + ['?'] + record
    #            for record in records]
    # nums = [n + n for n in nums]
    # print(records)
    # print(nums)
    # exit(0)
    res = 0
    for i, record in enumerate(records):
        res += check_how_many_var(record=record, nums=nums[i])
        break
        # print(res)
    print(res)


def get_posibilities(record: List[str], start: int, stop: int, num: int):
    res = 0
    if stop - start + 1 < num:
        return res
    for k in range(start, stop+1, num):
        pos = True
        for j in range(start, stop+1, 1):
            if j < k:
                if record[j] == '#':
                    pos = False
                    break
            elif k <= j <= k + num:
                if record[j] == '.':
                    pos = False
                    break
            else:
                if record[j] == '#':
                    pos = False
                    break
        if pos:
            res += 1
    return res


def get_posible_arrangements(record: List[str], nums: List[int]):
    """
    take s1,s2 index check only one part is present and return number of possible positions
    iterate this for each part
    . between each part

    take all posibilities from memo
    """
    n = len(record)

    memo = np.zeros(shape=(n,n))

    start_idx = 0
    for num in nums:
        # tmp = deepcopy(memo)
        for i in range(n):
            if i < start_idx:
                memo[i,j] = 0
            for j in range(i, n):
                if start_idx == 0:
                    memo[i,j] = get_posibilities(record=record, start=i, stop=j, num=num)
                else:
                    if record[j-1] != '#':
                        memo[i,j] = memo[0,j-2]*get_posibilities(record=record, start=i, stop=j, num=num)
                    else:
                        memo[i,j] = 0
                    print('hah')
                print(memo)
        exit(0)
        start_idx = num + 1

        # break
    # print(memo)
    return 0


def solve_2_improved():
    records, nums = parse()

    res = 0
    for idr, record in enumerate(records):
        res += get_posible_arrangements(record=record, nums=nums[idr])
        break
    print(res)



if __name__ == '__main__':
    # solve_1()
    solve_2()
    solve_2_improved()
