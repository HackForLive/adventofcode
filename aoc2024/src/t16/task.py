from __future__ import annotations
from collections import deque
import heapq
from pathlib import Path
from typing import Set, Tuple

from dataclasses import dataclass

from aoc.model.direction import Direction, get_next_left_dir, get_next_right_dir
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'

import numpy as np

@dataclass(frozen=True, init=True)
class Step:
    """
    Current step identified by
    position (x,y)
    current direction
    current heat loss
    current steps (incremented by same direction)
    """
    x: int
    y: int
    direction: Direction
    price: int

    def __lt__(self, other):
        return self.price < other.price
    
def get_point_on_map(c: str, map: np.matrix) -> Tuple[int, int]:
    rows, cols = np.where(map == c)
    assert len(rows) == 1
    assert len(cols) == 1
    return int(rows[0]), int(cols[0])

def get_directions(d: Direction):
    return [d, get_next_left_dir(d), get_next_right_dir(d)]

def cache_key(step: Step) -> Tuple[int, int, str]:
    # without price !  step.price
    return (step.y, step.x, step.direction.name)

def cache_key_all(step: Step) -> Tuple[int, int, str, int]:
    # without price !  step.price
    return (step.y, step.x, step.direction.name, step.price)

def get_unique_points_at_all_best_paths(
    e_s: Step, visited: Set[Tuple[int, int, str, int]]) -> int:

    q = deque()
    q.append(e_s)

    uniq = set()

    while q:
        curr: Step = q.popleft()

        if curr in uniq:
            continue
        
        for c_dir in get_directions(curr.direction):
            if c_dir != curr.direction:
                prev_step = Step(x=curr.x, y=curr.y, direction=c_dir, price=curr.price-1000)

            else:
                prev_step = Step(x=curr.x - c_dir.value[1], y=curr.y - c_dir.value[0], direction=c_dir, 
                            price=curr.price-1)
            if cache_key_all(step=prev_step) in visited:
                q.append(prev_step)
    
        uniq.add((curr.y, curr.x))
    return len(uniq)
    


def shortest_paths_points(m: np.matrix, rotate_cost: int, s_p: Tuple[int, int], e_p: Tuple[int, int]
                          ) -> Tuple[int, int]:
    
    s_east = Step(y=s_p[0], x=s_p[1], direction=Direction.EAST, price=0)
    # print(f"{s_p =}")
    # print(f"{e_p =}")
    pq = []
    heapq.heappush(pq, s_east)

    # visited
    visited = set()
    visited.add(cache_key(s_east))

    visited_f = set()
    visited_f.add(cache_key_all(s_east))
    while pq:
        u: Step = heapq.heappop(pq)
        if u.x == e_p[1] and u.y == e_p[0]:
            return u.price, get_unique_points_at_all_best_paths(e_s=u, visited=visited_f)

        for c_dir in get_directions(u.direction):
            ny = u.y
            nx = u.x
            curr_price = 1

            # handle rotation price
            if c_dir != u.direction:
                curr_price = rotate_cost
            else:
                ny = u.y + c_dir.value[0]
                nx = u.x + c_dir.value[1]
                if m[ny, nx] == '#':
                    continue

            next_step: Step = Step(
                x = nx,
                y = ny,
                direction=c_dir,
                price=u.price + curr_price,
            )
            if not cache_key(next_step) in visited:
                heapq.heappush(pq, next_step)
                visited.add(cache_key(next_step))
                visited_f.add(cache_key_all(next_step))
    return -1, -1


def parse(p: Path):
    with open(p, 'r', encoding='utf8') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return matrix

@timer_decorator
def solve_1(p: Path) -> int:
    matrix = parse(p=p)
    rotate_cost = 1000
    s_p = get_point_on_map(c='S', map=matrix)
    e_p = get_point_on_map(c='E', map=matrix)
    price, _ = shortest_paths_points(m=matrix, rotate_cost=rotate_cost, s_p=s_p, e_p=e_p)
    return price

@timer_decorator
def solve_2(p: Path) -> int:
    matrix = parse(p=p)
    rotate_cost = 1000
    s_p = get_point_on_map(c='S', map=matrix)
    e_p = get_point_on_map(c='E', map=matrix)
    _, points = shortest_paths_points(m=matrix, rotate_cost=rotate_cost, s_p=s_p, e_p=e_p)
    return points


if __name__ == '__main__':
    assert solve_1(p=t_f) == 7036
    assert solve_1(p=t2_f) == 11048
    assert solve_1(p=in_f) == 143580

    assert solve_2(p=t_f) == 45
    assert solve_2(p=t2_f) == 64
    assert solve_2(p=in_f) == 645
    print("All passed!")
