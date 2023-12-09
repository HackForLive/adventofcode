from __future__ import annotations
import os
import pathlib
from typing import List

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        res: List[List[int]] = []
        for line in f:
            clean_l = line.strip()
            res.append([int(p) for p in clean_l.split(' ')])
        return res

def next_number(seq: List[int]):
    # print(seq)
    res: int = 0
    n = len(seq) - 1
    should_run = True
    while should_run:
        last = seq[n]
        for i in range(n, -1, -1):
            if i == 0:
                break
            tmp = last - seq[i-1]
            last = seq[i-1]
            seq[i-1] = tmp
            if tmp == 0 and i == n:
                should_run = False
                break
        # print(f"{seq =}")
        if not should_run:
            break
        n = n - 1

    # print(f"{n =}")
    for i in range(n, len(seq)):
        res += seq[i]
    return res


def solve_1():
    print(sum((next_number(num) for num in parse())))


if __name__ == '__main__':
    solve_1()
