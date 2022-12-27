import os
import numpy as np

class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

if __name__ == "__main__" :
    f = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'input.txt'), 'r')
    lines = f.readlines()

    res:int = 0
    l = []
    mat3d = np.zeros((500,)*3)
    n = len(lines)             
    for i in range(n):
        coord = lines[i].strip().split(",")
        x = int(coord[0])
        y = int(coord[1])
        z = int(coord[2])
        mat3d[z][y][x] = 1
        l.append(Cube(x,y,z))

    v = [[0,0,1],[0,0,-1],[0,1,0],[0,-1,0],[1,0,0],[-1,0,0]]

    s = sorted(l, key=lambda i: ( i.x, i.y,i.z ), reverse=True)
    for a in l:
        for dir in v:
            if mat3d[a.z + dir[0]][a.y + dir[1]][a.x + dir[2]] == 0:
                res += 1

    print(res)