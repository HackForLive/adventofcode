import os
import pathlib

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
mt_file = os.path.join(curr_dir, 'mt.txt')

A = np.matrix([[1, 1], [1, 1]])

E = np.tile(A,(5,5))
for i in range(0,5):
    for j in range(0,5):
        E[i*2:(i+1)*2,j*2:(j+1)*2] = (A + A*(j+i))%4
        print(E)

with open(mt_file, mode='w', encoding='utf-8') as f:
    np.savetxt(f, E, fmt='%.0f', delimiter=',')

print(A)
# print(E)

print(9%10)