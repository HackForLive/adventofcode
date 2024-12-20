from __future__ import annotations
from collections import deque
from pathlib import Path
from typing import Dict, List, Set, Tuple

from dataclasses import dataclass

from aoc.model.direction import Direction, get_next_left_dir, get_next_right_dir
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np

@dataclass(frozen=True, init=True)
class Step:
    """
    Current step identified by
    position (x,y)
    current direction
    """
    x: int
    y: int
    price: int = -1

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )
    
def get_point_on_map(c: str, map: np.matrix) -> Tuple[int, int]:
    rows, cols = np.where(map == c)
    assert len(rows) == 1
    assert len(cols) == 1
    return int(rows[0]), int(cols[0])

def get_all_directions():
    return [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]

def get_directions(d: Direction):
    return [d, get_next_right_dir(direction=d), get_next_left_dir(direction=d)]

def bfs(s_p: Step, e_p: Step, m: np.matrix) -> Tuple[int, Set[Step]]:
    q = deque()

    q.append(Step(x=s_p.x, y=s_p.y, price=0))
    visited = set()

    while q:
        curr: Step = q.popleft()

        if curr in visited:
            continue

        if curr == e_p:
            visited.add(curr)
            return curr.price, visited
        
        for c_dir in get_all_directions():
            x = curr.x + c_dir.value[1]
            y = curr.y + c_dir.value[0]
            p = m[y, x]
            if p == '#':
                continue
            next_step = Step(x=x, y=y, price=curr.price+1)
            q.append(next_step)

        visited.add(curr)
    return -1, set()


def bfs_find_cheats(s_p: Step, e_p: Step, points: Dict[Tuple[int, int], int], m: np.matrix) -> List[int]:
    q = deque()

    q.append(Step(x=s_p.x, y=s_p.y, price=0))
    visited = set()
    cheats = []

    while q:
        curr: Step = q.popleft()

        if curr in visited:
            continue

        if curr == e_p:
            visited.add(curr)
            break
        
        for c_dir in get_all_directions():
            x = curr.x + c_dir.value[1]
            y = curr.y + c_dir.value[0]
            p = m[y, x]
            if p == '#':
                # test if cheat
                for cc_dir in get_directions(d=c_dir):
                    xx = x + cc_dir.value[1]
                    yy = y + cc_dir.value[0]
                    # fix here the ds
                    if ((curr.y, curr.x) in points) and ((yy, xx) in points):
                        diff = points[(curr.y, curr.x)] - points[(yy, xx)] - 2
                        if diff > 0:
                            cheats.append(diff)
                            # return cheats
                continue
            next_step = Step(x=x, y=y, price=curr.price+1)
            q.append(next_step)
    
        visited.add(curr)
    return cheats


def get_number_of_cheats(s_p: Tuple[int, int], e_p: Tuple[int, int], cheat_lim: int, m: np.matrix) -> int:
    start_s = Step(x=s_p[1], y=s_p[0])
    end_s = Step(x=e_p[1], y=e_p[0])
    _, steps = bfs(s_p=end_s, e_p=start_s, m=m)

    d ={(step.y, step.x): step.price for step in steps}

    cheats = bfs_find_cheats(s_p=start_s, e_p=end_s, points=d, m=m)
    # print(cheats)

    return sum((1 for i in cheats if i >= cheat_lim))
    

def parse(p: Path) -> np.matrix:
    with open(p, 'r', encoding='utf8') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix

@timer_decorator
def solve_1(p: Path, cheat_lim: int) -> int:
    matrix = parse(p=p)
    s_p = get_point_on_map(c='S', map=matrix)
    e_p = get_point_on_map(c='E', map=matrix)
    return get_number_of_cheats(s_p=s_p, e_p=e_p, cheat_lim=cheat_lim, m=matrix)

# @timer_decorator
# def solve_2(p: Path, cheat_lim: int) -> int:
#     matrix = parse(p=p)
#     s_p = get_point_on_map(c='S', map=matrix)
#     e_p = get_point_on_map(c='E', map=matrix)
#     return get_number_of_cheats(s_p=s_p, e_p=e_p, cheat_lim=cheat_lim, m=matrix)


if __name__ == '__main__':

    assert solve_1(p=t_f, cheat_lim=10) == 10 
    assert solve_1(p=in_f, cheat_lim=100) == 1286
    print("All passed!")
