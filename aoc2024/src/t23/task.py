from __future__ import annotations
from typing import List, Dict, Set, Tuple
from pathlib import Path
from collections import deque
from dataclasses import dataclass

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
 
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


@dataclass(frozen=False, init=True, unsafe_hash=False)
class Node:
    name: str
    parent: Node | None

    def __eq__(self, obj):
        return isinstance(obj, Node) and obj.name == self.name
    
    def __hash__(self):
        return hash(self.name)


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

def find_cycle(start: str, adj: Dict[str, str]) -> Tuple:
    
    visited = set()

    s_node = Node(name=start, parent=None)
    stack = deque([s_node])

    while stack:
        curr = stack.pop()

        if curr in visited:
            # get all node names

            res = set([curr.name])
            tmp = curr
            while tmp.parent:
                # if tmp.parent.name in res:
                #     break
                res.add(tmp.parent.name)
                tmp = tmp.parent
            
            return tuple(res)
        visited.add(curr)

        for neighbor in adj[curr.name]:
            stack.append(Node(name=neighbor, parent=curr))

    return ()


def is_complete_graph(v: Tuple, adj: Dict[str, str]):
    for i in range(len(v)):
        for j in range(i+1, len(v)):
            if not v[i] in adj[v[j]]:
                return False
    return True


def longest_cycle(v: Set[str], adj: Dict[str, str]) -> str:
    
    # keep track of cycles
    # tuple of nodes
    cycles = set()
   
    # for each vertice
    # do BFS
    for n in v:
        cycle = find_cycle(start=n, adj=adj)
        print(cycle)
        if is_complete_graph(v=cycle, adj=adj):
            cycles.add(cycle)

    max_l = 0
    max_nodes = ()
    for c in cycles:
        if len(c) > max_l:
            max_l = len(c)
            max_nodes = c

    return ','.join(sorted(set(max_nodes)))
    

def solve_2(p: Path) -> str:
    v, adj = parse(p=p)
    # print(adj)
    return longest_cycle(v=v, adj=adj)
   

if __name__ == '__main__':
    assert solve(p=t_f) == 7
    assert solve(p=in_f) == 1358
    print(solve_2(p=in_f))
    print("All passed!")
