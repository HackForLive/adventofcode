import pathlib
import os

import numpy as np

curr_dir = pathlib.Path(__file__).parent.resolve()
input_file = os.path.join(curr_dir, 'input.txt')

def solve_1():
    with open(input_file, 'rt', encoding='utf8') as f:
        cubes = []
        numbers = [int(number.strip()) for number in f.readline().strip().split(',')]
        i: int = 0
        matrix = np.zeros((5,5))
        for line in f:
            line = line.strip()
            if line == '':
                i = 0
                matrix = np.zeros((5,5))
                continue
            else:
                for idx, j in enumerate([int(k) for k in line.split(' ') if k.isdigit()]):
                    matrix[i][idx] = j

                i+=1
                if i == 5:
                    cubes.append(matrix)

        for number in numbers:
            for cube in cubes:
                mark_cube(cube=cube, number=number)
                if check_cube(cube=cube):
                    return sum_unmarked_cube(cube=cube)*number
                

def solve_2():
     with open(input_file, 'rt', encoding='utf8') as f:
        cubes = []
        numbers = [int(number.strip()) for number in f.readline().strip().split(',')]
        i: int = 0
        matrix = np.zeros((5,5))
        for line in f:
            line = line.strip()
            if line == '':
                i = 0
                matrix = np.zeros((5,5))
                continue
            else:
                for idx, j in enumerate([int(k) for k in line.split(' ') if k.isdigit()]):
                    matrix[i][idx] = j

                i+=1
                if i == 5:
                    cubes.append(matrix)
        
        last = set(range(len(cubes)))

        for number in numbers:
            for idx, cube in enumerate(cubes):
                mark_cube(cube=cube, number=number)
                if idx in last and check_cube(cube=cube):
                    last.remove(idx)
                    if len(last) == 0:
                        return sum_unmarked_cube(cube=cube)*number

def mark_cube(cube: np.ndarray, number: int,  mark: int = -1):
    n = cube.shape[0]
    for i in range(n):
        for j in range(n):
            if cube[i][j] == number:
                cube[i][j] = mark


def check_cube(cube: np.ndarray, mark: int = -1) -> bool:
    n = cube.shape[0]
    for i in range(n):
        sum_row = 0
        sum_col = 0
        for j in range(n):
            if cube[i][j] == mark:
                if sum_row == n - 1:
                    return True
                sum_row += 1
            if cube[j][i] == mark:
                if sum_col == n - 1:
                    return True
                sum_col += 1
    return False


def sum_unmarked_cube(cube: np.ndarray, mark: int = -1) -> int:
    n = cube.shape[0]
    sum = 0
    for i in range(n):
        for j in range(n):
            if cube[i][j] != mark:
                sum += int(cube[i][j])
    return sum
      

if __name__ == '__main__':
    print(solve_1())
    print(solve_2())
