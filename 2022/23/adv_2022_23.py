import os
import numpy as np
from operator import add

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

    shouldMove: bool = False
    resultDir = None
    for j in range(round, round + len(checkDirsOrder)):
        canMoveInDirection: bool = True
        for dir in getCheckDirs(checkDirsOrder[j%len(checkDirsOrder)]):
            proposed: Node = Node(node.x + dir[1], node.y + dir[0])
            # found !!!
            if proposed in nodes:
                shouldMove = True
                canMoveInDirection = False
                break
        # take first
        if not resultDir and canMoveInDirection:
            resultDir = getDirection(checkDirsOrder[j%len(checkDirsOrder)])

    if shouldMove:
        return resultDir    
    else:
        return None

def doSimulation(rounds: int, nodes):
    currentRound: int = 0

    while currentRound < rounds:
        # printCurrentState(nodes, row, col)
        proposedNodes = {}
        for node in nodes:
            pos = getNodePosition(node, nodes, currentRound)
            if pos:
                proposedNode: Node = Node(node.x + pos[1], node.y + pos[0])
                if proposedNode in proposedNodes:
                    proposedNodes[proposedNode].append(node)
                else:
                    proposedNodes[proposedNode] = [node]
        
        if len(proposedNodes) == 0:
            print(currentRound+1)
            break
        for proposedNode in proposedNodes:
            if len(proposedNodes[proposedNode]) == 1:
                if proposedNodes[proposedNode][0] in nodes:
                    nodes.remove(proposedNodes[proposedNode][0])
                nodes.add(proposedNode)
                
        currentRound += 1

# def printCurrentState(nodes, n: int, m: int):
#     mat2d = np.zeros((n+3,m+3))

#     for node in nodes:
#         mat2d[node.y][node.x] = 1
    
#     print(mat2d)

def getEmptyPlaces(nodes):
    mins = [100000, 100000]
    maxs = [-100000, -100000]

    for node in nodes:
        if node.x < mins[1]:
            mins[1] = node.x
        if node.x > maxs[1]:
            maxs[1] = node.x
        if node.y < mins[0]:
            mins[0] = node.y
        if node.y > maxs[0]:
            maxs[0] = node.y

    return (maxs[0]-mins[0]+1)*(maxs[1]-mins[1]+1) - len(nodes)
if __name__ == "__main__" :
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input2.txt'), 'r')
    lines = f.readlines()

    nodes = set()
    n = len(lines)
    rounds: int = 2000
    for i in range(n):
        line = lines[i].strip()
        for j in range(len(line)):
            if line[j] == '#':
                x = j
                y = i
                nodes.add(Node(x,y))

    doSimulation(rounds=rounds, nodes=nodes)
    print(getEmptyPlaces(nodes))
