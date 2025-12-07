from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

import numpy as np

def find_start(start: str, matrix: np.ndarray) -> list[tuple[int, int]]:
    return [(int(i[0]), int(i[1])) for i in zip(*np.where(matrix == start))]

def find_splits(start: str, matrix: np.ndarray) -> list[tuple[int, int]]:
    return [(int(i[0]), int(i[1])) for i in zip(*np.where(matrix == start))]


def count_splits(matrix: np.matrix, start: tuple[int, int]) -> int:

    streams = set([start])
    res = 0
    ok = True

    while ok:
        next_streams = set()
        for s in streams:
            next_p =  (s[0]+1, s[1])
            if s[0]+1 >= matrix.shape[0]:
                ok = False
                break
            if matrix[next_p] == '.':
                next_streams.add(next_p)
            if matrix[next_p] == '^':
                next_streams.add((s[0]+1, s[1]-1))
                next_streams.add((s[0]+1, s[1]+1))
                res += 1

        streams = next_streams

    return res

def count_all_paths(matrix: np.matrix, start: tuple[int, int]) -> int:

    streams = set([start])
    res = 0
    ok = True

    track = {}

    while ok:
        next_streams = []
        for s in streams:
            next_p =  (s[0]+1, s[1])
            if s[0]+1 >= matrix.shape[0]:
                ok = False
                res += track[s]
                continue
            if matrix[next_p] == '.':
                next_streams.append(next_p)
                track[next_p] = track.get(s, 1) + track.get(next_p, 0) 
            if matrix[next_p] == '^':
                le = (s[0]+1, s[1]-1)
                ri = (s[0]+1, s[1]+1) 
                next_streams.append(le)
                next_streams.append(ri)
                track[le] = track.get(s, 1) + track.get(le, 0) 
                track[ri] = track.get(s, 1) + track.get(ri, 0)

        streams = set(next_streams)
    return res

def count_splits_tbfixed(splits: list[tuple[int,int]], start: tuple[int, int]) -> int:
    splits_y = sorted(splits, key=lambda x: (x[0], x[1]))

    streams = set([start])

    res = 0

    print(f"{len(splits_y) =}")


    for spl in splits_y: # from top to bottom

        # print(streams)
        match_s = None
        le = None
        ri = None
        for stre in streams:
            if spl[1] == stre[1] and stre[0] < spl[0]:
                # split
                res += 1
                le = (spl[0], spl[1] - 1)
                ri = (spl[0], spl[1] + 1)
                match_s = stre
                break
        
        if match_s and le and ri:
            streams.remove(match_s)
            streams.add(le)
            streams.add(ri)
            # print(streams)
    return res


@timer_decorator
def solve_1(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)

        start = find_splits(start='S', matrix=matrix)
        # splits = find_splits(start='^', matrix=matrix)

        return count_splits(matrix=matrix, start=start[0])
    
@timer_decorator
def solve_2(p: Path) -> int:
    with open(p, encoding='utf-8', mode='r') as f:
        arr_2d = np.array([[c for c in line.strip()] for line in f.readlines()])
        matrix = np.asmatrix(arr_2d)
        start = find_splits(start='S', matrix=matrix)
        return count_all_paths(matrix=matrix, start=start[0])
    
if __name__ == '__main__':
    assert solve_1(p=t_f) == 21
    print(solve_1(p=in_f)) # 1553
    assert solve_2(p=t_f) == 40
    print(solve_2(p=in_f)) # 15811946526915
    print("All passed!")
