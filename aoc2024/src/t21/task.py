from __future__ import annotations
from pathlib import Path
import re
import sys
from typing import Dict, List, Tuple

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def get_sequence(code: str, robot_n: int) -> int:
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

    return get_shortest_seq(key_pad_s='A', code=code, n_keypad=n_keypad, d_keypad=d_keypad, d=robot_n)


def get_shortest_seq(key_pad_s: str, code: str, n_keypad: Dict[str, Tuple[int, int]], 
                     d_keypad: Dict[str, Tuple[int, int]], d: int) -> int:
    
    n_keypad_map = {v:k for k,v in n_keypad.items()}
    
    curr = key_pad_s
    res = 0
    dest = ''
    for i in code:
        # get subsequence for each part of code and append the shortest
        # greedy property go hor/ver or ver/hor if both possible and get the shortest
        
        dest = i

        if curr != dest:
            horiz = '>' if n_keypad[curr][1] < n_keypad[dest][1] else '<'
            vert = 'v' if n_keypad[curr][0] < n_keypad[dest][0] else '^'

            v = [vert for _ in range(abs(n_keypad[curr][0]-n_keypad[dest][0]))]
            h = [horiz for _ in range(abs(n_keypad[curr][1]-n_keypad[dest][1]))]

            # can I go horizontally?
            h_f = sys.maxsize
            if (n_keypad[curr][0], n_keypad[dest][1]) in n_keypad_map:
                seq = h + v + ['A']
                
                h_f = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d)
                
            # can I go vertically?
            v_f = sys.maxsize
            if (n_keypad[dest][0], n_keypad[curr][1]) in n_keypad_map:
                seq = v + h + ['A']
                v_f = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d)

            # compare both
            res += min(h_f, v_f)
        else:
            seq = ['A']
            res += enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d)
            # traverse
        curr = dest
    return res

memo = {}

def enter_sequence(key_pad_s: str, in_seq: List[str], d_keypad: Dict[str, Tuple[int, int]], d: int) -> int:
    """
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    """
    if not d > 0:
        return len(in_seq)
    
    if (''.join(in_seq), d) in memo:
        return memo[(''.join(in_seq), d)]

    d_keypad_map = {v:k for k,v in d_keypad.items()}
    curr = key_pad_s
    res = 0
    dest = ''
    for i in in_seq:
        dest = i
        if curr != dest:
            horiz = '>' if d_keypad[curr][1] < d_keypad[dest][1] else '<'
            vert = 'v' if d_keypad[curr][0] < d_keypad[dest][0] else '^'

            v = [vert for _ in range(abs(d_keypad[curr][0]-d_keypad[dest][0]))]
            h = [horiz for _ in range(abs(d_keypad[curr][1]-d_keypad[dest][1]))]

            # can I go horizontally first?
            # f_s = []
            h_f = sys.maxsize
            if (d_keypad[curr][0], d_keypad[dest][1]) in d_keypad_map:
                seq = h + v + ['A']
                h_f = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d-1)
            
            # can I go vertically first?
            # s_s = []
            v_f = sys.maxsize
            if (d_keypad[dest][0], d_keypad[curr][1]) in d_keypad_map:
                seq = v + h + ['A']
                v_f = enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d-1)
            # traverse
            # compare both
            res += min(v_f, h_f)
        else:
            seq = ['A']
            res += enter_sequence(key_pad_s='A', in_seq=seq, d_keypad=d_keypad, d=d-1)
        curr = dest
    
    memo[(''.join(in_seq), d)] = res
    return res

def get_complexity(code: str, robot_n: int) -> int:
    n = int(re.findall(pattern='(\\d+)', string=code)[0])
    return n*get_sequence(code=code, robot_n=robot_n)

def parse(p: Path) -> List[str]:
    with open(p, 'r', encoding='utf8') as f:
        return [line.strip() for line in f]

@timer_decorator
def solve(p: Path, robot_n: int) -> int:
    return sum((get_complexity(code=code, robot_n=robot_n) for code in parse(p=p)))


if __name__ == '__main__':
    assert solve(p=t_f, robot_n=2) == 126384
    assert solve(p=in_f, robot_n=2) == 238078
    assert solve(p=in_f, robot_n=25) == 293919502998014
    print("All passed!")
