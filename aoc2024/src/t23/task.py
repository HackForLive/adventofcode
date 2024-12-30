from typing import List, Dict, Set, Tuple
from pathlib import Path
from collections import deque

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
 
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def parse(p: Path) -> Tuple[Set, Dict]:
    adj = {}
    vert = set()
    with open(p, 'r', encoding='utf8') as f:
        for line in f:
            l, r = [str(i) for i in line.strip().split('-')]
            
            if l not in adj:
                adj[l]=[r]
            else:
                adj[l].append(r)
                
            if r not in adj:
                adj[r]=[l]
            else:
                adj[r].append(l)
            vert.add(r)
            vert.add(l)         
        return vert, adj

@timer_decorator
def solve(p: Path) -> int:
    v, adj = parse(p=p)
    
    v=list(v)
    res = set()
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            for k in range(j+1, len(v)):
                if not (v[i].startswith('t') or v[j].startswith('t') or v[k].startswith('t')):
                    continue
                if v[i] in adj[v[k]] and v[j] in adj[v[k]] and v[j] in adj[v[i]]:
                    res.add((v[i], v[j], v[k]))
                
    return len(res)

def solve_2(p: Path) -> int:
    v, adj = parse(p=p)
    # print(v)
    print(len(v))
    res =0
    return res
   

if __name__ == '__main__':
    assert solve(p=t_f) == 7
    assert solve(p=in_f) == 1358
    print(solve_2(p=in_f))
    print("All passed!")
