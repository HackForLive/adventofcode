import itertools
from pathlib import Path
import sys
from collections import deque

from aoc.performance import timer_decorator
from solver import solve_min_items_unbounded

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
 
def compute(states: list[str], actions: list[list[list[int]]]):
    def recurse(target_state: str, actions_i: list[list[int]], state: str, i: int) -> int:
        if i >= len(actions_i):
            if state != target_state:
                return sys.maxsize
            return 0
        
        if state == target_state:
            return 0
        
        action = actions_i[i]

        # take action, apply action to curr_state
        a = recurse(
            target_state=target_state, actions_i=actions_i, state=apply_action(state=state, action=action), 
            i=i+1) + 1
        # skip action
        b = recurse(target_state=target_state, actions_i=actions_i, state=state, i=i+1)
        return min(a,b)

    return itertools.accumulate(func=lambda x,y: x+y, iterable=(
        recurse(target_state=s, actions_i=actions[i], state='0'*len(s), i=0) for i, s in enumerate(states)))


def bfs(items: list[list[int]], target: tuple):
    # items: list of tuples, e.g. [(1,5,6), (2,5,9)]
    # target: tuple of target counts, e.g. (10,20,30,4,...)

    n = len(target)
    start = (0,) * n

    queue = deque([start])
    dist = {start: 0}

    while queue:
        state: tuple = queue.popleft()
        steps = dist[state]

        if state == target:
            return steps

        for item in items:
            # create next state
            new_state = list(state)
            for idx in item:
                new_state[idx] += 1

            new_state = tuple(new_state)

            # prune states that go beyond target
            if any(new_state[i] > target[i] for i in range(n)):
                continue

            # skip visited
            if new_state in dist:
                continue

            dist[new_state] = steps + 1
            queue.append(new_state)

    return None  # no solution

def verify(picks: list[int], jolts: list[tuple], actions: list[list[int]]):
    curr = (0,)*len(jolts)

    for i, pick in enumerate(picks):
        curr = apply_jolt(jolt=curr, action=actions[i], n=pick)

    return all(curr[i] == jolts[i] for i in range(len(jolts)))

def compute_jolts(actions: list[list[list[int]]], jolts: list[tuple]):
    res = 0
    for j, jolt in enumerate(jolts):
        action = actions[j]

        tmp, picks = solve_min_items_unbounded(items=action, target=jolt, debug=False, time_limit_s=40)
        
        assert verify(picks=picks, jolts=jolt, actions=action) and tmp and isinstance(picks, list)
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
    assert solve_1(p=t_f) #== 7
    print(solve_1(p=in_f)) # 558

    assert solve_2(p=t_f) == 33
    print(solve_2(p=in_f)) # => too low 20317
    print("All passed!")
