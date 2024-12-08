from pathlib import Path
from typing import List, Set, Tuple

import numpy as np

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'


def is_inside_rectangle_area(antenna: Tuple[int, int], size: Tuple[int, int]) -> bool:
    return (0 <= antenna[0] < size[0]) and (0 <= antenna[1] < size[1])    


def unique_antinodes_for_antennas(antennas: List[Tuple[int, int]], size: Tuple[int, int]
                                  ) -> Set[Tuple[int, int]]:
    res = set()
    for idx in range(len(antennas)):
        for jdx in range(idx+1, len(antennas)):
            first = (
                    antennas[idx][0] + (antennas[idx][0] - antennas[jdx][0]),
                    antennas[idx][1] + (antennas[idx][1] - antennas[jdx][1])
            )
            if is_inside_rectangle_area(antenna=first, size=size):
                res.add(first)
            
            second = (
                    antennas[jdx][0] + (antennas[jdx][0] - antennas[idx][0]),
                    antennas[jdx][1] + (antennas[jdx][1] - antennas[idx][1])
            )

            if is_inside_rectangle_area(antenna=second, size=size):
                res.add(second)
    return res

def unique_antinodes_for_antennas_with_resonance(antennas: List[Tuple[int, int]], size: Tuple[int, int]
                                  ) -> Set[Tuple[int, int]]:
    res = set()
    for idx in range(len(antennas)):
        for jdx in range(idx+1, len(antennas)):

            i = 1
            while True:
                first = (
                        antennas[idx][0] + i*(antennas[idx][0] - antennas[jdx][0]),
                        antennas[idx][1] + i*(antennas[idx][1] - antennas[jdx][1])
                )
                if is_inside_rectangle_area(antenna=first, size=size):
                    res.add(first)
                    i += 1
                else:
                    break
                
            i = 1
            while True:
                second = (
                        antennas[jdx][0] + i*(antennas[jdx][0] - antennas[idx][0]),
                        antennas[jdx][1] + i*(antennas[jdx][1] - antennas[idx][1])
                )

                if is_inside_rectangle_area(antenna=second, size=size):
                    res.add(second)
                    i += 1
                else:
                    break
    return res

def unique_antinode_locations(matrix: np.matrix) -> Set[Tuple[int, int]]:
    antennas = {}

    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == '.':
            continue
        if matrix[y, x] in antennas:
            antennas[str(matrix[y, x])].append((y, x))
        else:
            antennas[str(matrix[y, x])] = [(y, x)]

    res = set()
    for _, ant in antennas.items():
        res = res.union(unique_antinodes_for_antennas(antennas=ant, size=matrix.shape))

    return res

def unique_antinode_locations_with_resonance(matrix: np.matrix) -> Set[Tuple[int, int]]:
    antennas = {}

    for y, x in np.ndindex(matrix.shape):
        if matrix[y, x] == '.':
            continue
        if matrix[y, x] in antennas:
            antennas[str(matrix[y, x])].append((y, x))
        else:
            antennas[str(matrix[y, x])] = [(y, x)]

    res = set()
    for _, ant in antennas.items():
        res = res.union(
            unique_antinodes_for_antennas_with_resonance(antennas=ant, size=matrix.shape)).union(
                ant)
    return res

@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return len(unique_antinode_locations(matrix=matrix))
    

@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        return len(unique_antinode_locations_with_resonance(matrix=matrix))
    

if __name__ == '__main__':
    assert solve_1(p=t_f) == 14
    assert solve_1(p=in_f) == 222
    assert solve_2(p=t_f) == 34
    assert solve_2(p=in_f) == 884
    print("All passed!")
