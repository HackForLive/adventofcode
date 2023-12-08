from __future__ import annotations
import os
import pathlib
import math
from typing import Dict, List, Tuple

from itertools import cycle

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')


def parse():
    with open(input_file, 'r', encoding='utf8') as f:
        lines = f.readlines()
        instr: List[str] = []
        node_dict: Dict[str, Tuple[str, str]] = {}
        for i, line in enumerate(lines):
            clean_l = line.strip()
            if clean_l == '':
                continue
            if i == 0:
                instr = list(clean_l)
            else:
                k, r = clean_l.split(' = ')
                l, r = r.split(', ')

                node_dict[k] = (l[1:], r[:-1])

    return instr, node_dict

def find_steps_for_node(node: str, node_dict: Dict[str, Tuple[str, str]], instr: List[str]):
    steps = 0
    curr = node
    for instruction in cycle(instr):
        curr = node_dict[curr][1 if instruction == 'R' else 0]
        steps += 1
        if curr.endswith('Z'):
            break
    return steps

def solve_1():
    instr, node_dict = parse()
    print(find_steps_for_node(node='AAA', instr=instr, node_dict=node_dict))

def solve_2():
    instr, node_dict = parse()
    curr: List[str] = [node_name for node_name in node_dict if node_name[-1] == 'A']
    print(math.lcm(*[find_steps_for_node(node=c, instr=instr, node_dict=node_dict) for c in curr]))

if __name__ == '__main__':
    solve_1()
    solve_2()
