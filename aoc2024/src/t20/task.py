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

def bfs_update_cheat_paths(
        s_x: int, s_y: int, m: np.matrix, cheats: Dict[Tuple[int, int, int, int], int], max_cheat_l: int,
        d: Direction, points: Dict[Tuple[int, int], int]) -> Dict[Tuple[int, int, int, int], int]:

    from_x = s_x - d.value[1]
    from_y = s_y - d.value[0]

    if (from_y, from_x) not in points:
        return cheats

    for k, v in points.items():
        y = k[0]
        x = k[1]

        price = abs(from_y-y) + abs(from_x-x)

        if price > max_cheat_l:
            continue

        diff = points[(from_y, from_x)] - (points[(y, x)] + price)
        if diff > 0:
            if (from_y, from_x, y, x) not in cheats:
                cheats[(from_y, from_x, y, x)] = diff
    return cheats


def bfs_find_cheats(s_p: Step, e_p: Step, points: Dict[Tuple[int, int], int], max_cheat_l:int,
                    m: np.matrix) -> Dict[Tuple[int, int, int, int], int]:
    q = deque()

    q.append(Step(x=s_p.x, y=s_p.y, price=0))
    visited = set()
    cheats = {}

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
                # test all cheats
                cheats = bfs_update_cheat_paths(s_x=x, s_y=y, m=m, cheats=cheats, max_cheat_l=max_cheat_l, 
                                            d=c_dir, points=points)
                continue
            next_step = Step(x=x, y=y, price=curr.price+1)
            q.append(next_step)
    
        visited.add(curr)
    return cheats

def get_number_of_cheats(s_p: Tuple[int, int], e_p: Tuple[int, int], cheat_lim: int, max_cheat_l: int,
                           m: np.matrix) -> int:
    start_s = Step(x=s_p[1], y=s_p[0])
    end_s = Step(x=e_p[1], y=e_p[0])
    _, steps = bfs(s_p=end_s, e_p=start_s, m=m)

    d ={(step.y, step.x): step.price for step in sorted(steps, key=lambda x:x.price)}
    cheats = bfs_find_cheats(s_p=start_s, e_p=end_s, points=d, max_cheat_l=max_cheat_l, m=m)

    return sum((1 for _, v in cheats.items() if v >= cheat_lim))
    

def parse(p: Path) -> np.matrix:
    with open(p, 'r', encoding='utf8') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix

@timer_decorator
def solve(p: Path, cheat_lim: int, max_cheat_l: int) -> int:
    matrix = parse(p=p)
    s_p = get_point_on_map(c='S', map=matrix)
    e_p = get_point_on_map(c='E', map=matrix)
    return get_number_of_cheats(s_p=s_p, e_p=e_p, cheat_lim=cheat_lim, max_cheat_l=max_cheat_l, m=matrix)


if __name__ == '__main__':
    assert solve(p=t_f, cheat_lim=10, max_cheat_l=2) == 10
    assert solve(p=in_f, cheat_lim=100, max_cheat_l=2) == 1286
    assert solve(p=t_f, cheat_lim=50, max_cheat_l=20) == 285
    assert solve(p=in_f, cheat_lim=100, max_cheat_l=20) == 989316
    print("All passed!")
