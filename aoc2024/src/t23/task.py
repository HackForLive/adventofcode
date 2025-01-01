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


def parse(p: Path) -> Tuple[Set, Dict[str, List[str]]]:
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

def find_cycles(start: str, adj: Dict[str, List[str]]) -> List[List[str]]:
    
    visited = set()

    s_node = Node(name=start, parent=None)
    stack = deque([s_node])

    cycles = []
    while stack:
        curr = stack.pop()

        if curr in visited:
            # get all node names

            cycle = [curr.name]
            tmp = curr
            while tmp.parent:
                if tmp.parent.name == curr.name:
                    break
                cycle.append(tmp.parent.name)
                tmp = tmp.parent
            
            cycles.append(sorted(cycle))
            continue
        
        visited.add(curr)

        for neighbor in adj[curr.name]:
            stack.append(Node(name=neighbor, parent=curr))

    return cycles


def is_complete_graph(cycle: List[str], adj: Dict[str, List[str]]):
    for i in range(len(cycle)):
        for j in range(i+1, len(cycle)):
            if (not cycle[i] in adj[cycle[j]]) or (not cycle[j] in adj[cycle[i]]):
                return False
    return True

    
def get_unique_cycles(v: Set[str], adj: Dict[str, List[str]]) -> List[List[str]]:
     # keep track of cycles
    # tuple of nodes
    cycles = []
   
    # for each vertice
    # do BFS
    for n in v:
        n_cycles = find_cycles(start=n, adj=adj)
        for cycle in n_cycles:
            if is_complete_graph(cycle=cycle, adj=adj):
                cycles.append(sorted(cycle))
    return cycles

def get_cycles_with_chief(cycles: List[List[str]], start_letter: str) -> List[Tuple]:
    res = []
    for cycle in cycles:
        for n in cycle:
            if n.startswith(start_letter):
                res.append(cycle)
                break
    return res

def longest_cycle(v: Set[str], adj: Dict[str, List[str]]) -> str:
    
    # keep track of cycles
    # tuple of nodes
    cycles = get_unique_cycles(v=v, adj=adj)

    max_l = 0
    max_nodes = ()
    for c in cycles:
        if len(c) > max_l:
            max_l = len(c)
            max_nodes = c

    return ','.join(sorted(set(max_nodes)))


@timer_decorator
def solve_2_alternative(p: Path) -> str:
    v, adj = parse(p=p)
    return longest_cycle(v=v, adj=adj)



@timer_decorator
def solve_1(p: Path, count: int) -> int:
    v, adj = parse(p=p)

    from itertools import combinations

    res = {}
    for k, v in adj.items():
        for c in combinations(iterable=[k]+v, r=count):
            i = tuple(sorted(c))
            res[i] = res.get(i, 0) + 1
    
    r = []
    for k, v in res.items():
        is_chief = False
        for j in k:
            if j.startswith('t'):
                is_chief = True
                break
        if is_chief and (v >= count):
            if is_complete_graph(cycle=k, adj=adj):
                r.append(k)
    return len(r)

@timer_decorator
def solve_2(p: Path) -> str:
    v, adj = parse(p=p)

    for k, v in adj.items():
        count = len(v)
        break
    from itertools import combinations

    res = {}
    for k, v in adj.items():
        for c in combinations(iterable=[k]+v, r=count):
            i = tuple(sorted(c))
            res[i] = res.get(i, 0) + 1
    for k, v in res.items():
        if (v >= count) and is_complete_graph(cycle=k, adj=adj):
            return ','.join(k)
    
    return ''


if __name__ == '__main__':

    assert solve_1(p=t_f, count=3) == 7
    assert solve_1(p=in_f, count=3) == 1358
    assert solve_2(p=t_f) == 'co,de,ka,ta'
    assert solve_2(p=in_f) == 'cl,ei,fd,hc,ib,kq,kv,ky,rv,vf,wk,yx,zf'

    # very slow
    # print(solve_2_alternative(p=in_f))

    print("All passed!")
