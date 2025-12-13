from collections import deque
import dataclasses
from pathlib import Path
import sys

import numpy as np

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

@dataclasses.dataclass(frozen=True, init=True)
class Board:
    wide: int
    long: int
    indices: list[int]


def rotate(shape):
    return [(y, 2 - x) for x, y in shape]

def normalize(shape):
    minx = min(x for x, y in shape)
    miny = min(y for x, y in shape)
    return sorted((x - minx, y - miny) for x, y in shape)

def unique_rotations(shape):
    rots = set()
    cur = shape
    for _ in range(4):
        cur = rotate(cur)
        rots.add(tuple(normalize(cur)))
    return [list(r) for r in rots]

# def best_combination():
#     for each x, y shape 


def compute(presents: dict[str, list[tuple[int,int]]], wide: int, long: int, indices: list[int]) -> int:

    # 3x3

    # meta shapes better than 6x3 6x6 etc

    # naive put all 3x3
    alls = sum(indices)

    upper_bound = (wide // 3)*(long // 3)
    if upper_bound > alls:
        return 1

    print(presents)
    # print(boards)
    return 0

def compute_all(presents: dict[str, list[tuple[int,int]]], boards: list[Board]) -> int:
    return sum(compute(presents=presents, wide=b.wide, long=b.long, indices=b.indices) for b in boards)

@timer_decorator
def solve_1(p: Path):
    presents = {}
    boards = []
    with open(p, 'r', encoding='utf8') as f:
        is_present = True
        last_p_id = 0
        last_p = []
        i = 0
        for l in f:
            if 'x' in l:
                is_present = False
            
            if is_present:
                line = l.strip()
                if ':' in line:
                    last_p_id = int(line[0])
                elif not line:
                    presents[last_p_id] = last_p
                    last_p = []
                    i = 0
                    continue
                else:
                    for j in range(3):
                        if line[j] == '#':
                            last_p.append((i,j))
                    i += 1
                    
            else:
                le, ri = l.strip().split(':')

                wide, long = [int(i.strip()) for i in le.split('x') if i.strip()]
                indices = [int(i.strip()) for i in ri.split(' ') if i.strip()]

                boards.append(Board(wide=wide, long=long, indices=indices))

    return compute_all(presents=presents, boards=boards)

if __name__ == '__main__':
    print(solve_1(p=t_f))
    assert solve_1(p=t_f) == 2
    print(solve_1(p=in_f)) # 607

    print("All passed!")
