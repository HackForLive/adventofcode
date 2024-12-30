from __future__ import annotations
from collections import deque
from pathlib import Path
import re
from typing import Dict, List, Set, Tuple

from dataclasses import dataclass

from aoc.model.direction import Direction, get_next_left_dir, get_next_right_dir
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np

# @dataclass(frozen=True, init=True)
# class Step:
#     """
#     Current step identified by
#     position (x,y)
#     current direction
#     """
#     x: int
#     y: int
#     price: int = -1

#     def __hash__(self):
#         return hash((self.x, self.y))

#     def __eq__(self, other):
#         return (
#             self.__class__ == other.__class__ and
#             self.x == other.x and
#             self.y == other.y
#         )
    
# def get_point_on_map(c: str, map: np.matrix) -> Tuple[int, int]:
#     rows, cols = np.where(map == c)
#     assert len(rows) == 1
#     assert len(cols) == 1
#     return int(rows[0]), int(cols[0])

# def get_all_directions():
#     return [Direction.EAST, Direction.NORTH, Direction.WEST, Direction.SOUTH]

# def get_directions(d: Direction):
#     return [d, get_next_right_dir(direction=d), get_next_left_dir(direction=d)]

# def bfs(s_p: Step, e_p: Step, m: np.matrix) -> Tuple[int, Set[Step]]:
#     q = deque()

#     q.append(Step(x=s_p.x, y=s_p.y, price=0))
#     visited = set()

#     while q:
#         curr: Step = q.popleft()

#         if curr in visited:
#             continue

#         if curr == e_p:
#             visited.add(curr)
#             return curr.price, visited
        
#         for c_dir in get_all_directions():
#             x = curr.x + c_dir.value[1]
#             y = curr.y + c_dir.value[0]
#             p = m[y, x]
#             if p == '#':
#                 continue
#             next_step = Step(x=x, y=y, price=curr.price+1)
#             q.append(next_step)

#         visited.add(curr)
#     return -1, set()

def get_sequence(code: str) -> List[str]:
    """
    numeric keypad
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    """

    """
    directional keypad
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """

    "=> get directions of first directional keypad => get dir on sec => get dir on third"
    n_keypad = {
        'A' : (3,2),
        '0' : (3,1),
        '3' : (2,2),
        '2' : (2,1),
        '1' : (2,0),
        '6' : (1,2),
        '5' : (1,1),
        '4' : (1,0),
        '9' : (0,2),
        '8' : (0,1),
        '7' : (0,0),
    }

    d_keypad = {
        'A' : (0,2),
        '^' : (0,1),
        '<' : (1,0),
        'v' : (1,1),
        '>' : (1,2),
    }

    return get_shortest_seq(key_pad_s='A', code=code, n_keypad=n_keypad, d_keypad=d_keypad)


def get_shortest_seq(key_pad_s: str, code: str, n_keypad: Dict[str, Tuple[int, int]], 
                     d_keypad: Dict[str, Tuple[int, int]]) -> List[str]:
    
    n_keypad_map = {v:k for k,v in n_keypad.items()}
    
    curr = key_pad_s
    last_pos = curr
    fin_seq = []
    dest = ''
    for i in code:
        # get subsequence for each part of code and append the shortest
        # greedy property go hor/ver or ver/hor if both possible and get the shortest
        
        dest = i
        # print(f"1. {curr =} {dest =}")

        if curr != dest:
            horiz = '>' if n_keypad[curr][1] < n_keypad[dest][1] else '<'
            vert = 'v' if n_keypad[curr][0] < n_keypad[dest][0] else '^'

            
            # can I go horizontally?
            f_s = []
            if (n_keypad[curr][0], n_keypad[dest][1]) in n_keypad_map:
                seq = [horiz for _ in range(abs(n_keypad[curr][1]-n_keypad[dest][1]))]
                seq.extend([vert for _ in range(abs(n_keypad[curr][0]-n_keypad[dest][0]))])
                seq.append('A')
                # print(f'1. {seq =}')
                
                f_s = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)
                
            # can I go vertically?
            s_s = []
            if (n_keypad[dest][0], n_keypad[curr][1]) in n_keypad_map:
                seq = [vert for _ in range(abs(n_keypad[curr][0]-n_keypad[dest][0]))]
                seq.extend([horiz for _ in range(abs(n_keypad[curr][1]-n_keypad[dest][1]))])
                seq.append('A')
                # print(f'1. {seq =}')
                s_s = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)

            # compare both
            if not f_s:
                fin_seq.extend(s_s)
            elif not s_s:
                fin_seq.extend(f_s)
            elif len(f_s) < len(s_s):
                fin_seq.extend(f_s)
            else:
                fin_seq.extend(s_s)
        else:
            seq = ['A']
            n_seq = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)
            fin_seq.extend(n_seq)
            # traverse
        # print(f"{fin_seq =}")
        # exit(0)
        curr = dest
    return fin_seq



