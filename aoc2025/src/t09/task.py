from pathlib import Path

from aoc.model.geometry import Point3D
from aoc.performance import timer_decorator

curr_dir = Path(__file__).parent
t_f = curr_dir / 'test.txt'
in_f = curr_dir / 'in.txt'

def compute(pts: list[tuple[int,int]]):
    return max(((abs(s[0]-f[0])+1)*(abs(s[1]-f[1])+1) for f in pts for s in pts))


@timer_decorator
def solve_1(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y = [int(i) for i in l.strip().split(',')]
            points.append((x,y))

    return compute(pts=points)

@timer_decorator
def solve_2(p: Path):
    points = []
    with open(p, 'r', encoding='utf8') as f:
        for l in f:
            x,y = [int(i) for i in l.strip().split(',')]
            points.append((x,y))

    return compute(pts=points)

if __name__ == '__main__':
    assert solve_1(p=t_f) == 50
    print(solve_1(p=in_f)) # 4744899849

    # assert solve_2(p=t_f) == 24
    # print(solve_2(p=in_f)) # 7858808482092
    print("All passed!")
