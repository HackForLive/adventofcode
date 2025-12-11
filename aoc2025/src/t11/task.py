from collections import deque
import dataclasses
from pathlib import Path
import sys

import numpy as np

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test_2.txt'
in_f = curr_dir / 'in.txt'

def count_paths_simple(start: str, end: str, out_dic: dict[str, list[str]]):
    # print(out_dic)
    queue = deque()
    queue.append(start)

    res = 0
    while queue:
        curr = queue.pop()

        if curr == end:
            res += 1
            continue

        for i in out_dic.get(curr, []):
            queue.append(i)
    return res

def reachability(start: str, end: str, out_dic: dict[str, list[str]]) -> bool:
    # print(out_dic)
    queue = deque()
    queue.append(start)

    visited = set()

    while queue:
        curr = queue.popleft()

        if curr == end:
            return True
        
        if curr in visited:
            continue
        visited.add(curr)
        
        for i in out_dic.get(curr, []):
            queue.append(i)
    return False

@timer_decorator
def solve_1(p: Path):
    
    out_dic = {}
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            le, ri = l.strip().split(':')
            out_dic[le.strip()]=[i.strip() for i in ri.split(' ') if i.strip()]

    start = 'you'
    end = 'out'
    return count_paths_simple(start=start, end=end, out_dic=out_dic)


def count_paths_with_cycle_handle(graph, start, target):
    memo = {}
    visiting = set()

    def dfs(u):
        if u == target:
            return 1
        if u in memo:
            return memo[u]
        if u in visiting:
            raise Exception("Cycle → infinite paths")

        visiting.add(u)
        total = 0
        for v in graph.get(u, []):
            total += dfs(v)
        visiting.remove(u)

        memo[u] = total
        return total

    return dfs(start)


def count_paths_no_cycle(graph, start, target):
    memo = {}

    def dfs(u):
        if u == target:
            return 1
        if u in memo:
            return memo[u]

        memo[u] = sum(dfs(v) for v in graph.get(u, []))
        return memo[u]

    return dfs(start)


@timer_decorator
def solve_2(p: Path):
    out_dic = {}
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            le, ri = l.strip().split(':')
            out_dic[le.strip()]=[i.strip() for i in ri.split(' ') if i.strip()]

    start = 'svr'
    end = 'out'


    # false
    if reachability(start='dac', end='fft', out_dic=out_dic):
        sec = 'dac'
        th = 'fft'
    if reachability(start='fft', end='dac', out_dic=out_dic):
        sec = 'fft'
        th = 'dac'
    
    res = count_paths_no_cycle(graph=out_dic, start=start, target=sec)
    res *= count_paths_no_cycle(start=sec, target=th, graph=out_dic)
    res *= count_paths_no_cycle(start=th, target=end, graph=out_dic)
    return res

if __name__ == '__main__':
    assert solve_1(p=t_f) == 5
    print(solve_1(p=in_f)) # 607

    assert solve_2(p=t2_f) == 2
    print(solve_2(p=in_f)) # 506264456238938
    print("All passed!")
