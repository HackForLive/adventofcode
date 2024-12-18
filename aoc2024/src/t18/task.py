from __future__ import annotations
from collections import deque
from pathlib import Path
import re
from typing import List, Set, Tuple

from aoc.model.direction import Direction
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def parse(p: Path) -> List[Tuple[int, int]]:
    bytes_pos = []

    with open(p, 'r', encoding='utf8') as f:
        for line in f:
            matches = re.findall('(\\d+),(\\d+)', line)
            bytes_pos.append((int(matches[0][1]), int(matches[0][0])))
        return bytes_pos
    

def check_valid_pos(pos: Tuple[int, int], 
                    bytes_p: Set[Tuple[int, int]], s_pos: Tuple[int, int], e_pos: Tuple[int, int]) -> bool:
    if not ((s_pos[0] <= pos[0] <= e_pos[0]) and (s_pos[1] <= pos[1] <= e_pos[1])):
        return False
    if pos in bytes_p:
        return False
    return True

def get_directions() -> List[Direction]:
    return [Direction.NORTH, Direction.EAST, Direction.WEST, Direction.SOUTH]

def bfs(bytes_p: Set[Tuple[int, int]], s_pos: Tuple[int, int], e_pos: Tuple[int, int]):

    q = deque()
    q.append((s_pos[0], s_pos[1], 0))

    visited = set()

    while q:
        curr = q.popleft()
        if (curr[0], curr[1]) in visited: 
            continue 

        if curr[0] == e_pos[0] and curr[1] == e_pos[1]:
            return curr[2]
        
        for dir in get_directions():
            y = curr[0] + dir.value[0]
            x = curr[1] + dir.value[1]

            if check_valid_pos(pos=(y, x), bytes_p=bytes_p, s_pos=s_pos, e_pos=e_pos):
                q.append((y, x, curr[2] + 1))

        visited.add((curr[0], curr[1])) 

    return -1


def find_first_blocker(bytes_p: List[Tuple[int, int]], s_pos: Tuple[int, int], e_pos: Tuple[int, int]
                       ) -> Tuple[int, int]:
    # could be written better => binary search
    for i in range(len(bytes_p)):
        if bfs(bytes_p=set(bytes_p[:i+1]), s_pos=s_pos, e_pos=e_pos) == -1:
            return bytes_p[i]
    return (-1, -1)
    

@timer_decorator
def solve_1(p: Path, s_pos: Tuple[int, int], e_pos: Tuple[int, int], b_limit: int) -> int:
    b_list = set(parse(p=p)[:b_limit])
    return bfs(bytes_p=b_list, s_pos=s_pos, e_pos=e_pos)

@timer_decorator
def solve_2(p: Path, s_pos: Tuple[int, int], e_pos: Tuple[int, int]) -> Tuple[int, int]:
    b_list = parse(p=p)
    return find_first_blocker(bytes_p=b_list, s_pos=s_pos, e_pos=e_pos)

if __name__ == '__main__':
    assert solve_1(p=t_f, s_pos=(0,0), e_pos=(6,6), b_limit=12) == 22
    assert solve_1(p=in_f, s_pos=(0,0), e_pos=(70,70), b_limit=1024) == 338
    assert solve_2(p=t_f, s_pos=(0,0), e_pos=(6,6)) == (1,6)
    assert solve_2(p=in_f, s_pos=(0,0), e_pos=(70,70)) == (44,20)
    print("All passed!")
