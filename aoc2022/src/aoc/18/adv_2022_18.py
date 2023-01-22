import os
import numpy as np
from collections import deque

class Cube:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z
    
    def __eq__(self, other):
        return (isinstance(other, self.__class__) and
            getattr(other, 'x', None) == self.x and
            getattr(other, 'y', None) == self.y and
            getattr(other, 'z', None) == self.z)

    def __hash__(self):
        return hash(str(self.x) + str(self.y) + str(self.z))


def hasCubeNonNegativeCoords(cube: Cube):
    return cube.x >= 0 and cube.y >= 0 and cube.z >= 0

def hasCubeLimitedCoords(cube: Cube, limit: int):
    return cube.x < limit and cube.y < limit and cube.z < limit

def BFS(cube: Cube, cubes):
    dxyz = [[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]]
    q = deque()
    q.appendleft(cube)
    outside: bool = False
    maxDepth: int = len(cubes)

    res: int = 0
    while q:
        tmp: Cube = q.pop()
        # is visited?
        if cubes[tmp.z][tmp.y][tmp.x] == 2:
            continue
        else:
            cubes[tmp.z][tmp.y][tmp.x] = 2
        for d in dxyz:
            nextC: Cube = Cube(tmp.x + d[2], tmp.y + d[1], tmp.z + d[0])
            # process only allowed cubes and not visited
            if hasCubeNonNegativeCoords(nextC) and hasCubeLimitedCoords(nextC, maxDepth):
                if cubes[nextC.z][nextC.y][nextC.x] == 0:
                    q.appendleft(nextC)
                elif cubes[nextC.z][nextC.y][nextC.x] == 1:
                    res += 1
                elif cubes[nextC.z][nextC.y][nextC.x] == 2:
                    continue
                else:
                    raise ValueError("Unknown value: %d ", cubes[nextC.z][nextC.y][nextC.x])
            else:
                outside = True
    if outside == True:
        return -1
    return res

if __name__ == "__main__" :
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    res:int = 0
    l = []
    n:int = 21
    mat3d = np.zeros((n,n,n))
    n = len(lines)             
    for i in range(n):
        coord = lines[i].strip().split(",")
        x = int(coord[0])
        y = int(coord[1])
        z = int(coord[2])
        mat3d[z][y][x] = 1
        l.append(Cube(x,y,z))

    v = [[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]]    
    # get surface
    pot_air_cubes = set()
    for a in l:
        for dir in v:
            if mat3d[a.z + dir[0]][a.y + dir[1]][a.x + dir[2]] == 0:
                res += 1
                pot_air_cubes.add(Cube(a.x + dir[2], a.y + dir[1], a.z + dir[0]))
    
    # test them
    # s = sorted(pot_air_cubes, key=lambda i: ( i.x, i.y,i.z ), reverse=True)
    # maxDepth = 20
    for pot_air_cube in pot_air_cubes:
        # print("x: %d, y: %d, z: %d" % (pot_air_cube.x, pot_air_cube.y, pot_air_cube.z))
        bfs = BFS(pot_air_cube, mat3d)
        if bfs > -1: 
            res -= bfs

    print(res)