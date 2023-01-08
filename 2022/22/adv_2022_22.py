import os
import numpy as np
from operator import add
from collections import deque

class Node:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            getattr(other, 'x', None) == self.x and
            getattr(other, 'y', None) == self.y)

    def __hash__(self):
        return hash(str(self.x) + str(self.y))

"""
param dir:

N, S, W, E
"""
def getCheckDirs(dir: str):

    checkDirs = {
        "N": [
                getDirection("N"),
                list(map(add, getDirection("N"),getDirection("E"))),
                list(map(add, getDirection("N"),getDirection("W")))
            ],
        "S": [
                getDirection("S"),
                list(map(add, getDirection("S"),getDirection("E"))),
                list(map(add, getDirection("S"),getDirection("W")))
            ],
        "E": [
                getDirection("E"),
                list(map(add, getDirection("N"),getDirection("E"))),
                list(map(add, getDirection("S"),getDirection("E")))
            ],
        "W": [  getDirection("W"),
                list(map(add, getDirection("N"),getDirection("W"))),
                list(map(add, getDirection("S"),getDirection("W")))
            ],
    }

    return checkDirs[dir]

def getDirection(dir: str):
    dirs = {
        "N": [-1,0],
        "S": [1,0],
        "W": [0,-1],
        "E": [0,1]
    }

    return dirs[dir]

def getNodePosition(node: Node, nodes, round: int):
    checkDirsOrder = {
        0: "N",
        1: "S",
        2: "W",
        3: "E",
    }

if __name__ == "__main__" :
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
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
            tmpN = 1
            tmpM = 0
            for j in reversed(range(len(instr))):
                if instr[j].isdigit():
                    tmpM = tmpM + int(instr[j]) * tmpN
                    tmpN *= 10
                elif tmpM > 0:
                    instructions.append(tmpM)
                    tmpN = 1
                    tmpM = 0
                if  instr[j] == 'L':
                    instructions.append(instr[j])
                elif  instr[j] == 'R':
                    instructions.append(instr[j])
            if tmpM > 0:
                instructions.append(tmpM)
            break
        else:
            for c in range(len(line)):
                if line[c] == '.':
                    mat2d[i][c] = 1
                elif line[c] == '#':
                    mat2d[i][c] = 2

    while instructions:
        print(instructions.pop())

    # for i in ROW:
    print(mat2d)
