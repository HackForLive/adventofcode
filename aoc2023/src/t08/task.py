from __future__ import annotations
import os
import pathlib
from typing import Dict, List, Tuple


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
                parts = clean_l.split('=')
                node_name = parts[0].strip()

                childs = parts[1].strip().split(',')
                left_name = childs[0].strip()[1:]
                right_name = childs[1].strip()[:-1]

                node_dict[node_name] = (left_name, right_name)

    return instr, node_dict

def solve_1():
    instr, node_dict = parse()

    curr: str = 'AAA'
    steps = 0
    should_run = True
    while should_run:
        for instruction in instr:
            if instruction == 'R':
                curr = node_dict[curr][1]
            elif instruction == 'L':
                curr = node_dict[curr][0]
            steps += 1
            if curr == 'ZZZ':
                should_run = False
                break

    print(steps)

def solve_2():
    instr, node_dict = parse()

    curr: List[str] = [node_name for node_name in node_dict if node_name[-1] == 'A']
    print(curr)

    steps = 0
    should_run = True
    while should_run:
        for instruction in instr:
            should_run = False
            for i in range(0, len(curr), 1):
                if instruction == 'R':
                    curr[i] = node_dict[curr[i]][1]
                elif instruction == 'L':
                    curr[i] = node_dict[curr[i]][0]
                if curr[i][-1] != 'Z':
                    should_run = True
            steps += 1
            if not should_run:
                break

    print(steps)

if __name__ == '__main__':
    # solve_1()
    solve_2()
