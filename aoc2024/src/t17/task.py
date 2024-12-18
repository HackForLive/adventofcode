from __future__ import annotations
from collections import deque
import heapq
import itertools
from pathlib import Path
import re
from typing import List, Set, Tuple

from dataclasses import dataclass

from aoc.model.direction import Direction, get_next_left_dir, get_next_right_dir
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
t2_f = curr_dir / 'test2.txt'
in_f = curr_dir / 'in.txt'


def get_lit(lit: int, reg_a: int, reg_b:int, reg_c: int) -> int:
    if 0<= lit <= 3:
        return lit
    elif lit == 4:
        return reg_a
    elif lit == 5:
        return reg_b
    elif lit == 6:
        return reg_c
    raise NotImplementedError()

def get_program_output(reg_a: int, reg_b: int, reg_c:int, prog: List[int]) -> str:
    # print(f"{reg_a=}")
    # print(f"{reg_b=}")
    # print(f"{reg_c=}")
    # print(f"{prog=}")

    instr_pointer = 0 # pointing at first number in prog increase by 2 if not increased by jump pointer
    # trying to read ops code outside end of program, program halts
    output = []

    while instr_pointer < (len(prog) - 1):

        opcode = prog[instr_pointer]
        operand = prog[instr_pointer+1]
        
        # print(instr_pointer)
        if opcode == 0:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_a = reg_a // 2**lit_v
        elif opcode == 1:
            reg_b ^= operand
        elif opcode == 2:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_b =  lit_v % 8
        elif opcode == 3:
            if reg_a != 0 and instr_pointer != operand:
                instr_pointer = operand
                continue
        elif opcode == 4:
            reg_b ^= reg_c
        elif opcode == 5:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            output.append(lit_v % 8)
        elif opcode == 6:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_b = reg_a // 2**lit_v
        elif opcode == 7:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_c = reg_a // 2**lit_v

        instr_pointer += 2
    return ','.join([str(i) for i in output])

def get_program_output_2(reg_a: int, reg_b: int, reg_c:int, prog: List[int]) -> str:
    # print(f"{reg_a=}")
    # print(f"{reg_b=}")
    # print(f"{reg_c=}")
    # print(f"{prog=}")

    instr_pointer = 0 # pointing at first number in prog increase by 2 if not increased by jump pointer
    # trying to read ops code outside end of program, program halts
    output = []

    i = 0
    while instr_pointer < (len(prog) - 1):

        opcode = prog[instr_pointer]
        operand = prog[instr_pointer+1]
        
        # print(instr_pointer)
        if opcode == 0:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_a = reg_a // 2**lit_v
        elif opcode == 1:
            reg_b ^= operand
        elif opcode == 2:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_b =  lit_v % 8
        elif opcode == 3:
            if reg_a != 0 and instr_pointer != operand:
                instr_pointer = operand
                continue
        elif opcode == 4:
            reg_b ^= reg_c
        elif opcode == 5:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            
            if lit_v % 8 != prog[i]:
                return f"{i}"
            output.append(lit_v % 8)
            i+=1
        elif opcode == 6:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_b = reg_a // 2**lit_v
        elif opcode == 7:
            lit_v = get_lit(lit=operand, reg_a=reg_a, reg_b=reg_b, reg_c=reg_c)
            reg_c = reg_a // 2**lit_v

        instr_pointer += 2
    return ','.join([str(i) for i in output])
 
def find_reg_a_to_program_copy(reg_a: int, reg_b: int, reg_c:int, prog: List[int]) -> int:
    to_match = ','.join([str(i) for i in prog])
    
    start_a = 8**15
    end_a = 8**16
    diffs = [8**15]
    for a in range(start_a, end_a, 1):
        output = get_program_output_2(reg_a=a, reg_b=reg_b, reg_c=reg_c, prog=prog)
        if int(output) > 4:
            diffs.append(a)
            if len(diffs) > 200:
                break
            # print(a)
            # print(output)
        # print(a)
        if output == to_match:
            return a
    
    offset = diffs[1] - diffs[0]
    # manually set the repeating seq
    fifths = [diffs[i] - diffs[i-1] for i in range(1,len(diffs))][1:95]
    
    repeatingGenerator = itertools.cycle(fifths)
    # offset = 10794
    start_a = 8**15 + offset

    j = start_a
    diffs = [j]
    for ii, i in enumerate(repeatingGenerator):
        if j > 8**16:
            break
        output = get_program_output_2(reg_a=j, reg_b=reg_b, reg_c=reg_c, prog=prog)
        if int(output) > 9:
            diffs.append(j)
            if len(diffs) > 200:
                # print([diffs[i] - diffs[i-1] for i in range(1,len(diffs))])
                break
            # print(f"{j =}")
            # print(f"{output =}")
        if output == to_match:
            return j
        j = j + i

    offset = offset + diffs[1] - diffs[0]
    # manually set the repeating seq
    tenths = [diffs[i] - diffs[i-1] for i in range(1,len(diffs))][1:40]
    print(offset)
    print(offset - (diffs[1] - diffs[0]))
    print(tenths)

    repeatingGenerator = itertools.cycle(tenths)
    start_a = 8**15 + offset
    j = start_a

    for ii, i in enumerate(repeatingGenerator):
        if j > 8**16:
            break
        output = get_program_output_2(reg_a=j, reg_b=reg_b, reg_c=reg_c, prog=prog)
        if output == to_match:
            return j
        if int(output) > 14:
            diffs.append(j)
        if output == to_match:
            return j
        j = j + i
    return -1

def parse(p: Path):
    reg_a = -1
    reg_b = -1
    reg_c = -1

    prog = []
    with open(p, 'r', encoding='utf8') as f:
        for line in f:
            if line.startswith('Register A:'):
                matches = re.findall('(\\d+)', line)
                reg_a = int(matches[0])
            elif line.startswith('Register B:'):
                matches = re.findall('(\\d+)', line)
                reg_b = int(matches[0])
            elif line.startswith('Register C:'):
                matches = re.findall('(\\d+)', line)
                reg_c = int(matches[0])
            elif line.startswith('Program:'):
                prog = [int(c) for c in line.strip().split(':')[1].split(',')]
        return reg_a, reg_b, reg_c, prog

@timer_decorator
def solve_1(p: Path) -> str:
    reg_a, reg_b, reg_c, prog = parse(p=p)
    return get_program_output(reg_a=reg_a, reg_b=reg_b, reg_c=reg_c, prog=prog)

@timer_decorator
def solve_2(p: Path) -> int:
    reg_a, reg_b, reg_c, prog = parse(p=p)
    return find_reg_a_to_program_copy(reg_a=reg_a, reg_b=reg_b, reg_c=reg_c, prog=prog)


if __name__ == '__main__':
    assert solve_1(p=t_f) == '4,6,3,5,6,3,5,2,1,0'
    assert solve_1(p=in_f) == '1,3,7,4,6,4,2,3,5'
    # assert solve_2(p=t2_f) == 117440
    # 202367025818154
    print(solve_2(p=in_f))
    print("All passed!")
