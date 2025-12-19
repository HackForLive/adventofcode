
import dataclasses
from pathlib import Path

from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

@dataclasses.dataclass(frozen=True, init=True)
class Board:
    wide: int
    long: int
    indices: list[int]

def rotate(shape) -> list[tuple[int, int]]:
    return [(y, 2 - x) for x, y in shape]

def flip(shape) -> list[tuple[int, int]]:
    return [(2 - x, y) for x, y in shape]   # horizontal flip

def all_orientations(shape):
    seen = set()
    shapes = []

    cur = shape
    for _ in range(4):
        cur = rotate(cur)
        for s in (cur, flip(cur)):
            n = tuple(sorted(s, key=lambda x: (x[0], x[1])))
            if n not in seen:
                seen.add(n)
                shapes.append(list(n))
    return shapes

def compute(presents: dict[str, list[tuple[int,int]]], wide: int, long: int, indices: list[int], 
            max_l: int, max_w: int) -> int:

    # naive put all 3x3
    alls = sum(indices)

    upper_bound = wide*long
    # 3x3
    if upper_bound >= alls*max_l*max_w: 
        return 1
    return 0

def compute_all(presents: dict[str, list[tuple[int,int]]], boards: list[Board], max_l: int, max_w: int) -> int:
    return sum(compute(presents=presents, wide=b.wide, long=b.long, indices=b.indices, max_l=max_l, 
                       max_w=max_w) for b in boards)

@timer_decorator
def solve_1(p: Path):
    presents = {}
    boards = []
    with open(p, 'r', encoding='utf8') as f:
        last_p_id = 0
        last_p = []
        i = 0

        max_l = 0 
        max_w = 0
        for l in f:
            line = l.strip()

            if 'x' in line:
                le, ri = l.strip().split(':')

                wide, long = map(int, le.split('x'))
                indices = list(map(int, ri.split()))

                boards.append(Board(wide=wide, long=long, indices=indices))
            if ':' in line:
                last_p_id = int(line[0])
                last_p = []
                i = 0
            elif not line:
                presents[last_p_id] = last_p                
                continue
            elif any(i in line for i in ('#', '.')):
                last_p.extend(((i,j) for j in line if j == '#'))
                i += 1
                max_w = max(max_w, len(line))
                max_l = max(max_l, i)

    return compute_all(presents=presents, boards=boards, max_w=max_w, max_l=max_l)

if __name__ == '__main__':
    print(solve_1(p=t_f)) # incorrect
    print(solve_1(p=in_f)) # 591

    print("All passed!")
