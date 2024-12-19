from __future__ import annotations
import functools
from pathlib import Path
from typing import List, Tuple

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def parse(p: Path) -> Tuple[List[str], List[str]]:
    patterns = []
    products = []

    with open(p, 'r', encoding='utf8') as f:
        is_pattern = True
        for line in f:
            if line.strip():
                if is_pattern:
                    patterns = [c.strip() for c in line.split(',')]
                else:
                    products.append(line.strip())
            else:
                is_pattern=False
    return patterns, products


def traverse(pos: int, product: str, patterns: List[str], memo: List[int]) -> int:
    if pos == len(product):
        return 1
    
    remaing = product[pos:]

    res = 0
    for p in patterns:
        k = len(remaing) - len(p)
        if k < 0:
            continue
         
        if remaing.startswith(p):
            if memo[pos + len(p)] != 0:
                res += memo[pos + len(p)]
            else:
                memo[pos + len(p)] = traverse(pos=pos + len(p), product=product, patterns=patterns, memo=memo)
                res += memo[pos + len(p)]
    return res


def how_many_ways_product_is_made(product: str, patterns: List[str]) -> int:
    memo = [0 for _ in range(len(product)+1)]
    res = traverse(pos=0, product=product, patterns=patterns, memo=memo)
    return res

    
@timer_decorator
def solve_1(p: Path) -> int:
    patterns, products = parse(p=p)
    return functools.reduce(
        lambda x,y: x+y, [
            min(1, how_many_ways_product_is_made(product=o, patterns=patterns)) for o in products], 0)

@timer_decorator
def solve_2(p: Path) -> int:
    patterns, products = parse(p=p)
    return functools.reduce(
        lambda x,y: x+y, [how_many_ways_product_is_made(product=o, patterns=patterns) for o in products], 0)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 6
    assert solve_1(p=in_f) == 213
    assert solve_2(p=t_f) == 16
    assert solve_2(p=in_f) == 1016700771200474
    print("All passed!")
