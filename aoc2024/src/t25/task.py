from typing import List, Tuple
from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
 
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def parse(p: Path) -> Tuple[List[List[int]], List[List[int]]]:
    with open(p, 'r', encoding='utf8') as f:

        locks = []
        keys = []

        start = True
        counter = [0, 0, 0, 0, 0]
        for line in f:
            l = line.strip()

            if not l:
                start = True
                if key:
                    keys.append(counter)
                if lock:
                    locks.append(counter)
                continue

            if start:
                if l == '#####':
                    lock = True
                    key = False
                    counter = [0, 0, 0, 0, 0]
                else:
                    lock = False
                    key = True
                    counter = [-1, -1, -1, -1, -1]
                start = False
                continue
            
            for ii, i in enumerate(l):
                if i == '#':
                    counter[ii] += 1             
            
        if key:
            keys.append(counter)
        if lock:
            locks.append(counter)
        return keys, locks

@timer_decorator
def solve(p: Path) -> int:
    keys, locks = parse(p=p)

    res = 0
    for k in keys:
        for l in locks:
            m = True
            for j in range(len(l)):
                if k[j] + l[j] > 5:
                    m = False
                    break
            res = res + 1 if m else res
    # print(f"{keys =}")
    # print(f"{locks =}")
    return res
   

if __name__ == '__main__':
    assert solve(p=t_f) == 3
    assert solve(p=in_f) == 3223
    print("All passed!")