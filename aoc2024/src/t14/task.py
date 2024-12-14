import os
from pathlib import Path
import re
import time
from typing import List, Tuple

from attr import dataclass

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'


@dataclass(frozen=True, init=True, slots=True)
class Robot:
    s_pos: Tuple[int, int]
    velocity: Tuple[int, int]

def get_safety_factor(robots: List[Robot], steps: int, w: int, h: int):
    q1 = 0
    q2 = 0
    q3 = 0
    q4 = 0

    h_2 = h // 2
    w_2 = w // 2
    for r in robots:
        x = (r.s_pos[1] + steps*r.velocity[1]) % w
        y = (r.s_pos[0] + steps*r.velocity[0]) % h

        if x < w_2:
            if y < h_2:
                q1 += 1
            if y > h_2:
                q4 += 1 
        elif x > w_2:
            if y < h_2:
                q2 += 1
            if y > h_2:
                q3 += 1
    return q1 * q2 * q3 * q4

def get_safety_factor_q(robots: List[Robot], w: int, h: int):
    start = 1
    limit = 10000
    inc = 1
    for s in range(start, limit, inc):
        pts = {}

        for i in range(h):
            pts[i] = ['.' for _ in range(w)]

        for r in robots:
            x = (r.s_pos[1] + s*r.velocity[1]) % w
            y = (r.s_pos[0] + s*r.velocity[0]) % h
            pts[y][x] = 'X'

        for i in range(h):
            l = ''.join(pts[i])
            if "XXXXXXXXXXX" in l:
                return s
    return -1

@timer_decorator
def solve_1(p: Path, steps: int, w: int, h: int) -> int:
    robots: List[Robot] = []
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            l = line.strip()
            if l:
                matches = re.findall('p=(-?\\d+),(-?\\d+).*v=(-?\\d+),(-?\\d+)', l)
                pos = (int(matches[0][1]), int(matches[0][0]))
                vel = (int(matches[0][3]), int(matches[0][2]))
                robots.append(Robot(s_pos=pos, velocity=vel))

    # print(robots)
    return get_safety_factor(robots=robots, steps=steps, w=w, h=h)


@timer_decorator
def solve_2(p: Path, w: int, h: int) -> int:
    robots: List[Robot] = []
    with open(p, encoding='utf-8', mode='r') as f:
        for line in f:
            l = line.strip()
            if l:
                matches = re.findall('p=(-?\\d+),(-?\\d+).*v=(-?\\d+),(-?\\d+)', l)
                pos = (int(matches[0][1]), int(matches[0][0]))
                vel = (int(matches[0][3]), int(matches[0][2]))
                robots.append(Robot(s_pos=pos, velocity=vel))

    # print(robots)
    return get_safety_factor_q(robots=robots, w=w, h=h)

if __name__ == '__main__':
    assert solve_1(p=t_f, steps=100, h=7, w=11) == 12
    assert solve_1(p=in_f, steps=100, h=103, w=101) == 233709840
    assert solve_2(p=in_f, h=103, w=101) == 6620
    print("All passed!")
