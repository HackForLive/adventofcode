from pathlib import Path
from typing import Dict, List, Tuple

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def get_sum_of_corrected_updates(ord_rules: Dict[int, List[int]], updates: List[List[int]]):
    res = 0
    for l in updates:
        is_corr = False
        for i in range(len(l)):
            for j in range(i+1, len(l)):
                if l[j] in ord_rules and l[i] in ord_rules[l[j]]:
                    #swap
                    is_corr = True
                    tmp = l[j]
                    l[j] = l[i]
                    l[i] = tmp 
        if is_corr:
            res += l[len(l)//2]
    return res


def get_sum_of_correct_updates(ord_rules: Dict[int, List[int]], updates: List[List[int]]):
    res = 0
    for l in updates:
        visited = set()
        is_corr = True
        for u in l:
            if not u in visited:
                if u in ord_rules:
                    for k in ord_rules[u]:
                        if k in visited:
                            is_corr = False
                            break
                visited.add(u)
        if is_corr:
            res += l[len(l)//2]
    return res


def parse(p: Path) -> Tuple[Dict[int, List[int]], List[List[int]]]:
    ord_rules = {}
    updates = []
    switch_updates = False
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            l = line.strip()
            if not l:
                switch_updates = True
                continue
            if not switch_updates:
                left, right = [int(i) for i in l.split('|')]
                if left in ord_rules:
                    ord_rules[left].append(right)
                else:
                    ord_rules[left] = [right]
            else:
                updates.append([int(i) for i in l.split(',')])
    return ord_rules, updates

@timer_decorator
def solve_1(p: Path):
    ord_rules, updates = parse(p=p)
    return get_sum_of_correct_updates(ord_rules=ord_rules, updates=updates)


@timer_decorator
def solve_2(p: Path):
    ord_rules, updates = parse(p=p)
    return get_sum_of_corrected_updates(ord_rules=ord_rules, updates=updates)


if __name__ == '__main__':
    assert solve_1(p=t_f) == 143
    # assert solve_1(p=in_f) == 4689
    assert solve_2(p=t_f) == 123
    # assert solve_2(p=in_f) == 6336    
    print("All passed!")
