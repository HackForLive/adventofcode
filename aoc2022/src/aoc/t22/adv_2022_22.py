import os
from collections import deque
import copy

import numpy as np

from aoc.t22.point import Node


def get_direction(direction: str):
    """
    Get y,x list based on direction
    """
    directions = {
        "N": [-1,0],
        "S": [1,0],
        "W": [0,-1],
        "E": [0,1]
    }

    return directions[direction]

def get_direction_val(direction: str):
    directions = {
        "N": 3,
        "S": 1,
        "W": 2,
        "E": 0
    }

    return directions[direction]

def get_next_left_dir(direction: str):
    """
    Turn 90 degrees in counter clockwise manner 
    """
    directions = {
        "N": 0,
        "W": 1,
        "S": 2,
        "E": 3
    }
    directions_reversed = dict((v, k) for k, v in directions.items())

    numb = (directions[direction] + 1) % len(directions)
    return directions_reversed[numb]

def get_next_right_dir(direction: str):
    """
    Turn 90 degrees in clockwise manner 
    """
    directions = {
        "N": 0,
        "E": 1,
        "S": 2,
        "W": 3
    }
    directions_reversed = dict((v, k) for k, v in directions.items())

    numb = (directions[direction] + 1) % len(directions)
    return directions_reversed[numb]

def get_start_position(mat2d):
    for i in range(len(mat2d)):
        for j in range(len(mat2d[0])):
            if mat2d[i][j] == 1:
                return Node(x = j, y = i, direction = "E")
    return None

def is_eligible_to_go(x: int, y: int, mat2d):
    return x >= 0 and y >=0 and y < len(mat2d) and x < len(mat2d[0]) and (mat2d[y][x] == 1 or mat2d[y][x] == 2)

def wrap_around(dir, curr: Node, mat2d):
    x = curr.x
    y = curr.y
    while is_eligible_to_go(x=x, y=y, mat2d=mat2d):
        x -= dir[1]
        y -= dir[0]
    
    if mat2d[y + dir[0]][x + dir[1]] == 1:
        curr.x = x + dir[1]
        curr.y = y + dir[0]


def go_dir(curr: Node, steps: int, mat2d):
    dir = get_direction(curr.direction)

    # eligible to go
    # next step is wall
    # wrap around
    for i in range(steps):
        y = curr.y + dir[0]
        x = curr.x + dir[1]
        if is_eligible_to_go(x=x, y=y, mat2d=mat2d):
            # wall
            if mat2d[y][x] == 2:
                break
            elif mat2d[y][x] == 1:
                curr.y = y
                curr.x = x
        else:
            wrap_around(dir=dir, curr=curr, mat2d=mat2d)

def turn_left(curr:Node):
    curr.direction = get_next_left_dir(curr.direction)

def turn_right(curr:Node):
    curr.direction = get_next_right_dir(curr.direction)

def get_result(instructions, mat2d):
    instrs = copy.deepcopy(instructions)
    curr: Node = get_start_position(mat2d=mat2d)
    while instrs:
        instr = instrs.pop()
        # number
        # print('start')
        # print(f"{curr.x = } {curr.y = } {curr.direction = }")
        if isinstance(instr, int):
            go_dir(curr=curr, steps= instr, mat2d= mat2d)
        elif instr == "R":
            turn_right(curr=curr)
        elif instr == "L":
            turn_left(curr=curr)
        else:
            raise ValueError(f'Uknown instruction: {instr:%s}')
        # print(f"{curr.x = } {curr.y = } {curr.direction = }")
        # print('end')
    return (curr.y + 1) * 1000 + (curr.x + 1) * 4 + get_direction_val(curr.direction)

if __name__ == "__main__" :
    f = open(file=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'),
        mode='r', encoding="UTF8")
    lines = f.readlines()

    n = len(lines)
    instructions = deque()

    ROW = 0
    COL = -1
    for i in range(n):
        lineN = len(lines[i][:-1])
        if lineN == 0:
            break
        ROW += 1
        COL = max(COL, lineN)

    mat2d = np.zeros((ROW, COL))

    for i in range(n):
        line = lines[i][:-1]
        
        if line == "":
            instr = lines[i+1].strip()
            tmp_n = 1
            tmp_m = 0
            for j in reversed(range(len(instr))):
                if instr[j].isdigit():
                    tmp_m = tmp_m + int(instr[j]) * tmp_n
                    tmp_n *= 10
                elif tmp_m > 0:
                    instructions.append(tmp_m)
                    tmp_n = 1
                    tmp_m = 0
                if  instr[j] == 'L':
                    instructions.append(instr[j])
                elif  instr[j] == 'R':
                    instructions.append(instr[j])
            if tmp_m > 0:
                instructions.append(tmp_m)
            break
        else:
            for j, c in enumerate(line):
                if c == '.':
                    mat2d[i][j] = 1
                elif c == '#':
                    mat2d[i][j] = 2

    print(get_result(instructions, mat2d))
    # while instructions:
    #     print(instructions.pop())

    # # for i in ROW:
    # print(mat2d)
