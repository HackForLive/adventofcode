from pathlib import Path
import sys

import numpy as np

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def apply_action(state: str, action: list[int]):
    n = [0 if s == '0' else 1 for s in state]
    for a in action:
        n[a] = 1 if n[a] == 0 else 0
    
    return ''.join([str(i) for i in n])
 
# memo_cache = np.zeros(shape=(26,26,26), dtype=np.uint64)

def recurse(target_state: str, state: str, actions: list[list[int]], i: int) -> int:
    if i >= len(actions):
        if state != target_state:
            return sys.maxsize
        return 0
    
    if state == target_state:
        return 0
    
    action = actions[i]
    new_state = apply_action(state=state, action=action)
    # take action, apply action to curr_state
    a = recurse(target_state=target_state, state=new_state, actions=actions, i=i+1) + 1

    # skip action
    b = recurse(target_state=target_state, state=state, actions=actions, i=i+1)

    return min(a,b)


def compute(states: list[str], actions: list[list[list[int]]], jolts: list[list[int]]):
    res = 0
    for i, s in enumerate(states):
        action = actions[i]
        state = s
        res += recurse(target_state=state, state='0'*len(state), actions=action, i=0)
    return res

@timer_decorator
def solve_1(p: Path):
    states = []
    actions = []
    jolts = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            action = []
            for i in l.strip().split(' '):
                if i.startswith('['):
                    states.append(''.join(['1' if x == '#' else '0' for x in i[1:-1]]))
                elif i.startswith('('):
                    action.append([int(o) for o in i[1:-1].split(',')])
                else:
                    jolts.append([int(o) for o in i[1:-1].split(',')])
            actions.append(action)

    return compute(states=states, actions=actions, jolts=jolts)

@timer_decorator
def solve_2(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y = [int(i) for i in l.strip().split(',')]
            points.append((x,y))

    return 0

if __name__ == '__main__':
    assert solve_1(p=t_f) == 7
    print(solve_1(p=in_f)) # 558

    # assert solve_2(p=t_f) == 24
    # print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
