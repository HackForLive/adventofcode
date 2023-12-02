from dataclasses import dataclass, field
import time
import os
import functools
import pathlib
import heapq
from typing import List, Tuple
from line_profiler import LineProfiler

import numpy as np


curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'test.txt')
matrix_file = os.path.join(curr_dir, 'matrix.txt')


@dataclass(frozen=True, eq=True)
class Node:
    """
    Node in matrix
    """
    x: int
    y: int
    value: int = field(compare=False)
    path: List[Tuple[int, int]] = field(compare=False)

    def __lt__(self, other):
        return self.value < other.value


def timer_decorator(func):
    functools.wraps(func)
    def with_timer(*args, **kwargs):
        t0 = time.time()
        result = func(*args, **kwargs)
        t1 = time.time()
        elapsed = t1 - t0

        print(f"@timer: {func.__name__} took {elapsed:0.4f} seconds")
        return result
    return with_timer

def get_matrix_with_offset(matrix: np.matrix, val: int, offset: int)  -> np.matrix:
    rows, cols = offset, offset
    offset_matrix = np.full((2*rows+matrix.shape[0], 2*cols+matrix.shape[1]), fill_value=val, 
                            dtype=int)
    offset_matrix[rows:rows+matrix.shape[0], cols:cols+matrix.shape[1]] = matrix
    return offset_matrix

def bfs(matrix: np.matrix, offset: int, shape: Tuple[int, int]):
    start = Node(x=0 + offset, y = 0 + offset, value=matrix[0 + offset,0 + offset], path=[])
    q = []
    heapq.heappush(q, start)

    n_max = 100000000

    closest_m = np.zeros(shape=matrix.shape, dtype=int) + n_max
    closest_m[start.y, start.x] = 0

    while q:
        curr = heapq.heappop(q)

        if curr.x == shape[0] and curr.y == shape[1]:
            n_max = closest_m[shape[1], shape[0]]

        for direction in ([-1, 0], [1, 0], [0, 1], [0, -1]):
            x = curr.x + direction[1]
            y = curr.y + direction[0]
            val = matrix[y, x]

            if val == -1 or (closest_m[y, x] <= val + closest_m[curr.y, curr.x]):
                continue
            closest_m[y, x] = val + closest_m[curr.y, curr.x]
            # q.append(Node(x=x, y=y, value=val, path=curr.path + [(y,x)]))
            heapq.heappush(q, Node(x=x, y=y, value=curr.value + val, path=curr.path + [(y,x)]))

    return closest_m[shape[1], shape[0]]


# @timer_decorator
def solve_1():
    offset = 1
    val = -1
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        matrix_with_offset = get_matrix_with_offset(matrix=matrix, val=val, offset=offset)
        res = bfs(matrix=matrix_with_offset, offset=offset, shape=matrix.shape)
        print(res)

def solve_2():
    offset = 1
    val = -1
    extend_val = 5
    # modulo fix = 10 - 1
    mod_val = 9
    with open(input_file, 'r', encoding='utf8') as f:
        arr_2d = np.array([[int(number) for number in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        height = matrix.shape[0]
        width = matrix.shape[1]
        # modulo fix
        matrix = matrix - 1
        matrix_extended = np.tile(matrix,(extend_val,extend_val))
        for i in range(0,extend_val):
            for j in range(0,extend_val):
                matrix_extended[i*height:(i+1)*height,j*width:(j+1)*width] = (
                    matrix + (j+i))%mod_val

        matrix_extended = matrix_extended + 1

        # with open(matrix_file, mode='w', encoding='utf-8') as f:
        #     np.savetxt(f, matrix_extended, fmt='%.0f', delimiter=',')
        # matrix_extended.tofile(matrix_file, sep='\r\n')

        matrix_with_offset = get_matrix_with_offset(matrix=matrix_extended, val=val, offset=offset)
        # print(matrix_with_offset)
        res = bfs(matrix=matrix_with_offset, offset=offset, shape=matrix_extended.shape)
        print(res)


if __name__ == '__main__':
    # solve_1()
    # solve_2()
    lp = LineProfiler()
    lp.add_function(bfs)
    lp_wrapper = lp(solve_2)
    lp_wrapper()
    lp.print_stats()