def enter_sequence(key_pad_s: str, in_seq: List[str], d_keypad: Dict[str, Tuple[int, int]]
                   ) -> Tuple[List[str], str]:
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    d_keypad_map = {v:k for k,v in d_keypad.items()}
    curr = key_pad_s
    fin_seq = []
    dest = ''
    for i in in_seq:
        dest = i
        # print(f"2. {curr =} {dest =}")
        last = curr
        if curr != dest:
            horiz = '>' if d_keypad[curr][1] < d_keypad[dest][1] else '<'
            vert = 'v' if d_keypad[curr][0] < d_keypad[dest][0] else '^'

            v = [vert for _ in range(abs(d_keypad[curr][0]-d_keypad[dest][0]))]
            h = [horiz for _ in range(abs(d_keypad[curr][1]-d_keypad[dest][1]))]

            # can I go horizontally?
            f_s = []
            if (d_keypad[curr][0], d_keypad[dest][1]) in d_keypad_map:
                seq = []
                seq.extend(h)
                seq.extend(v)
                seq.append('A')
                # print(f'2. {seq =}')
                f_s = enter_sequence_2(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)
                # res
            
            # can I go vertically?
            s_s = []
            if (d_keypad[dest][0], d_keypad[curr][1]) in d_keypad_map:
                seq = []
                seq.extend(v)
                seq.extend(h)
                seq.append('A')
                # print(f'2. {seq =}')
                s_s = enter_sequence_2(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)
            # traverse
            # compare both
            if not f_s:
                fin_seq.extend(s_s)
            elif not s_s:
                fin_seq.extend(f_s)
            elif len(f_s) < len(s_s):
                fin_seq.extend(f_s)
            else:
                fin_seq.extend(s_s)
        else:
            seq = ['A']
            n_seq = enter_sequence_2(key_pad_s='A', in_seq=seq, d_keypad=d_keypad)
            fin_seq.extend(n_seq)
        curr = dest
    return fin_seq


def enter_sequence_2(key_pad_s: str, in_seq: List[str], d_keypad: Dict[str, Tuple[int, int]]
                     ) -> Tuple[List[str], str]:
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    d_keypad_map = {v:k for k,v in d_keypad.items()}
    curr = key_pad_s
    fin_seq = []
    dest = ''
    for i in in_seq:
        dest = i
        # print(f"3. {curr =} {dest =}")
        if curr != dest:
            horiz = '>' if d_keypad[curr][1] < d_keypad[dest][1] else '<'
            vert = 'v' if d_keypad[curr][0] < d_keypad[dest][0] else '^'

            v = [vert for _ in range(abs(d_keypad[curr][0]-d_keypad[dest][0]))]
            h = [horiz for _ in range(abs(d_keypad[curr][1]-d_keypad[dest][1]))]
            # print(f'{h =}')
            # print(f'{v =}')

            f_seq = []
            # can I go horizontally?
            if (d_keypad[curr][0], d_keypad[dest][1]) in d_keypad_map:
                f_seq.extend(h)
                f_seq.extend(v)
                f_seq.append('A')
                # print(f'3. {f_seq =}')
                # res
            # can I go vertically?
            s_seq = []
            if (d_keypad[dest][0], d_keypad[curr][1]) in d_keypad_map:
                s_seq.extend(v)
                s_seq.extend(h)
                s_seq.append('A')
                # print(f'3. {s_seq =}')
            # traverse
            # compare both
            if not f_seq:
                fin_seq.extend(s_seq)
            elif not s_seq:
                fin_seq.extend(f_seq)
            elif len(f_seq) < len(s_seq):
                fin_seq.extend(f_seq)
            else:
                fin_seq.extend(s_seq)
        else:
            seq = ['A']
            # print(f'3. {seq =}')
            fin_seq.extend(seq)
        curr = dest
    return fin_seq


def get_complexity(code: str) -> int:
    matches = re.findall(pattern='(\\d+)', string=code)

    n = int(matches[0])
    m = get_sequence(code=code)
    # print(f"{n =}")
    # print(f"{len(m) =}")
    # print(f"{m =}")
    # print(f"{''.join(m) =}")
    # exit(0)
    return n*len(m)

def get_complexity_sum(codes: List[str]) -> int:
    return sum((get_complexity(code=code) for code in codes))

def parse(p: Path) -> List[str]:
    with open(p, 'r', encoding='utf8') as f:
        return [line.strip() for line in f]

@timer_decorator
def solve(p: Path) -> int:
    codes = parse(p=p)
    return get_complexity_sum(codes=codes)


if __name__ == '__main__':
    print(solve(p=in_f))
    assert solve(p=t_f) == 126384
    assert solve(p=in_f) == 238078
    print("All passed!")
