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

def apply_jolt(jolt: tuple, action: list[int], n: int):
    tmp = list(jolt)
    for a in action:
        tmp[a] = tmp[a] + n
    
    return tuple(tmp)

def max_jolt(jolt: tuple, target_jolt: tuple, action: list[int]) -> int:
   
    res = sys.maxsize
    for i in action:
        curr_res = target_jolt[i]-jolt[i]
        if curr_res < res:
            res = curr_res
    
    return res
 
memo = {}

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
    if (new_state, i) not in memo:
        a = recurse(target_state=target_state, state=new_state, actions=actions, i=i+1) + 1
        memo[(new_state, i+1)] = a
    else:
        a = memo[(new_state, i)]
    # skip action
    if (state, i) not in memo:
        b = recurse(target_state=target_state, state=state, actions=actions, i=i+1)
        memo[(state, i+1)] = b
    else:
        b = memo[(state, i)]

    return min(a,b)


def compute(states: list[str], actions: list[list[list[int]]]):
    res = 0
    global memo
    for i, s in enumerate(states):
        memo = {}
        action = actions[i]
        state = s
        res += recurse(target_state=state, state='0'*len(state), actions=action, i=0)
    return res


def recurse_jolts(target_jolt: tuple, jolt: tuple, actions: list[list[int]], i: int) -> int:
    if i >= len(actions):
        if jolt != target_jolt:
            return sys.maxsize
        return 0
    
    if jolt == target_jolt:
        return 0
    if (jolt) + (i,) in memo:
        # print('cache')
        return memo[(jolt) + (i,)]

    action = actions[i]
    
    res = []
    # apply as many times possible

    n = max_jolt(jolt=jolt, target_jolt=target_jolt, action=action)
    if n < 0:
        return sys.maxsize
    # print(n)
    for k in reversed(range(0, n+1)):
        # print(k)
        if k > 0:
            new_jolt = apply_jolt(jolt=jolt, action=action, n=k)
        else:
            new_jolt = jolt

        a = recurse_jolts(target_jolt=target_jolt, jolt=new_jolt, actions=actions, i=i+1) + k
        res.append(a)
        
    rr = min(res)
    memo[(jolt) + (i,)] = rr
    return rr


def compute_jolts(actions: list[list[list[int]]], jolts: list[tuple]):
    res = 0
    global memo
    for j, jolt in enumerate(jolts):
        # if j != 8:
        #     continue
        memo = {}
        action = actions[j]
        tmp = recurse_jolts(target_jolt=jolt, jolt=tuple([0]*len(jolt)), actions=action, i=0)
        print(tmp)
        res += tmp
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
                    jolts.append(tuple([int(o) for o in i[1:-1].split(',')]))
            actions.append(action)

    return compute(states=states, actions=actions)

@timer_decorator
def solve_2(p: Path):
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
                    jolts.append(tuple([int(o) for o in i[1:-1].split(',')]))
            actions.append(action)

    return compute_jolts(actions=actions, jolts=jolts)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 7
    print(solve_1(p=in_f)) # 558

    # 10 + 12 + 11 = 33
    assert solve_2(p=t_f) == 33
    print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
