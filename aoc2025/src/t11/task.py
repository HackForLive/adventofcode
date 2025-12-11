from collections import deque
from pathlib import Path
import sys

import numpy as np

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def all_paths(start: str, end: str, out_dic: dict[str, list[str]]):
    # print(out_dic)
    queue = deque()
    queue.append(start)

    res = 0
    while queue:
        curr = queue.pop()

        if curr == end:
            res += 1
            continue

        for i in out_dic[curr]:
            queue.append(i)
    return res

@timer_decorator
def solve_1(p: Path):
    
    out_dic = {}
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            le, ri = l.strip().split(':')
            out_dic[le.strip()]=[i.strip() for i in ri.split(' ') if i.strip()]

    start = 'you'
    end = 'out'
    return all_paths(start=start, end=end, out_dic=out_dic)

@timer_decorator
def solve_2(p: Path):
    out_dic = {}
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            le, ri = l.strip().split(':')
            out_dic[le.strip()]=[i.strip() for i in ri.split(' ') if i.strip()]

    start = 'you'
    end = 'out'
    return all_paths(start=start, end=end, out_dic=out_dic)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 5
    print(solve_1(p=in_f)) # 607

    assert solve_2(p=t_f) == 2
    # print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
